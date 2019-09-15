from django.conf.urls import url

from verify import views

urlpatterns = [
    url(r'^api/v1.0/imagecode/$', views.ImageVerifyGenerateView.as_view()),
    url(r'^api/v1.0/smscode/$', views.SmsVerifyCodeGenerateView.as_view()),
]