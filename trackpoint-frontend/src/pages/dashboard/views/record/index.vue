<template>
    <table-layout>
        <template #header>
            <project-event-selector @change="change">
                <template #extra>
                    <record-plot />
                    <params-filter />
                </template>
            </project-event-selector>
        </template>
        <table-body />
    </table-layout>
</template>


<script lang="ts" setup>
import { SideMenuNameEnum } from '@/enum';
import { useRecordStore } from '@/store';
import RecordPlot from './component/plot/index.vue'
import ParamsFilter from './component/params-filter/index.vue'
import TableBody from './component/table/index.vue'
import TableLayout from '~dashboard/component/table-layout.vue';
import { watch } from 'vue'
import { storeToRefs } from 'pinia';
import ProjectEventSelector from '~dashboard/component/project-event-selector.vue'

defineOptions({
    name: SideMenuNameEnum.Record
})

const { query } = storeToRefs(useRecordStore())
const { refresh } = useRecordStore()

const change = (projectId: string, eventId: string) => {
    query.value.projectId = projectId
    query.value.eventId = eventId
}

watch(query, () => {
    refresh()
}, {
    deep: true
})
</script>