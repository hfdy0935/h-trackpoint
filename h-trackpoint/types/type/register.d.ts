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
    /**
     * 前端生成的uid
     */
    uid: string;
    /**
     * 操作系统信息
     */
    os: ExtractData<IOS>;
    /**
     * 设备类型，可为空
     */
    device: ExtractData<IDevice>["type"] | null;
    /**
     * 浏览器信息
     */
    browser: {
        name: string;
        version: string;
    };
}
/**
 * 注册请求体
 */
export interface ReqRegister {
    /**
     * 项目id
     */
    projectId: string;
    /**
     * 项目key
     */
    projectKey: string;
    /**
     * 前端生成的uid
     */
    uid: string;
    /**
     * 操作系统信息
     */
    os: ExtractData<IOS>;
    /**
     * 设备类型，可为空
     */
    device: ExtractData<IDevice>["type"] | null;
    /**
     * 浏览器信息
     */
    browser: {
        name: string;
        version: string;
    };
}
