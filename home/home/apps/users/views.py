import json
from django import http
from django.contrib.auth import login
from django.views import View
from django_redis import get_redis_connection
import logging
from redis import StrictRedis
from home.utils.response_code import RET
from users.models import User

logger = logging.getLogger('django')


class Register(View):
    """用户注册"""

    def post(self, request):
        # 1. 获取参数并进行参数校验
        data_dict = json.loads(request.body.decode())
        mobile = data_dict.get("mobile")  # 获取手机号
        phonecode = data_dict.get("phonecode")  # 获取短信验证码
        password = data_dict.get("password")  # 密码
        password2 = data_dict.get('password2')  # 密码2

        # 判断参数是否完整
        if not all([mobile, phonecode, password, password2]):
            return http.JsonResponse({'errno': RET.PARAMERR, 'errmsg': "参数不全"})

        # 判断密码是否一致
        if password != password2:
            return http.JsonResponse({'errno': RET.PWDERR, 'errmsg': "密码不一致"})

        # 2. 从redis中获取指定手机号对应的短信验证码的
        redis_conn = get_redis_connection('verify_code')  # type: StrictRedis
        try:
            sms_code = redis_conn.get("SMS_" + mobile)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'errno': RET.DBERR, 'errmsg': "获取本地验证码失败"})

        if not sms_code:
            return http.JsonResponse({'errno': RET.NODATA, 'errmsg': "短信验证码过期"})

        # 3. 校验验证码
        if phonecode != sms_code.decode():
            return http.JsonResponse({'errno': RET.DATAERR, 'errmsg': "短信验证码错误"})

        # 4. 初始化 user 模型，并设置数据并添加到数据库
        try:
            user = User.objects.create_user(username=mobile, mobile=mobile, password=password)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'errno': RET.DATAERR, 'errmsg': "用户创建失败"})

        # 状态保持
        login(request, user)
        return http.JsonResponse({'errno': RET.OK, 'errmsg': "注册成功"})
