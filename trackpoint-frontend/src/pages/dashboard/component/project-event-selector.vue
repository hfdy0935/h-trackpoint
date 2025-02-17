<template>
    <a-row style="width: 100%;">
        <a-col style="margin:5px 10px">
            <a-form-item label="项目" :colon="false">
                <a-select v-model:value="query.projectId" style="width: 200px;margin-left: 10px;"
                    :options="projectOptions" placeholder="选择项目"
                    :field-names="{ label: 'project_name', value: 'project_id' }">
                </a-select>
            </a-form-item>
        </a-col>
        <a-col style="margin:5px 10px" v-if="showEvent">
            <a-form-item label="事件" :colon="false">
                <a-select v-model:value="query.eventId" style="width: 200px;margin-left: 10px;" :options="eventOptions"
                    placeholder="选择事件" :field-names="{ label: 'event_name', value: 'event_id' }">
                </a-select>
            </a-form-item>
        </a-col>
        <a-col style="margin:5px 10px">
            <slot name="extra"></slot>
        </a-col>
    </a-row>
</template>


<script lang="ts" setup>
import { computed, ref, watch, watchEffect } from 'vue'
import { reqProjectEventInfo } from '@/api/v1/record';
import { message } from 'ant-design-vue';
import type { IProjectEventInfo } from '@/type/record';

const { showEvent = true } = defineProps<{
    showEvent?: boolean
}>()

const emit = defineEmits<{
    /**
     * 改变了且项目id和事件id都不为空时触发
     */
    change: [projectId: string, eventId: string]
}>()
const query = ref<{
    projectId: string
    eventId: string
}>({ projectId: '', eventId: '' })
// 各项目下事件选项响应体
const projectOptions = ref<IProjectEventInfo[]>([])

watchEffect(async () => {
    try {
        const resp = await reqProjectEventInfo()
        if (resp.code === 200) {
            projectOptions.value = resp.data
            // 默认选第一个项目和第一个事件
            query.value.projectId = resp.data[0]?.project_id ?? ''
            query.value.eventId = resp.data[0]?.events[0]?.event_id ?? ''
        }
        else message.error(resp.msg)
    } catch {
        message.error('获取项目信息失败')
    }
})
// 选中项目的事件名列表
const eventOptions = computed(() => projectOptions.value.find(item => item.project_id === query.value.projectId)?.events)

// 清空项目时，自动清空所选事件
watchEffect(() => {
    if (!query.value.projectId) {
        query.value.eventId = ''
    }
})
watch(query, () => {
    emit('change', query.value.projectId, query.value.eventId)
}, {
    deep: true
})
</script>