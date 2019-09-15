import json
from datetime import datetime
from django import http
from django.views import View


import logging

from home.utils.common import LoginRequiredJSONMixin
from home.utils.response_code import RET
from house.models import House
from order.models import Order

logger = logging.getLogger('django')


class AddOrderView(LoginRequiredJSONMixin, View):

    def post(self, request):
        """添加订单"""
        # 获取参数
        json_dict = json.loads(request.body.decode())
        house_id = json_dict.get('house_id')
        start_date = json_dict.get('start_date')
        end_date = json_dict.get('end_date')
        # 检验参数
        if not all([house_id, start_date, end_date]):
            return http.JsonResponse({'errmsg': '参数错误', 'errno': RET.PARAMERR})
        # 检验house_id
        try:
            house = House.objects.get(id=house_id)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'errmsg': '参数错误', 'errno': RET.PARAMERR})
        # 时间检验
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            # 假设大于，不满足报错
            assert end_date >= start_date
            # 计算天数
            days = (end_date - start_date).days
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'errno': RET.PARAMERR, 'errmsg': "日期参数错误"})
        # 判断房东预订的房屋是不是自己的发布的房屋
        user = request.user
        if user.id == house.user_id:
            return http.JsonResponse({'errno': RET.ROLEERR, 'errmsg': "不能预定自己的房子"})
        # 检查用户预订的时间内，房屋没有被别人下单
        try:
            count = Order.objects.filter(house_id=house_id, begin_date__lte=end_date,
                                         end_date__gte=start_date).count()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'errno': RET.DBERR, 'errmsg': '系统繁忙，请稍候重试'})
        # count大于0表示，在该时间段该房子已被其他人预定
        if count > 0:
            return http.JsonResponse({'errno': RET.DATAERR, 'errmsg': '房屋已被预订'})

        # 添加订单
        try:
            order = Order.objects.create(
                user=request.user,
                house=house,
                begin_date=start_date,
                end_date=end_date,
                days=days,
                house_price=house.price,
                amount=house.price * days,
                status='WAIT_ACCEPT'
            )
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'errno': RET.DBERR, 'errmsg': "创建订单失败"})

        # 返回
        return http.JsonResponse({'errno': RET.OK, 'errmsg': "ok", 'data': {'order_id': order.id}})

    def get(self, request):
        """我的订单"""
        # 获取参数
        role = request.GET.get('role')
        # 获取用户
        user = request.user
        # 判断用户是客户还是房东
        try:
            if role == "landlord":
                # 房东
                # 以房东的身份在数据库中查询自己发布过的房屋
                houses = House.objects.filter(user=user)

                # 通过列表生成式方式保存房东名下的所有房屋的id
                houses_ids = [house.id for house in houses]
                # 在Order表中查询预定了自己房子的订单,并按照创建订单的时间的倒序排序，也就是在此页面显示最新的订单信息
                orders = Order.objects.filter(house_id__in=houses_ids).order_by('-create_time').all()

            else:
                # 以房客的身份查询订单，则查询的是我的订单
                orders = Order.objects.filter(user_id=user.id).order_by('-create_time').all()

        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'errno': RET.DBERR, 'errmsg': "数据库错误"})
        # 整理格式
        orders_list = []
        for order in orders:
            orders_list.append({
                'amount': order.amount,
                'ctime': order.create_time.strftime('%Y-%m-%d'),
                'days': order.days,
                'end_date': order.end_date.strftime('%Y-%m-%d'),
                'img_url': order.house.index_image_url,
                'order_id': order.id,
                'start_date': order.begin_date.strftime('%Y-%m-%d'),
                'status': order.status,
                'title': order.house.title,
                'comment': order.comment if order.comment else ''
            })
        return http.JsonResponse({'data': {'orders': orders_list}, 'errmsg': 'ok', 'errno': RET.OK})

    def put(self, request):
        """接单或拒单"""
        # 获取用户
        user = request.user
        # 接收参数
        json_dict = json.loads(request.body.decode())
        action = json_dict.get("action")
        order_id = json_dict.get("order_id")
        # 检验参数
        if action not in ("accept", "reject"):
            return http.JsonResponse({'errno': RET.PARAMERR, 'errmsg': "参数错误"})
        # 在数据库中根据订单号查询订单状态为等待接单状态的订单
        try:
            order = Order.objects.get(id=order_id, status='WAIT_ACCEPT')

            # 获取order订单对象中的house对象
            house = order.house
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'errno': RET.DBERR, 'errmsg': "数据库查询错误"})

        # 如果order对象不存在或者订单中的房屋id不等于用户id 则说明房东在修改不属于自己房屋订单
        if not order or house.user_id != user.id:
            return http.JsonResponse({'errno': RET.REQERR, 'errmsg': "非法请求或请求次数受限"})

        # 房东选择接单，则对应订单状态为待支付，拒单则需房东填写拒单的原因
        if action == "accept":  # 接单
            order.status = 'WAIT_COMMENT'
        elif action == "reject":  # 拒单
            # 填写拒单理由
            reason = json_dict.get('reason')
            # 修改订单状态
            order.status = 'REJECTED'
            order.comment = reason

        # 将订单修改后的对象提交到数据库
        order.save()

        # 返回响应
        return http.JsonResponse({'errno': RET.OK, 'errmsg': 'ok'})


class OrderComment(LoginRequiredJSONMixin, View):
    """评论订单"""
    def put(self, request):
        # 获取参数
        json_dict = json.loads(request.body.decode())
        comment = json_dict.get('comment')
        order_id = json_dict.get('order_id')
        # 检验参数
        if not all([comment, order_id]):
            return http.JsonResponse({'errno': RET.PARAMERR, 'errmsg': "参数错误"})
        # order_id检验
        try:
            order = Order.objects.get(id=order_id)
            house = order.house
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'errno': RET.PARAMERR, 'errmsg': "order_id参数错误"})
        # 修改订单评价和订单状态
        try:
            order.comment = comment
            order.status = 'COMPLETE'
            # 修改房源的销量
            house.order_count += 1
            order.save()
            house.save()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'errno': RET.DBERR, 'errmsg': "评论失败"})
        # 返回
        return http.JsonResponse({'errno': RET.OK, 'errmsg': "ok"})



