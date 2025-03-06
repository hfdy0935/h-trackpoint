<template>
    <a-tag class="tag">点击</a-tag><h-tag manual></h-tag>，点击事件，记录屏幕宽高和点击坐标
    <a-tooltip title="事件参数">
        <InfoCircleOutlined @click="$emit('open', dataSource)" />
    </a-tooltip>
</template>

<script setup lang="ts">
import { sendEvent } from 'h-trackpoint'
import type { TableDataItem } from './data'
import { InfoCircleOutlined } from '@ant-design/icons-vue';
import HTag from './h-tag.vue';

defineEmits<{
    open: [data: TableDataItem[]]
}>()

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
