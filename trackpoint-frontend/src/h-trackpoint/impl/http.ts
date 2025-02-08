import type { ARB, BaseResp } from "../type/common";
import type { ISendEventParams, ReqSendEvent, RespSendEvent } from "../type/event";
import type { IRegister, ReqRegister, UserBaseInfo } from "../type/register";
import { getInstance } from "./project";
import html2canvas from "html2canvas";
import { getCurrentTime, request } from "../util/request";
import { DefaultEventNameEnum } from "../enum";

/**
 * 注册项目
 * @param options 项目id、key、上传频率（暂时没用到）
 * @param props 用户传的配置，注册成功、失败、报错时的回调函数
 * @param baseInfo 用户基本信息，用于注册客户端
 * @returns Promise
 */
export async function reqRegister(options: IRegister, baseInfo: UserBaseInfo): Promise<ARB<DefaultEventNameEnum[]>> {
  const { uploadPercent, ...rest } = options;
  const data: ReqRegister = {
    ...rest,
    ...baseInfo,
  };
  return await request.post<DefaultEventNameEnum[], ARB<DefaultEventNameEnum[]>, ReqRegister>("/register", data)
}

/**
 * 上报事件
 * @param props 事件名和参数
 */
export async function reqSendEvent(props: ISendEventParams): Promise<ARB<RespSendEvent>> {
  const { eventName, params } = props;
  const {
    commonParams,
    userBaseInfo: { uid },
    options: { uploadPercent, ...rest },
  } = getInstance();
  const data: ReqSendEvent = { uid, ...rest, eventName, params: { ...params, ...commonParams }, pageUrl: window.location.href, createTime: getCurrentTime() };
  try {
    // commonParams和params合并
    const resp = await request.post<RespSendEvent, ARB<RespSendEvent>, ReqSendEvent>("/send-event", data);
    if (resp.data.code === 200) {
      if (resp.data.data?.need_upload_shot) {
        await reqSendScreenshot(resp.data.data.record_id);
      }
    }
    return Promise.resolve(resp)
  } catch (e) {
    return Promise.reject(e)
  }
}

/**
 * 上传截图
 * @param rid 之前上报事件的记录id
 */
export async function reqSendScreenshot(rid: string) {
  html2canvas(document.documentElement).then((canvas) => {
    canvas.toBlob(async (b) => {
      if (b) {
        const formData = new FormData();
        formData.append("screenshot", b, "screenshot.png");
        formData.append("record_id", rid);
        console.log(formData);
        await request.post<null, ARB<null>, FormData>("/upload-shot", formData);
      }
    });
  });
}
