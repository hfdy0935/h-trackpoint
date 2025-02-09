import { type IRegister } from "./type/register";

/**
 * 后端url
 */
export const BASE_URL = "http://localhost:8000/v1/client/";
/**
 * 用户uid在localStorage中存储的key
 */
export const UID_LOCALSTORAGE_FIELD = "h-trackpoint-uid";
/**
 * 默认注册配置
 */
export const DEFAULT_REGISTER_CONFIG: IRegister = {
  projectId: "",
  projectKey: "",
  uploadPercent: 1,
  maxRetries: 3,
  batchSize: 10,
  flushInterval: 5000,
  retryInterval: 3000,
};
