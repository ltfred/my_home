from django.db import models
from home.utils.models import BaseModel
from users.models import User
from house.models import House


class Order(BaseModel):
    '''订单'''
    ORDER_STATUS_CHOICES = (
        ("WAIT_ACCEPT", '待接单'),
        ('WAIT_PAYMENT', '待支付'),
        ('PAID', '已支付'),
        ('WAIT_COMMENT', '待评价'),
        ('COMPLETE', '已完成'),
        ('CANCELED', '已取消'),
        ('REJECTED', '已拒单'),

    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户订单')
    house = models.ForeignKey(House, on_delete=models.SET_NULL, verbose_name='房屋订单', null=True)
    begin_date = models.DateTimeField(null=False, verbose_name='预订的起始时间')
    end_date = models.DateTimeField(null=False, verbose_name='预订的结束时间')
    days = models.IntegerField(null=False, verbose_name='预订的总天数')
    house_price = models.IntegerField(null=False, verbose_name='房屋的单价')
    amount = models.IntegerField(null=False, verbose_name='订单的总金额')
    comment = models.TextField(verbose_name='订单的评论信息或拒单原因')
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default='WAIT_ACCEPT', verbose_name="订单状态")

    class Meta:
        db_table = 'ih_order_info'
