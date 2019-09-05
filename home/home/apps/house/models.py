from django.db import models
from home.utils.fastdfs.models import BaseModel


class House(BaseModel):
    '''房屋信息'''
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='房屋用户')
    area = models.ForeignKey('address.Area', on_delete=models.SET_NULL, null=True, verbose_name='房屋地区')
    title = models.CharField(max_length=64, null=False, verbose_name='房屋标题')
    price = models.IntegerField(default=0, verbose_name='房屋单价')  # 单价分
    address = models.CharField(max_length=512, default='', verbose_name='房屋地址')
    room_count = models.IntegerField(default=1, verbose_name='房间数目')
    acreage = models.IntegerField(default=0, verbose_name='房屋面积')
    unit = models.CharField(max_length=32, default='', verbose_name='房屋单元')  # 如几室几厅
    capacity = models.IntegerField(default=1, verbose_name='房屋容纳')  # 房屋容纳的人数
    beds = models.CharField(max_length=64, default='', verbose_name='房屋床铺配置')
    deposit = models.IntegerField(default=0, verbose_name='房屋押金')
    min_days = models.IntegerField(default=1, verbose_name='最少入住天数')
    max_days = models.IntegerField(default=0, verbose_name='最大入住天数')  # 0表示不限制
    order_count = models.IntegerField(default=0, verbose_name='预计该房屋的订单数')
    index_image_url = models.CharField(max_length=500, default='', verbose_name='房屋主图片的路径')
    facilities = models.ManyToManyField('Facility')

    class Meta:
        db_table = 'ih_house_info'
        verbose_name = '房屋信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Facility(models.Model):
    '''房屋设施信息'''
    name = models.CharField(max_length=32, verbose_name='设施名称')

    class Meta:
        db_table = 'ih_facility_info'
        verbose_name = '设施信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class HouseImage(BaseModel):
    '''房屋图片'''
    house = models.ForeignKey(House, verbose_name='房屋信息', on_delete=models.CASCADE)
    url = models.CharField(max_length=256, null=False, verbose_name='房屋图片地址')

    class Meta:
        db_table = 'ih_house_image'
        verbose_name = '房屋图片'
        verbose_name_plural = verbose_name

