### my_home
- A renting house information website base on Django

#### Requirements

```bash
pip install -r requirements.txt
```

#### Migrate

```bash
create database home charset=utf8;
python manage.py migrate  
python manage.py makemigrations
```

#### FastDFS

```bash
# 安装客户端包
pip install fdfs_client-py-master.zip
# 修改配置client.conf/dev.py文件fastDFS相关ip为自己fastdfs的ip
```

#### Run

```bash
python manage.py runserver
```

