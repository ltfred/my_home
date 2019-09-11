# -*- coding: utf-8 -*-
# flake8: noqa
import random

from qiniu import Auth, put_file, etag, put_data
import qiniu.config


def qiniuyun(content, name):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = '54fSiNOKjQcwLwOKvXipXBcB3YSEbew_74uHxJVo'
    secret_key = 'ukpNkvfteq2O92rm8P0qtsauESxSYh_mmN9PLE29'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'ihome_123456'
    # 上传后保存的文件名
    pro = '%06d' % random.randint(0, 999)
    key = pro + name
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径
    # localfile = './房屋1.jpg'
    ret, info = put_data(token, key, content)
    print(info)
    # assert ret['key'] == key
    # assert ret['hash'] == etag(content)

    url = 'http://pu0inobnm.bkt.clouddn.com/' + key
    print(url)
    return url


# with open('煤老板.png', 'rb')as f:
#     content = f.read()
#     qiniuyun(content, 'lolo.png')

