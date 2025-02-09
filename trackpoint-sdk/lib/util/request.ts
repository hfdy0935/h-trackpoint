import { BASE_URL } from "../constants";
import axios from "axios";

export const request = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
});
// request.interceptors.response.use(
//   (response) => {
//     return response.data;
//   },
//   (error) => {
//     return Promise.reject(error);
//   }
// );


/**
 * 获取当前时间戳，用于上报
 * @returns
 */
export function getCurrentTime(): number {
  return Date.now();
}
