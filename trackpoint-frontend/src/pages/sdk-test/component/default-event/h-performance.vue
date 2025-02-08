<template>
    <a-tag class="tag">performance API指标</a-tag><h-tag auto></h-tag>，浏览器支持的情况下会在项目注册完毕时上报一次
    <a-tooltip title="事件参数">
        <InfoCircleOutlined @click="$emit('open', dataSource)" />
    </a-tooltip>
</template>

<script setup lang="ts">
import type { TableDataItem } from './data';
import HTag from './h-tag.vue';
import { InfoCircleOutlined } from '@ant-design/icons-vue';

defineEmits<{
    open: [data: TableDataItem[]]
}>()


const dataSource: TableDataItem[] = [
    {
        name: 'dns',
        type: 'number',
        desc: 'DNS查询耗时，单位ms'
    },
    {
        name: 'tcp',
        type: 'number',
        desc: 'TCP连接耗时，单位ms'
    },
    {
        name: 'request',
        type: 'number',
        desc: '开始请求到接收到第一个字节的耗时，单位ms'
    },
    {
        name: 'response',
        type: 'number',
        desc: '从接收到第一个至接收到最后一个字节的耗时，单位ms'
    },
    {
        name: 'processing',
        type: 'number',
        desc: '渲染页面耗时，单位ms'
    },
    {
        name: 'loadEvent',
        type: 'number',
        desc: '资源加载完毕之后，加载事件的耗时，单位ms'
    },
    {
        name: 'jsHeapUsedPercent',
        type: 'number',
        desc: 'JS堆占用百分比'
    }
];
</script>

<style scoped></style>