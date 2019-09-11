from django.conf.urls import url

from house import views

urlpatterns = [
    # 区域信息
    url(r'^api/v1.0/areas/$', views.AreasView.as_view()),
    # 发布新房源
    url(r'^api/v1.0/houses/$', views.NewHouseView.as_view()),
    # 房源图片
    url(r'api/v1.0/houses/(?P<house_id>\d+)/images/$', views.HouseImageView.as_view()),
]