const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const { v4: uuidv4 } = require('uuid');

const app = express();
const port = 8000;

// CORS配置，允许跨域请求携带cookie
app.use(cors({
  origin: 'http://localhost:5173', // 替换为你的前端开发服务器地址
  credentials: true,
  methods: ['GET', 'POST', 'DELETE'],
  allowedHeaders: ['Content-Type']
}));

app.use(cookieParser());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// 模拟数据存储
const events = [];
const clients = new Map(); // 使用Map存储，key为uid

// 路由前缀
const prefix = '/v1/client';

// 验证客户端中间件
const validateClient = (req, res, next) => {
  const uid = req.cookies['h-trackpoint-uid'];
  if (!uid || !clients.has(uid)) {
    return res.status(401).json({
      code: 401,
      msg: '未注册或无效的客户端',
      data: null
    });
  }
  req.clientInfo = clients.get(uid);
  next();
};

// 注册客户端
app.post(`${prefix}/register`, (req, res) => {
  const clientInfo = req.body;
  console.log('\n[注册客户端] 收到数据:', JSON.stringify(clientInfo, null, 2));

  // 验证必要的字段
  if (!clientInfo.projectId || !clientInfo.projectKey) {
    return res.status(400).json({
      code: 400,
      msg: '缺少必要的项目信息',
      data: null
    });
  }

  const client = {
    ...clientInfo,
    registerTime: new Date().toISOString()
  };

  // 存储客户端信息
  clients.set(clientInfo.uid, client);

  // 设置cookie，注意配置
  res.cookie('h-trackpoint-uid', clientInfo.uid, {
    maxAge: 365 * 24 * 60 * 60 * 1000, // 一年有效期
    httpOnly: true,
    sameSite: 'lax', // 改为lax以支持跨站请求
    secure: false, // 本地开发时设为false
    path: '/'
  });
  
  // 返回支持的默认事件列表
  res.json({
    code: 200,
    msg: 'success',
    data: ['performance', 'js_error', 'click', 'page_stay_duration', 'request']
  });
});

// 批量上报事件
app.post(`${prefix}/send-events`, validateClient, (req, res) => {
  const { events: batchEvents } = req.body;
  console.log('\n[批量事件上报] 收到事件数量:', batchEvents.length);
  
  const results = batchEvents.map(eventData => {
    const recordId = uuidv4();
    const event = {
      ...eventData,
      uid: req.clientInfo.uid,
      projectId: req.clientInfo.projectId,
      record_id: recordId,
      serverTime: new Date().toISOString()
    };
    events.push(event);
    console.log(`[事件上报] record_id: ${recordId}, eventName: ${eventData.eventName}`);

    // 随机决定是否需要上传截图
    const needUploadShot = Math.random() > 0.7;
    return {
      record_id: recordId,
      need_upload_shot: needUploadShot
    };
  });

  res.json({
    code: 200,
    msg: 'success',
    data: results
  });
});

// 上传截图
app.post(`${prefix}/upload-shot`, validateClient, (req, res) => {
  const recordId = req.body.record_id;
  console.log('\n[截图上传] 收到截图，record_id:', recordId);
  
  // 验证record_id是否属于当前客户端
  const event = events.find(e => e.record_id === recordId && e.uid === req.clientInfo.uid);
  if (!event) {
    return res.status(403).json({
      code: 403,
      msg: '无效的记录ID',
      data: null
    });
  }

  res.json({
    code: 200,
    msg: 'success',
    data: null
  });
});

// 查看所有已收集的事件（仅用于测试）
app.get(`${prefix}/events`, (req, res) => {
  const uid = req.query.uid;
  let filteredEvents = events;
  
  if (uid) {
    filteredEvents = events.filter(e => e.uid === uid);
    console.log('\n[查询事件] 客户端:', uid, '事件数:', filteredEvents.length);
  } else {
    console.log('\n[查询事件] 所有事件数:', events.length);
  }
  
  res.json({
    code: 200,
    msg: 'success',
    data: filteredEvents
  });
});

// 查看所有注册的客户端（仅用于测试）
app.get(`${prefix}/clients`, (req, res) => {
  console.log('\n[查询客户端] 当前注册的客户端数:', clients.size);
  
  res.json({
    code: 200,
    msg: 'success',
    data: Array.from(clients.values())
  });
});

// 清空所有数据（仅用于测试）
app.delete(`${prefix}/clear`, (req, res) => {
  console.log('\n[清空数据] 清空前 - 事件数:', events.length, '客户端数:', clients.size);
  
  events.length = 0;
  clients.clear();
  
  console.log('[清空数据] 清空后 - 事件数:', events.length, '客户端数:', clients.size);
  
  res.json({
    code: 200,
    msg: 'success'
  });
});

app.listen(port, () => {
  console.log(`测试服务器运行在 http://localhost:${port}`);
  console.log(`
可用接口：
POST ${prefix}/register     - 注册客户端
POST ${prefix}/send-events - 批量上报事件
POST ${prefix}/upload-shot  - 上传截图
GET  ${prefix}/events      - 查看所有事件（支持uid过滤）
GET  ${prefix}/clients     - 查看所有客户端
DEL  ${prefix}/clear       - 清空所有数据
  `);
}); 