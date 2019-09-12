from django.conf.urls import url

from house import views

urlpatterns = [

    # 发布新房源
    url(r'^api/v1.0/houses/$', views.NewHouseView.as_view()),
    # 房源图片
    url(r'api/v1.0/houses/(?P<house_id>\d+)/images/$', views.HouseImageView.as_view()),
    # 我的房源
    url(r'^api/v1.0/user/houses/$', views.MyHousesView.as_view()),
    # 房源详情
    url(r'^api/v1.0/houses/(?P<house_id>\d+)/$', views.HouseDetailView.as_view()),
    # 首页房源推荐
    url(r'^api/v1.0/houses/index/$', views.IndexHouseView.as_view()),
    # 首页搜索
    url(r'^api/v1.0/houses/search/$', views.IndexSearch.as_view())
]