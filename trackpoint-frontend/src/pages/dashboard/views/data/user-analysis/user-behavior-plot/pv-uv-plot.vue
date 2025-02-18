<template>
    <plot-card title="用户访问量" :spinning>
        <a-empty v-if="!spinning && data.length === 0"></a-empty>
        <div v-else ref="chartRef"></div>
    </plot-card>
</template>

<script setup lang="ts">
import { useChart } from '@/pages/dashboard/composable/useChart';
import type { RespUserBehaviorAnalysis } from '@/type/data/userAnalysis';
import { computed } from 'vue';
import PlotCard from '~dashboard/component/plot-card.vue'

const { data, spinning } = defineProps<{ data: RespUserBehaviorAnalysis['visit'], spinning: boolean }>()
interface IChartData {
    time: string
    type: 'pv' | 'uv'
    value: number
}
const chartData = computed<IChartData[]>(() => data.reduce((prev, curr) => [
    ...prev,
    {
        time: curr.time,
        type: 'pv',
        value: curr.pv,
    },
    {
        time: curr.time,
        type: 'uv',
        value: curr.uv,
    }
], [] as IChartData[]))

useChart({
    refName: 'chartRef',
    cb(chart) {
        chart
            .line()
            .data(chartData.value)
            .encode('x', 'time')
            .encode('y', 'value')
            .encode('color', 'type')
            .scale('color', {
                domain: ['pv', 'uv'],
                range: ['#1677FF', 'red'],
            })

        chart.axis('x', {
            title: '时间',
            tickFilter: (_: any, index: number) => index % 10 === 0,
            line: true
        }).axis('y', {
            title: '',
            line: true
        });

        chart.render();
    }
})

</script>

<style scoped></style>