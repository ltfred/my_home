import json
from django import http
from django.contrib.auth import login
from django.views import View
from django_redis import get_redis_connection
import logging
from redis import StrictRedis
from home.utils.common import LoginRequiredMixin
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


class Session(View):
    """用户状态查询"""

    def get(self, request):
        """检测用户是否登录，如果登录，则返回用户名和用户id"""

        user = request.user
        if user.is_authenticated:
            data = {'user_id': user.id, 'name': user.username}
            return http.JsonResponse({'errno': RET.OK, 'errmsg': "OK", 'data': data})

        return http.JsonResponse({'errno': RET.SESSIONERR, 'errmsg': '用户未登录'})


class Logout(LoginRequiredMixin, View):
    """用户退出"""

    def delete(self, request):

        # 清除session
        Logout(request)
        return http.JsonResponse({'errno': RET.OK, 'errmsg': "用户已退出"})


class Login(View):

    def post(self, request):
        # 1. 获取参数和判断是否有值
        data_dict = json.loads(request.body.decode())

        mobile = data_dict.get("mobile")
        password = data_dict.get("password")

        if not all([mobile, password]):
            return http.JsonResponse({'errno': RET.PARAMERR, 'errmsg': "参数不全"})

        # 2. 从数据库查询出指定的用户
        try:
            user = User.objects.get(mobile=mobile)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'errno': RET.DBERR, 'errmsg': "用户不存在"})

        # 3. 校验密码
        if not user.check_password(password):
            return http.JsonResponse({'errno': RET.PWDERR, 'errmsg': "密码错误"})

        # 4. 保存用户登录状态
        login(request, user)

        # 5. 返回结果
        return http.JsonResponse({'errno': RET.OK, 'errmsg': "登录成功"})