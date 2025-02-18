<template>
    <plot-card title="各页面用户停留时长" :spinning>
        <a-empty v-if="!spinning && data.length === 0"></a-empty>
        <div ref="chart" v-if="!spinning && data.length > 0"></div>
    </plot-card>
</template>

<script setup lang="ts">
import PlotCard from '@/pages/dashboard/component/plot-card.vue';
import { useChart } from '@/pages/dashboard/composable/useChart';
import type { RespUserBehaviorAnalysis } from '@/type/data/userAnalysis';

interface IStay {
    page_url: string
    // 单位： s
    max: number
    avg: number
    min: number
}
const { data, spinning } = defineProps<{
    data: RespUserBehaviorAnalysis['stay']
    spinning: boolean
}>()
useChart({
    refName: 'chart',
    options: { height: 456 },
    cb(chart) {
        chart.clear()
        chart
            .line()
            .data(data)
            .encode('x', 'page_url')
            .encode('y', 'min')
            .encode('color', 'orange')
            .style('gradient', 'y')
            .tooltip({
                title: (d: IStay) => d.page_url,
                items: [
                    (d: IStay) => ({
                        name: '最小值',
                        value: d.min + ' s',
                        channel: 'y',
                    }),
                ],
            }).style('lineWidth', 2)
        chart
            .line()
            .data(data)
            .encode('x', 'page_url')
            .encode('y', 'max')
            .encode('color', 'purple')
            .style('gradient', 'y')
            .tooltip({
                title: (d: IStay) => d.page_url,
                items: [
                    (d: IStay) => ({
                        name: '最大值',
                        value: d.max + ' s',
                        channel: 'y',
                    }),
                ]
            }).style('lineWidth', 2)
        chart
            .line()
            .data(data)
            .encode('x', 'page_url')
            .encode('y', 'avg')
            .encode('color', 'deepskyblue')
            .style('gradient', 'y')
            .tooltip({
                title: (d: IStay) => d.page_url,
                items: [
                    (d: IStay) => ({
                        name: '平均值',
                        value: d.avg + ' s',
                        channel: 'y',
                    }),
                ],
            }).style('lineWidth', 2)
        chart.axis('x', {
            title: '页面',
            line: true,
            labelFormatter: () => ''
        }).axis('y', {
            title: '',
            line: true
        }).scale('color', { palette: 'turbo' }).legend(false)
        chart.render()
    }
})
</script>

<style scoped></style>