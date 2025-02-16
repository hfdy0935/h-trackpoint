import axios from 'axios'
import type { AxiosRequestConfig } from 'axios'

const instance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    timeout: 10000
})

export const request = {
    get<T>(url: string, config?: AxiosRequestConfig) {
        return instance.get<T>(url, config)
    },
    post<T>(url: string, data?: any, config?: AxiosRequestConfig) {
        return instance.post<T>(url, data, config)
    },
    put<T>(url: string, data?: any, config?: AxiosRequestConfig) {
        return instance.put<T>(url, data, config)
    },
    delete<T>(url: string, config?: AxiosRequestConfig) {
        return instance.delete<T>(url, config)
    }
}
