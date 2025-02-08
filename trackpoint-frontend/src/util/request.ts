import { message } from 'ant-design-vue';
import { useUserStore } from "@/store";
import axios from "axios";
import { storeToRefs } from "pinia";
import { goToPublicPage } from "./goto";

export const request = axios.create({
    baseURL: import.meta.env.VITE_REQ_BASE_URL,
    timeout: 5000
})



request.interceptors.request.use(config => {
    const { token } = storeToRefs(useUserStore())
    config.headers.Authorization = token.value;
    return config;
}, error => {
    return Promise.reject(error);
});

request.interceptors.response.use(response => {
    // if (response.data.code === 401) {
    //     message.error('登录已过期，请重新登录')
    //     goToPublicPage()
    // }
    return response.data;
}, error => {
    return Promise.reject(error);
});