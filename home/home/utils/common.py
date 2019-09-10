from django.contrib.auth.decorators import login_required

from django import http

from home.utils.response_code import RET


def login_required_json(view_func):
    """
    判断用户是否登录的装饰器，并返回 json
    :param view_func: 被装饰的视图函数
    :return: json、view_func
    """

    def wrapper(request, *args, **kwargs):

        # 如果用户未登录，返回 json 数据
        if not request.user.is_authenticated():
            return http.JsonResponse({"errno": RET.SESSIONERR, "errmsg": "未登录"})
        else:
            # 如果用户登录，进入到 view_func 中
            return view_func(request, *args, **kwargs)

    return wrapper


class LoginRequiredJSONMixin(object):
    """验证用户是否登陆并返回 json 的扩展类"""

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return login_required_json(view)


"""验证用户是否登陆，并实名认证"""


def verify_required_json(view_func):
    """
    判断用户是否登录的装饰器，并返回 json
    :param view_func: 被装饰的视图函数
    :return: json、view_func
    """

    def wrapper(request, *args, **kwargs):

        # 如果用户未登录，返回 json 数据
        if not request.user.is_authenticated():
            return http.JsonResponse({"errno": RET.SESSIONERR, "errmsg": "未登录"})
        else:
            # 判断用户是否实名认证
            if not request.user.real_name:
                return http.JsonResponse({"errno": RET.ROLEERR, "errmsg": "未实名认证"})
            # 如果用户登录，进入到 view_func 中
            return view_func(request, *args, **kwargs)

    return wrapper


class VerifyRequiredJSONMixin(object):
    """验证用户是否登陆，并实名认证"""

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return login_required_json(view)
