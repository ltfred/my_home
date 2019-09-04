from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    """验证用户是否登录的扩展类"""

    @classmethod
    def as_view(cls, **initkwargs):
        # 调用父类的 as_view() 函数
        view = super().as_view()
        return login_required(view)
