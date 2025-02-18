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
import { useRecordStore } from '@/store';
import { dateStrToDayjs } from '@/util/format';
type RangeValue = [Dayjs?, Dayjs?];
// 自定义筛选器
defineProps<{
    data: any
}>()


const { query } = storeToRefs(useRecordStore())
const start = query.value.createTimePeriod?.start
const end = query.value.createTimePeriod?.end
const date = ref<RangeValue>([start ? dateStrToDayjs(start) : undefined, end ? dateStrToDayjs(end) : undefined]);

const change = async (_: [Dayjs, Dayjs] | [string, string], dateStrings: [string, string]) => {
    const createTimePeriod = query.value.createTimePeriod
    if ((dateStrings[0] !== createTimePeriod?.start || dateStrings[1] !== createTimePeriod?.end)) {
        query.value.createTimePeriod = {
            start: dateStrings[0] || undefined,
            end: dateStrings[1] || undefined
        }
    }
}
</script>