<template>
    <a-tag class="tag">网络请求</a-tag><h-tag manual></h-tag>，点<a-button @click="doReq" type="primary" class="btn"
        size="small">我</a-button>发送一个请求，随机1-3秒返回，成功失败随机，可以在network查看结果是否上报
    <a-tooltip title="事件参数">
        <InfoCircleOutlined @click="$emit('open', dataSource)" />
    </a-tooltip>
</template>

<script setup lang="ts">
import { sendEvent } from 'h-trackpoint'
import { InfoCircleOutlined } from '@ant-design/icons-vue';
import HTag from './h-tag.vue';
import type { AxiosResponse } from 'axios';
import axios from 'axios';
import type { BaseResp } from '@/type/base';
import type { TableDataItem } from './data';

defineEmits<{
    open: [data: TableDataItem[]]
}>()

interface HTTPRequestSendBody {
    request_url: string
    status_code: number
    request_method: string
    time_duration: number
}
const doReq = async () => {
    const start = performance.now()
    const url = `http://localhost:8000/v1/test/random-result`
    try {
        const resp = await axios<null, AxiosResponse<BaseResp<null>>>({
            url,
            method: 'POST',
        })
        if (resp.data.code === 200) {
            // 成功的业务逻辑
        }
        await sendEvent<HTTPRequestSendBody>('request', {
            request_url: resp.config.url ?? url,
            status_code: resp.status,
            request_method: 'POST',
            time_duration: +(performance.now() - start).toFixed(2)
        })
    } catch (e: any) {
        await sendEvent<HTTPRequestSendBody>('request', {
            request_url: url,
            status_code: e.status,
            request_method: 'POST',
            time_duration: +(performance.now() - start).toFixed(2)
        })
    }
}

const dataSource: TableDataItem[] = [
    {
        name: 'status_code',
        type: 'number',
        desc: '请求状态码'
    },
    {
        name: 'request_method',
        type: 'string',
        desc: '请求方法'
    },
    {
        name: 'request_url',
        type: 'string',
        desc: '请求url'
    },
    {
        name: 'time_duration',
        type: 'number',
        desc: '一个时间段，页面停留or网络请求，单位ms，保留两位小数'
    }
];
</script>

<style scoped></style>