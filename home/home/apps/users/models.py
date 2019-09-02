from django.db import models
from django.contrib.auth.models import AbstractUser


# 我们重写用户模型类, 继承自 AbstractUser
class User(AbstractUser):
    """自定义用户模型类"""

    # 在用户模型类中增加 mobile 字段
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    real_name = models.CharField(max_length=32, verbose_name='真实姓名', null=True)
    id_card = models.CharField(max_length=18, verbose_name='身份证号', null=True)
    avatar_url = models.CharField(max_length=300, verbose_name='用户头像路径', null=True)

    # 对当前表进行相关设置:
    class Meta:
        db_table = 'ih_user_profile'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    # 在 str 魔法方法中, 返回用户名称
    def __str__(self):
        return self.username
