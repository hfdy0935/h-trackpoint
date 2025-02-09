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
     * 项目密钥
     */
    projectKey: string;
    /**
     * 上报采样率，取值范围0-1，默认1表示100%上报
     */
    uploadPercent?: number;
    /**
     * 失败重试次数
     */
    maxRetries?: number;
    /**
     * 批量上报大小
     */
    batchSize?: number;
    /**
     * 定时上报间隔(ms)
     */
    flushInterval?: number;
    /**
     * 重试间隔(ms)
     */
    retryInterval?: number;
}
/**
 * 用户&设备基本信息，注册时发给后端
 */
export interface UserBaseInfo {
    uid: string;
    os: ExtractData<IOS>;
    device: ExtractData<IDevice>["type"];
    browser: ExtractData<IOS>;
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
export interface ReqRegister extends Omit<IRegister, "uploadPercent" | "maxRetries" | "batchSize" | "flushInterval" | "retryInterval">, UserBaseInfo {
}
