from django.conf.urls import url

from order import views

urlpatterns = [
    # 我的订单
    url(r'^api/v1.0/orders/$', views.AddOrderView.as_view()),
    # 评价订单
    url(r'^api/v1.0/orders/comment/$', views.OrderComment.as_view()),
]
