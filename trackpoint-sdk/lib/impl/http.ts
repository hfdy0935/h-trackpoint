import type { ARB } from "../type/common";
import type {  BatchSendEventsRequest, RespSendEvent } from "../type/event";
import type { IRegister, ReqRegister, UserBaseInfo } from "../type/register";
import html2canvas from "html2canvas";
import { request } from "../util/request";
import { DefaultEventNameEnum } from "../enum";

/**
 * 注册项目
 * @param options 项目配置
 * @param baseInfo 用户基本信息
 * @returns Promise
 */
export async function reqRegister(options: IRegister, baseInfo: UserBaseInfo): Promise<ARB<DefaultEventNameEnum[]>> {
  const data: ReqRegister = {
    projectId: options.projectId,
    projectKey: options.projectKey,
    uid: baseInfo.uid,
    os: baseInfo.os,
    device: baseInfo.device,
    browser: baseInfo.browser
  };
  return await request.post<DefaultEventNameEnum[], ARB<DefaultEventNameEnum[]>, ReqRegister>("/register", data);
}

/**
 * 批量上报事件
 * @param data 事件数据，包含用户ID、项目ID和事件数组
 */
export async function reqSendEvents(data: BatchSendEventsRequest): Promise<ARB<RespSendEvent[]>> {
  try {
    const resp = await request.post<RespSendEvent[], ARB<RespSendEvent[]>, BatchSendEventsRequest>("/send-events", data);
    
    if (resp.data.code === 200 && resp.data.data) {
      // 处理需要上传截图的事件
      for (const result of resp.data.data) {
        if (result.need_upload_shot) {
          await reqSendScreenshot(result.record_id);
        }
      }
    }
    return resp;
  } catch (e) {
    return Promise.reject(e);
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
        await request.post<null, ARB<null>, FormData>("/upload-shot", formData);
      }
    });
  });
}
