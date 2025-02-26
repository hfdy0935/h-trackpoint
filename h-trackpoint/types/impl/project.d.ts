import type { IRegister, UserBaseInfo } from "../type/register";
import type { ICommonParams } from "../type/common";
export declare class ProjectInstanceImpl {
    #private;
    private constructor();
    /**
     * 如果未创建实例就创建
     * @param options 注册的配置
     * @param info 用户基本信息
     */
    static create(options: IRegister, info: UserBaseInfo): Promise<void>;
    static get instance(): ProjectInstanceImpl;
    addCommonParams(params: ICommonParams): void;
    get commonParams(): ICommonParams;
    get options(): IRegister;
    get userBaseInfo(): UserBaseInfo;
}
/**
 * 获取项目实例
 * @returns
 */
export declare function getInstance(): ProjectInstanceImpl;
