from django.conf.urls import url

from users import views

urlpatterns = [
    # 用户注册
    url(r'^api/v1.0/user/register/$', views.Register.as_view(), name='smscode'),
    # 用户状态
    url(r'^api/v1.0/session/$', views.Session.as_view(), name='session'),
    # 用户登录
    url(r'^api/v1.0/login/$', views.Login.as_view(), name='login'),
    # 用户退出
    url(r'^api/v1.0/logout/$', views.Logout.as_view(), name='logout'),
    # 用户图像上传
    url(r'^api/v1.0/user/avatar/$', views.UserAvatar.as_view(), name='avatar'),
    # 用户信息获取/修改
    url(r'^api/v1.0/user/profile/$', views.AuthProfile.as_view(), name='profile'),

]