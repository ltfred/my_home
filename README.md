### my_home
- A renting house information website base on Django

#### requirements

```bash
pip install -r requirements.txt
```

### create database

```
create database home charset=utf8;
```

#### migrate

```bash
python manage.py makemigrations
python manage.py migrate  
```

#### FastDFS

```bash
# 安装客户端包
pip install fdfs_client-py-master.zip
# 修改配置client.conf/dev.py文件fastDFS相关ip为自己fastdfs的ip
```

#### run

```bash
python manage.py runserver
```

