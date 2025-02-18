<template>
    <a-tag class="tag">点击</a-tag><h-tag manual></h-tag>，点<a-button type="primary" @click="doSendClickEvent" class="btn"
        size="small" style="background-color: rgb(0,200,100);">我</a-button>上报一个点击事件
    <a-tooltip title="事件参数">
        <InfoCircleOutlined @click="$emit('open', dataSource)" />
    </a-tooltip>
</template>

<script setup lang="ts">
import { sendEvent } from '@/h-trackpoint/main'
import type { TableDataItem } from './data'
import { InfoCircleOutlined } from '@ant-design/icons-vue';
import HTag from './h-tag.vue';
import { onBeforeRouteLeave } from 'vue-router';

defineEmits<{
    open: [data: TableDataItem[]]
}>()
interface ReqSendClickEvent {
    x: number
    y: number
    w: number
    h: number
}
/**
 * 手动上报点击事件
 * @param e 
 */
const doSendClickEvent = async (e: MouseEvent) => {
    await sendEvent<ReqSendClickEvent>('click', {
        x: e.clientX,
        y: e.clientY,
        w: window.innerWidth,
        h: window.innerHeight
    })
}
/**
 * 点击事件参数表格数据
 */
const dataSource: TableDataItem[] = [
    {
        name: 'x',
        type: 'number',
        desc: 'x坐标'
    },
    {
        name: 'y',
        type: 'number',
        desc: 'y坐标'
    },
    {
        name: 'w',
        type: 'number',
        desc: '浏览器宽度'
    },
    {
        name: 'h',
        type: 'number',
        desc: '浏览器高度'
    }
]
</script>

<style scoped></style>