import { BASE_URL } from '../constants'
import axios from 'axios'

export const request = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
})

/**
 * 获取当前时间戳，用于上报
 * @returns
 */
export function getCurrentTime(): number {
  return Date.now()
}
