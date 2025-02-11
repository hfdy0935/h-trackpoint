<template>
    <a-card class="card">
        <span class="text">
            > 注册项目时，会返回<span style="color: red;font-size: 18px;">当前项目的</span>默认事件列表，分为<h-tag auto />上报和<h-tag
                manual />上报两类：<br />
            > <a-tag color="warning">注意</a-tag>，手动上报<span style="color: #1677FF;">需要包含绑定的参数</span>并<span
                style="color:red;font-size: 18px;">符合其类型约束</span>（包含这些就行，多传的不校验）
        </span>
        <template v-for="(item, idx) in componentList" :key="idx">
            <a-divider></a-divider>
            <span class="text">
                {{ idx + 1 }}. &emsp;
                <component :is="item" @open="openModal"></component>
            </span>
        </template>
    </a-card>
    <a-modal v-model:open="open" :footer="null" :closable="false">
        <a-table :data-source="modalData" :columns :pagination="false">
        </a-table>
    </a-modal>
</template>

<script setup lang="tsx">
import { computed, ref } from 'vue';
import { useLocalStorage } from '@vueuse/core';
import HClick from './h-click.vue';
import HScreenshot from './h-screenshot.vue';
import HPageStayDuration from './h-page-stay-duration.vue';
import HPerformance from './h-performance.vue';
import HJsError from './h-js-error.vue';
import HRequest from './h-request.vue';
import type { TableDataItem } from './data';
import HTag from './h-tag.vue';
import { columns } from './data';
import { useAppStore } from '@/store';


const componentList = [
    HClick, HScreenshot, HPageStayDuration, HPerformance, HJsError, HRequest
]

/* ---------------------------------- 主题配置 ---------------------------------- */
const { bgColor, textColor } = useAppStore()
/* ---------------------------------- 参数对话框 --------------------------------- */
const modalData = ref<TableDataItem[]>([])

const openModal = (ds: TableDataItem[]) => {
    modalData.value = ds
    open.value = true
}

const open = ref(false)
</script>

<style scoped>
.card {
    margin: 20px;
    padding-top: 10px;
    user-select: none;
    background-color: v-bind(bgColor);
    color: v-bind(textColor);

    .text {
        font-size: 16px;
        font-weight: 600;
        line-height: 40px;
    }

    :deep(.btn) {
        margin: 0 6px;
    }

    :deep(.tag) {
        color: v-bind(textColor)
    }
}
</style>