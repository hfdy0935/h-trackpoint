import type { IRegister, UserBaseInfo } from "../type/register";
import { reqRegister } from "./http";
import type { ICommonParams } from "../type/common";
import { registerAutoSendEvents } from "./autosend";

export class ProjectInstanceImpl {
  static #instance: ProjectInstanceImpl;
  #options: IRegister;
  #userBaseInfo: UserBaseInfo;
  #commonParams: ICommonParams;

  private constructor(options: IRegister, info: UserBaseInfo) {
    this.#options = options;
    this.#userBaseInfo = info;
    // 重新注册时清空之前的参数
    this.#commonParams = {};
  }

  /**
   * 如果未创建实例就创建
   * @param options 注册的配置
   * @param info 用户基本信息
   */
  static async create(options: IRegister, info: UserBaseInfo) {
    const denl = await reqRegister(options, info);
    ProjectInstanceImpl.#instance = new this(options, info);
    registerAutoSendEvents(denl.data.data!);
    // 还是改成每次注册都发送请求，防治注册不同项目但还是旧的项目.
    // if (!ProjectInstanceImpl.#instance) {
    //   const denl = await reqRegister(options, info);
    //   ProjectInstanceImpl.#instance = new this(options, info);
    //   registerAutoSendEvents(denl.data.data!);
    // }
  }

  static get instance(): ProjectInstanceImpl {
    if (!ProjectInstanceImpl.#instance) {
      throw new Error("项目还未初始化");
    }
    return ProjectInstanceImpl.#instance;
  }

  addCommonParams(params: ICommonParams) {
    Object.assign(this.#commonParams, params);
  }

  get commonParams() {
    return this.#commonParams;
  }
  get options() {
    return this.#options;
  }
  get userBaseInfo() {
    return this.#userBaseInfo;
  }
}

/**
 * 获取项目实例
 * @returns
 */
export function getInstance(): ProjectInstanceImpl {
  return ProjectInstanceImpl.instance;
}
