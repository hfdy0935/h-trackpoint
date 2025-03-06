
**h-trackpoint**是一个轻量级、使用简单、高性能的**前端埋点监控平台**。支持**不同埋点类型和上报方式**，并提供了丰富的项目、事件、参数管理和数据可视化界面；\
项目地址：https://github.com/hfdy0935/h-trackpoint\
npm地址：https://www.npmjs.com/package/h-trackpoint\
预览地址：Docker上运行后http://localhost:5173


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
    3. 安装依赖，`pip install -r requirements.txt`
    4. 启动，`python main.py`
<br/>

 - 后端端口 `8000`，swagger文档`http://localhost:8000/docs`
 - mysql端口 `3306`
 - redis端口 `6379`
 - minio端口 `9000`


# 2. 前端

```bash
cd trackpoint-frontend
pnpm i
pnpm run dev
```

- sdk单独拿出去每次调试都要在前端更新一次，所以先把sdk的功能移动到前端`/src`中，最后写完再转移打包


# 3. 说明及截图视频
见pdf