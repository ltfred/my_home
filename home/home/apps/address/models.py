from django.db import models


class Area(models.Model):
    name = models.CharField(max_length=32, null=False, verbose_name='区域名称')

    class Meta:
        db_table = 'ih_area_info'
        verbose_name = '地区'
        verbose_name_plural = verbose_name
