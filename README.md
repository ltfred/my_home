### my_home
- A renting house information website base on Django

#### 安装依赖包

```bash
pip install -r requirements.txt
```

#### 创建数据库/迁移数据

```bash
create database home charset=utf8;
python manage.py migrate  
python manage.py makemigrations
# 导入测试数据在test_data文件
```

#### 图片存储FastDFS

```bash
# 安装客户端包
pip install fdfs_client-py-master.zip
# 修改配置client.conf/dev.py文件fastDFS相关ip为自己fastdfs的ip
```

#### 运行项目

```bash
python manage.py runserver
```