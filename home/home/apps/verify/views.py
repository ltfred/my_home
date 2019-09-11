import json
import random
import re
from django import http
from django.views import View
from django_redis import get_redis_connection
from home.utils import constants
from home.utils.response_code import RET
from users.models import User
import logging
from verify.libs.captcha.captcha import captcha

logger = logging.getLogger('django')


class ImageVerifyGenerateView(View):
    """图形验证码"""
    def get(self, request):
        # 获取参数
        cur = request.GET.get('cur')
        pre = request.GET.get('pre')
        # 检验参数
        if not all([cur]):
            return http.JsonResponse({'errno': RET.PARAMERR, 'errmsg': '参数错误'})
        # 链接redis
        redis_conn = get_redis_connection('verify')
        # 创建管道
        pl = redis_conn.pipeline()
        # 生成图形验证码
        text, image = captcha.generate_captcha()
        print(text)
        # 保存图形验证码
        pl.setex('image_code_%s' % cur, constants.IMAGE_VERIFY_CODE, text)
        # 删除之前的验证码
        if pre:
            pl.delete('image_code_%s' % pre)
        # 执行管道
        pl.execute()

        return http.HttpResponse(image, content_type='image/jpg')


class SmsVerifyCodeGenerateView(View):
    """生成短信验证码"""
    def post(self, request):
        # 获取参数
        json_dict = json.loads(request.body.decode())
        mobile = json_dict.get('mobile')
        image_code_client = json_dict.get('image_code')
        uuid = json_dict.get('image_code_id')
        # 检验参数
        if not all([mobile, image_code_client, uuid]):
            return http.JsonResponse({'errno': RET.PARAMERR, 'errmsg': '参数错误'})
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.JsonResponse({'errno': RET.PARAMERR, 'errmsg': '手机号格式错误'})
        # 检验手机是否已注册
        try:

            user = User.objects.get(mobile=mobile)
            if user:
                return http.JsonResponse({'errno': RET.DATAEXIST, 'errmsg': '手机号已注册'})
        except Exception as e:
            logger.error(e)

        # 链接redis,获取图形验证码
        redis_conn = get_redis_connection('verify')
        image_code_server = redis_conn.get('image_code_%s' % uuid)
        if image_code_server is None:
            return http.JsonResponse({'errno': RET.UNKOWNERR, 'errmsg': '图形验证码过期'})
        # 删除图形验证码
        try:
            redis_conn.delete('image_code_%s' % uuid)
        except Exception as e:
            logger.error(e)

        # 检验图形验证码是否正确
        if image_code_server.decode().lower() != image_code_client.lower():
            return http.JsonResponse({'errno': RET.UNKOWNERR, 'errmsg': '图形验证码不正确'})
        # 发送验证码之前判断标志是否存在
        sms_flag = redis_conn.get('sma_code_flag_%s' % mobile)
        if sms_flag:
            return http.JsonResponse({'errno': RET.UNKOWNERR, 'errmsg': '发送手机验证码过于频繁'})

        # 生成手机验证码
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info(sms_code)
        # 保存手机验证码
        redis_conn.setex('sms_code_%s' % mobile, constants.SMS_VERIFY_CODE_EXPIRY, sms_code)
        # 避免重复发送短信验证码
        redis_conn.setex('sma_code_flag_%s' % mobile, constants.SMS_CODE_FLAG_EXPIRY, constants.SMS_CODE_FLAG)
        # 发送短信验证码
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)

        return http.JsonResponse({'errno': RET.OK, 'errmsg': '短信发送成功'})


