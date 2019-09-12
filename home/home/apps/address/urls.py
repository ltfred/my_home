from django.conf.urls import url

from address import views

urlpatterns = [
    # 区域信息
    url(r'^api/v1.0/areas/$', views.AreasView.as_view()),
]