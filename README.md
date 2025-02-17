# 1. 后端

1. 项目配置：
    - docker环境：`trackpoint-backend/resources/config.docker.yml`
    - 本地环境：`trackpoint-backend/resources/config.yml`
    - 如果要配置发送邮件，需要开一个SMTP服务，修改对应的用户名和密码

2. mysql: `trackpoint-backend/resources/init.sql`，有一个默认用户：
    - 邮箱 email@qq.com（编的，只能用于登录）
    - 密码 aaa1234
    - 不是管理员（目前管理员功能还没写）

3. 启动

- docker
```bash
cd trackpoint-backend
docker compose up -d
# `-d`表示后台执行，不输出日志
```

- 手动
    1. 下载、启动mysql、redis、minio
    2. 修改`trackpoint_backend/bean/config.py`中的`_cfg`函数中读取配置文件为`trackpoint_backend/resources/config.yml`
    3. 安装依赖，`pip install -r requirements.txt`
    4. 启动，`python main.py`
<br/>

 - 后端端口 `8000`，swagger文档`http://localhost:8000/docs`
 - mysql端口 `3306`
 - redis端口 `6379`
 - minio端口 `9000`


**ps：如果后端启动失败就等mysql、redis、minio启动之后手动再启动一次**
![alt text](README-image/image-26.png)
![alt text](README-image/image-27.png)
日志正常输出（如果没加`-d`的话）
![alt text](README-image/image-29.png)


# 2. 前端

```bash
cd trackpoint-frontend
pnpm i
pnpm run dev
```

- sdk单独拿出去每次调试都要在前端更新一次，所以先把sdk的功能移动到前端`/src`中，最后写完再转移打包


# 3. 截图

~~TODO: 下面的图，从mysql获取的中文是乱码，后面再修~~  
- 之前截的中文乱码，后面的正常；
- :white_check_mark: 已解决，`init/sql`前面加上`/*!40101 SET NAMES utf8 */;`

## 1. 主页、登录注册找回密码
![alt text](README-image/image.png)
![alt text](README-image/image-1.png)
......

# 2. 首页
![alt text](README-image/image-2.png)
![alt text](README-image/image-30.png)
个人信息：
![alt text](README-image/image-31.png)
修改密码：
![alt text](README-image/image-32.png)

# 3. 可视化
![alt text](README-image/image-3.png)
![alt text](README-image/image-4.png)


# 4. 项目管理

- 项目列表，可排序筛选
![alt text](README-image/image-5.png)
- 创建项目
![alt text](README-image/image-6.png)
![alt text](README-image/image-7.png)
- 修改项目
![alt text](README-image/image-8.png)
- 其他操作
![alt text](README-image/image-9.png)


# 5. 事件管理

- 默认事件，可排序筛选
![alt text](README-image/image-10.png)
- 自定义事件，可排序筛选
![alt text](README-image/image-11.png)
- 创建自定义事件（可以添加到之前创建的项目中）
![alt text](README-image/image-12.png)
- 修改自定义事件（可以修改所在的项目）
![alt text](README-image/image-13.png)
添加之后，项目列表信息也变了
![alt text](README-image/image-15.png)
- 其他操作
![alt text](README-image/image-14.png)
- 停用事件之后，项目那会变成
![alt text](README-image/image-16.png)
- 停用项目同理
![alt text](README-image/image-25.png)

- 测试

简单的sdk测试
![alt text](README-image/image-17.png)
1. 用之前创建项目时的id和key注册
![alt text](README-image/image-18.png)
1. 成功后**自动**发了一次性能事件
![alt text](README-image/image-19.png)
1. **手动**上报点击事件
![alt text](README-image/image-20.png)
后端判断是否需要截图，需要的话上传截图，用于做点击热力图
![alt text](README-image/image-21.png)
minio可查![alt text](README-image/image-22.png)
1. js错误**自动/手动**上报
![alt text](README-image/image-23.png)
1. 网络请求**手动**上报
![alt text](README-image/image-24.png)
