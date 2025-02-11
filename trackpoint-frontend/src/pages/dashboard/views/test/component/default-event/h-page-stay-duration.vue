<template>
    <a-tag class="tag">页面停留时长</a-tag><h-tag manual></h-tag>，离开页面之前手动上报
    <a-tooltip title="事件参数">
        <InfoCircleOutlined @click="$emit('open', dataSource)" />
    </a-tooltip>
</template>

<script setup lang="ts">
import type { TableDataItem } from './data';
import { InfoCircleOutlined } from '@ant-design/icons-vue';
import HTag from './h-tag.vue';

defineEmits<{
    open: [dataSource: TableDataItem[]]
}>()
const genJSError = () => {
    throw new Error("I'm an error")
}
const dataSource: TableDataItem[] = [
    {
        name: 'time_duration',
        type: 'string',
        desc: '一个时间段，页面停留or网络请求，单位ms，保留两位小数'
    },
]
</script>

<style scoped></style>