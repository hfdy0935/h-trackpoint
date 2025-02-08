<template>
    <a-card>
        <a-range-picker v-model:value="date" show-time @change="change" :allowEmpty="[true, true]" />
        <template #title>
            按{{ data.column.title }}过滤
        </template>
    </a-card>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { Dayjs } from 'dayjs';
import { storeToRefs } from 'pinia';
import { useProjectStore } from '@/store';
import { dateStrToDayjs } from '@/util/format';
type RangeValue = [Dayjs?, Dayjs?];
// 自定义筛选器
const props = defineProps<{
    data: any
}>()


const { query, filterProjectField } = storeToRefs(useProjectStore())
const start = (filterProjectField.value === 'create_time' ? query.value.createTimePeriod : query.value.updateTimePeriod)?.start
const end = (filterProjectField.value === 'create_time' ? query.value.createTimePeriod : query.value.updateTimePeriod)?.end
const date = ref<RangeValue>([start ? dateStrToDayjs(start) : undefined, end ? dateStrToDayjs(end) : undefined]);

const change = (_: [Dayjs, Dayjs] | [string, string], dateStrings: [string, string]) => {
    const createTimePeriod = query.value.createTimePeriod
    const updateTimePeriod = query.value.updateTimePeriod
    if (props.data.column.dataIndex === 'create_time' && (dateStrings[0] !== createTimePeriod?.start || dateStrings[1] !== createTimePeriod?.end)) {
        query.value.createTimePeriod = {
            start: dateStrings[0] || undefined,
            end: dateStrings[1] || undefined
        }
    } else if (props.data.column.dataIndex === 'update_time' && (dateStrings[0] !== updateTimePeriod?.start || dateStrings[1] !== updateTimePeriod?.end)) {
        query.value.updateTimePeriod = {
            start: dateStrings[0] || undefined,
            end: dateStrings[1] || undefined
        }
    }
}



</script>

<style scoped></style>