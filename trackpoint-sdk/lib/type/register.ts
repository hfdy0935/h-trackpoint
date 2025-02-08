import type { IDevice, IOS } from "ua-parser-js";
import { type ExtractData } from "./common";

/**
 * 注册项目的配置
 */
export interface IRegister {
  /**
   * 项目id
   */
  projectId: string;
  /**
   * 项目key
   */
  key: string;
  /**
   * 上传频率，默认1，即全部上传
   */
  uploadPercent?: number;
}

/**
 * 用户&设备基本信息，注册时发给后端
 */
export interface UserBaseInfo {
  uid: string;
  os: ExtractData<IOS>;
  device: ExtractData<IDevice>["type"];
  browser: ExtractData<IOS>; // 字段是一样的，就复用了
  /**
   * 经度
   */
  lng: number;
  /**
   * 纬度
   */
  lat: number;
}

/**
 * 注册请求体
 */
export interface ReqRegister extends Omit<IRegister, "uploadPercent">, UserBaseInfo { }
