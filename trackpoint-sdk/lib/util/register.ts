import { type IData, UAParser } from "ua-parser-js";
import type { UserBaseInfo } from "../type/register";
import type { ExtractData } from "../type/common";
import { UID_LOCALSTORAGE_FIELD } from "../constants";

interface IItem<T> extends IData<T> {
  [k: string]: any;
}
/**
 * 删除方法
 * @param obj
 */
function extractData<T, V extends {} = IItem<T>>(obj: V): ExtractData<V> {
  for (const [k, v] of Object.entries(obj)) {
    if (typeof v === "function") {
      delete obj[k as keyof V];
    }
  }
  return obj;
}

/**
 * 先读取，如果没有，生成用户唯一uid，并存到localStorage
 */
function getUserUid(): string {
  const uid = localStorage.getItem(UID_LOCALSTORAGE_FIELD);
  if (uid) return uid;
  const newUid = crypto.randomUUID();
  localStorage.setItem(UID_LOCALSTORAGE_FIELD, newUid);
  return newUid;
}

/**
 * 初始化时获取用户基本信息
 */
export async function getUserBaseInfo(): Promise<UserBaseInfo> {
  const parser = new UAParser();
  const browser = extractData(parser.getBrowser());

  return {
    uid: getUserUid(),
    os: extractData(parser.getOS()),
    device: parser.getDevice().type || null,
    browser: {
      name: browser.name || 'unknown',
      version: browser.version || '0',
    }
  };
}
