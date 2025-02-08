import type { AxiosResponse } from "axios";

export interface BaseResp<T = null> {
  code: number;
  msg: string;
  data?: T;
}

/**
 * 排除方法，只留数据
 */
export type ExtractData<T extends {}> = {
  [K in keyof T as T[K] extends Function ? never : K]: T[K] extends {} ? ExtractData<T[K]> : T[K];
};

/**
 * 通用参数
 */
export interface ICommonParams {
  [k: string]: any;
}

/**
 * 从I1中排除I2
 */
export type ExcludeInterface<I1 extends {}, I2 extends {}> = {
  [K in keyof I1 as K extends keyof I2 ? never : K]: I1[K];
};

/**
 * axios响应
 */
export type ARB<T> = AxiosResponse<BaseResp<T>>
