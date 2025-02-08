<template>
    <table-layout>
        <template #header>
            <a-row style="width: 100%;align-items: center;margin-bottom: 6px;">
                <a-col style="margin:5px 0">
                    <a-input v-model:value.trim="query.keyword" allow-clear placeholder="搜索事件名或描述"></a-input>
                </a-col>
                <a-col style="margin:5px 0">
                    <a-select v-model:value="query.projectIdList" mode="multiple"
                        style="width: 200px;margin-left: 10px;" :options="selectOptions" allowClear placeholder="选择项目">
                    </a-select>
                </a-col>
                <a-col :span="24">
                    <create-event-modal v-if="query.type === EventTypeEnum.CUSTOM" />
                </a-col>
            </a-row>
        </template>
        <template #table>
            <a-tabs v-model:activeKey="query.type" style="width: 100%;">
                <a-tab-pane :key="EventTypeEnum.DEFAULT" tab="默认事件">
                    <table-body />
                </a-tab-pane>
                <a-tab-pane :key="EventTypeEnum.CUSTOM" tab="自定义事件" force-render>
                    <table-body />
                </a-tab-pane>
            </a-tabs>
        </template>
    </table-layout>
</template>

<script setup lang="ts">
import { computed, watch, watchEffect } from 'vue'
import { EventTypeEnum, SideMenuNameEnum } from '@/enum';
import { storeToRefs } from 'pinia';
import { useEventStore } from '@/store';
import TableLayout from '../../component/table-layout.vue';
import CreateEventModal from './component/create-update-event-modal/index.vue'
import TableBody from './component/table-body.vue';
defineOptions({
    name: SideMenuNameEnum.Event
})

const { query, projectOptions } = storeToRefs(useEventStore())
/**
 * 根据项目名过滤事件
 */
const selectOptions = computed(() => projectOptions.value.map(el => ({ value: el.name })))
const { refresh } = useEventStore()
watch(query, () => {
    refresh()
}, { immediate: true, deep: true })
</script>

<style scoped>
.table {
    width: 100%;
}
</style>