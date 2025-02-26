# Trackpoint SDK

一个轻量级、高性能的前端埋点SDK，支持自动化埋点、自定义事件上报、性能监控等功能。

## 特性

- 🚀 高性能：批量处理，异步上报
- 💪 高可靠：失败重试，队列管理
- 🔄 自动化：支持自动埋点（性能指标、JS错误等）
- 🎯 精确性：支持自定义事件和参数
- 📊 可扩展：支持截图上传等扩展功能

## 安装

```bash
npm install trackpoint-sdk
# 或
yarn add trackpoint-sdk
```

## 快速开始

### 1. 初始化

```typescript
import { register } from 'trackpoint-sdk';

await register({
  projectId: 'your-project-id',
  projectKey: 'your-project-key',
  uploadPercent: 1, // 上报采样率，0-1，1表示100%上报
});
```

### 2. 事件上报

```typescript
import { sendEvent } from 'trackpoint-sdk';

// 上报自定义事件
await sendEvent('button_click', {
  buttonId: 'submit-btn',
  buttonText: '提交',
});
```

### 3. 添加通用参数

```typescript
import { addCommonParams } from 'trackpoint-sdk';

// 添加在所有事件中都会携带的通用参数
addCommonParams({
  userId: '12345',
  userType: 'vip',
});
```

## API 文档

### register(options: IRegister): Promise<void>

初始化SDK，必须在使用其他API前调用。

参数：
- `options.projectId`: string - 项目ID
- `options.projectKey`: string - 项目密钥
- `options.uploadPercent`: number - 上报采样率，取值范围0-1，1表示100%上报

```typescript
await register({
  projectId: 'your-project-id',
  projectKey: 'your-project-key',
  uploadPercent: 1, // 100%上报
});
```

### sendEvent<T>(eventName: string, params: T): void

上报自定义事件。

参数：
- `eventName`: string - 事件名称
- `params`: T - 事件参数，泛型类型继承自ICommonParams

```typescript
await sendEvent('page_view', {
  pageId: 'home',
  duration: 30000,
});
```

### addCommonParams<T>(params: T): void

添加通用参数，将在每个事件中携带。

参数：
- `params`: T - 通用参数对象，泛型类型继承自ICommonParams

```typescript
addCommonParams({
  platform: 'web',
  version: '1.0.0',
});
```

## 高级配置

SDK支持通过配置优化上报性能和可靠性：

```typescript
import { register } from 'trackpoint-sdk';

await register({
  projectId: 'your-project-id',
  projectKey: 'your-project-key',
  uploadPercent: 1, // 100%上报
  // 高级配置
  maxRetries: 3,        // 失败重试次数
  batchSize: 10,        // 批量上报大小
  flushInterval: 5000,  // 定时上报间隔(ms)
  retryInterval: 3000,  // 重试间隔(ms)
});
```

### 配置项说明

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| uploadPercent | number | 1 | 上报采样率，取值范围0-1，1表示100%上报 |
| maxRetries | number | 3 | 事件上报失败后的最大重试次数 |
| batchSize | number | 10 | 批量上报时单次发送的最大事件数 |
| flushInterval | number | 5000 | 定时上报的时间间隔（毫秒） |
| retryInterval | number | 3000 | 重试等待时间（毫秒） |

## 自动化埋点

SDK内置了一些自动埋点能力：

### 性能监控

自动收集页面性能指标：
- DNS解析时间
- TCP连接时间
- 请求响应时间
- DOM处理时间
- 资源加载时间
- JS内存使用情况

### 错误监控

自动捕获并上报：
- JS运行时错误
- Promise未捕获异常
- 资源加载错误

## 注意事项

1. 必须先调用`register`初始化SDK
2. 事件队列会在页面关闭时自动处理未发送的事件
3. 批量上报可能会导致事件延迟上报，如需实时性，可以调整`flushInterval`
4. 建议根据实际情况调整`batchSize`和`flushInterval`以平衡性能和实时性

## 类型定义

完整的类型定义请参考：
- `types/type/event.d.ts`
- `types/type/register.d.ts`
- `types/impl/queue.d.ts`

## License

MIT