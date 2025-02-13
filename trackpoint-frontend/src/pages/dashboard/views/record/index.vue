<template>
    <table-layout>
        <template #header>
            <a-row style="width: 100%;align-items: center;margin-bottom: 6px;">
                <a-col style="margin:5px 0">
                    <a-select v-model:value="query.projectId" style="width: 200px;margin-left: 10px;"
                        :options="projOptions" allowClear placeholder="选择项目">
                    </a-select>
                </a-col>
                <a-col style="margin:5px 0">
                    <a-select v-model:value="query.eventId" style="width: 200px;margin-left: 10px;"
                        :options="eventOptions" allowClear placeholder="选择事件">
                    </a-select>
                </a-col>
                <a-col>
                    <record-plot />
                    <params-filter />
                </a-col>
            </a-row>
        </template>
        <template #table>
            <table-body />
        </template>
    </table-layout>
</template>

<script setup lang="ts">
import { computed, watch, watchEffect } from 'vue'
import { SideMenuNameEnum } from '@/enum';
import { storeToRefs } from 'pinia';
import TableLayout from '../../component/table-layout.vue';
import TableBody from './component/table/index.vue';
import { useRecordStore } from '@/store';
import { reqProjectEventInfo } from '@/api/v1/record';
import { message } from 'ant-design-vue';
import RecordPlot from './component/plot/index.vue'
import ParamsFilter from './component/params-filter/index.vue'
defineOptions({
    name: SideMenuNameEnum.Record
})
const { query } = storeToRefs(useRecordStore())

// 各项目下事件选项响应体
const { respProjEventOptions } = storeToRefs(useRecordStore())
const { refresh } = useRecordStore()
// 项目名选项
const projOptions = computed(() => respProjEventOptions.value.map(p => ({ value: p.project_name })))
// 选中项目的事件名列表
const eventOptions = computed(() => respProjEventOptions.value.find(item => item.project_name === query.value.projectId)?.events.map(e => ({ value: e.event_name })) ?? [])

watchEffect(async () => {
    try {
        const resp = await reqProjectEventInfo()
        if (resp.code === 200) {
            respProjEventOptions.value = resp.data
            // 默认选第一个项目和第一个事件
            query.value.projectId = resp.data[0]?.project_name ?? ''
            query.value.eventId = resp.data[0]?.events[0]?.event_name ?? ''
        }
        else message.error(resp.msg)
    } catch {
        message.error('获取项目信息失败')
    }
})

// 发送请求
watch(query, () => {
    refresh()
}, {
    immediate: true, deep: true
})
// 清空项目时，自动清空所选事件
watchEffect(() => {
    if (!query.value.projectId) {
        query.value.eventId = ''
    }
})
</script>

<style scoped>
.table {
    width: 100%;
}
</style>