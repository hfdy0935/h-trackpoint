<template>
    <a-tag class="tag">js错误</a-tag><h-tag auto manual></h-tag>，点<a-button danger type="primary" size="small"
        @click="genJSError" style="margin: 0 6px">我</a-button>throw一个Error，可以在console、network查看错误和上报
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
        name: 'error_reason',
        type: 'string',
        desc: '报错原因'
    },
]
</script>

<style scoped></style>