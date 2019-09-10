from urllib.parse import urlencode
from django.shortcuts import redirect


def get_html_file(request, file_name):
    # 判断是否为网站logo，不是拼接前缀
    if file_name != 'favicon.ico':
        file_name = '/static/html/' + file_name

    # 如果有查询字符串拼接到url
    params = request.GET
    if params:
        result = urlencode(params)
        return redirect(file_name + '?{}'.format(result))
    # 重定向
    return redirect(file_name)


def index(request):
    """重定向到首页"""
    return redirect('/static/html/index.html')
