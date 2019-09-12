from django import http
from django.core.cache import cache
from django.views import View
from address.models import Area
from home.utils.response_code import RET
import logging
logger = logging.getLogger('django')


class AreasView(View):
    """区域信息"""

    def get(self, request):
        # 先去缓存中取，没有再去数据库中查询
        data = cache.get('index_area')
        if not data:
            # 查出所有的区域信息
            try:
                areas = Area.objects.all()
            except Exception as e:
                logger.error(e)
                return http.JsonResponse({'errno': RET.DBERR, 'errmsg': '数据库查询错误'})
            # 拼接格式
            data = []
            for area in areas:
                data.append({
                    'aid': area.id,
                    'aname': area.name
                })
            # 设置缓存
            cache.set('index_area', data, 3600)
            # 返回
        return http.JsonResponse({'errno': RET.OK, 'errmsg': 'ok', 'data': data})