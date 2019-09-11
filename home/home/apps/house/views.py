import json
# from fdfs_client.client import Fdfs_client
from django import http
from django.conf import settings
from django.core.cache import cache
from django.views import View
from address.models import Area
import logging
from home.utils.common import VerifyRequiredJSONMixin
from home.utils.qiniuyun import qiniuyun
from home.utils.response_code import RET
from house.models import Facility, House, HouseImage

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


class NewHouseView(VerifyRequiredJSONMixin, View):
    """发布新房源"""

    def post(self, request):
        # 获取参数
        json_dict = json.loads(request.body.decode())
        title = json_dict.get('title')
        price = json_dict.get('price')
        area_id = json_dict.get('area_id')
        address = json_dict.get('address')
        room_count = json_dict.get('room_count')
        acreage = json_dict.get('acreage')
        unit = json_dict.get('unit')
        capacity = json_dict.get('capacity')
        beds = json_dict.get('beds')
        deposit = json_dict.get('deposit')
        min_days = json_dict.get('min_days')
        max_days = json_dict.get('max_days')
        facility_ids = json_dict.get('facility')
        # 检验参数
        if not all([title, price, area_id, address, room_count, acreage, unit, capacity,
                    beds, deposit, min_days, max_days, facility_ids]):
            return http.JsonResponse({'errno': RET.PARAMERR, 'errmsg': "参数错误"})
        # 检验房屋单价和押金
        try:
            price = int(price)
            deposit = int(deposit)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'errno': RET.PARAMERR, 'errmsg': "参数错误"})
        # 判断区id是否存在
        try:
            Area.objects.get(id=area_id)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'errno': RET.PARAMERR, 'errmsg': "参数错误"})
        # 保存房屋信息到数据库
        user = request.user
        try:
            house = House.objects.create(
                user=user,
                title=title,
                price=price,
                area_id=area_id,
                address=address,
                room_count=room_count,
                acreage=acreage,
                unit=unit,
                capacity=capacity,
                beds=beds,
                deposit=deposit,
                min_days=min_days,
                max_days=max_days,
            )
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'errno': RET.SERVERERR, 'errmsg': "数据库错误"})

        # 检验房屋设施是否存在
        try:
            Facility.objects.filter(id__in=facility_ids)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'errno': RET.DBERR, 'errmsg': "数据库查询错误"})
        # 保存设施信息
        house.facilities.add(*facility_ids)

        # 返回
        return http.JsonResponse({'errno': RET.OK, 'errmsg': "Ok", 'data': {"house_id": house.id}})


class HouseImageView(VerifyRequiredJSONMixin, View):
    """房屋图片"""

    def post(self, request, house_id):
        # 获取图片
        house_image = request.FILES.get('house_image')
        if not house_image:
            return http.JsonResponse({'error': RET.PARAMERR, 'errmsg': '参数错误'})

        # 查询房屋
        try:
            house = House.objects.get(id=house_id)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'error': RET.PARAMERR, 'errmsg': '房屋不存在'})

        # # 上传到Fdfs
        # try:
        #     client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        #     result = client.upload_by_buffer(house_image.read())
        # except Exception as e:
        #     logger.error(e)
        #     return http.JsonResponse({'errno': RET.THIRDERR, 'errmsg': "上传图片错误"})
        #
        # # 初始化房屋的图片模型
        # # 上传成功：返回file_id,拼接图片访问URL
        # file_id = result.get('Remote file_id')
        # url = settings.FDFS_URL + file_id
        # try:
        #     house_image = HouseImage.objects.create(house=house, url=url)
        # except Exception as e:
        #     logger.error(e)
        #     return http.JsonResponse({'errno': RET.DBERR, 'errmsg': "保存数据失败"})
        #
        # # 判断是否有首页图片
        # if not house.index_image_url:
        #     # 保存图片地址
        #     house.index_image_url = url
        #     house.save()

        # 上传到七牛云
        try:
            content = house_image.read()
            file_name = request.FILES.get('house_image').name
            url = qiniuyun(content, file_name)
            # 保存图片
            HouseImage.objects.create(
                house=house,
                url=url
            )
            # 如果房子主图片没有，将第一张图片设置为房子主图片
            if not house.index_image_url:
                house.index_image_url = url
                house.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'errno': RET.DBERR, 'errmsg': "上传失败"})

        return http.JsonResponse({'errno': RET.OK, 'errmsg': "OK", 'data': {"url": url}})


