<template>
    <plot-card :title :spinning>
        <div ref="worldCloudChart" v-if="!spinning && data.length > 0"></div>
        <template #extra>
            <a-radio-group v-model:value="chartType" button-style="solid">
                <a-tooltip title="饼图">
                    <a-radio-button value="pie">
                        <pie-chart-outlined />
                    </a-radio-button>
                </a-tooltip>
                <a-tooltip title="词云图">
                    <a-radio-button value="wordCloud">
                        <file-word-outlined />
                    </a-radio-button>
                </a-tooltip>
            </a-radio-group>
        </template>
        <a-empty v-if="!spinning && data.length === 0"></a-empty>
    </plot-card>
</template>

<script setup lang="ts">
import PlotCard from '@/pages/dashboard/component/plot-card.vue';
import { useChart } from '@/pages/dashboard/composable/useChart';
import type { IClient } from '@/type/data/userAnalysis';
import { PieChartOutlined, FileWordOutlined } from '@ant-design/icons-vue';
import type { Chart } from '@antv/g2';
import { computed, ref, watch } from 'vue';


const { data, getField, spinning } = defineProps<{
    data: IClient[]
    title: string
    /**
     * 获取字段的方法
     */
    getField(d: IClient): string
    spinning: boolean
}>()
// 显示词云图还是饼图
const chartType = ref<'wordCloud' | 'pie'>('pie')
interface IChartDataItem {
    text: string
    value: number
}
const chartData = computed<IChartDataItem[]>(() => {
    const temp1 = new Map<string, number>()
    data.forEach((d) => {
        const osStr = getField(d)
        if (!temp1.has(osStr)) temp1.set(osStr, 1)
        else temp1.set(osStr, temp1.get(osStr)! + 1)
    })
    const result = []
    for (const [name, value] of temp1.entries()) {
        result.push({
            text: name,
            value
        })
    }
    return result
})

// 画词云图
const drawWordCloudChart = (chart: Chart) => {
    chart.wordCloud()
        .data(chartData.value)
        .layout({
            spiral: 'rectangular',
            fontSize: [20, 100],
        })
        .encode('color', 'text')
        .tooltip({
            title: (d: IChartDataItem) => d.text,
            items: [
                (d: IChartDataItem) => ({
                    name: '类型',
                    value: d.text,
                }),
                (d: IChartDataItem) => ({
                    name: '数量',
                    value: d.value,
                }),
                (d: IChartDataItem) => ({
                    name: '占比',
                    value: ((d.value / data.length) * 100).toFixed(2) + ' %',
                }),
            ],
        }).legend(false)
    chart.render()
}
// 画饼图
const drawPieChart = (chart: Chart) => {
    chart.coordinate({ type: 'theta', outerRadius: 0.8 })
    chart
        .interval()
        .data(chartData.value)
        .transform({ type: 'stackY' })
        .encode('y', 'value')
        .encode('color', 'text')
        .label({
            position: 'outside',
            text: (d: IChartDataItem) => ((d.value / data.length) * 100).toFixed(2) + ' %',
        })
        .tooltip((d: IChartDataItem) => ({
            name: d.text,
            value: ((d.value / data.length) * 100).toFixed(2) + ' %',
        }));
    chart.render();
}
const { getChart } = useChart({
    refName: 'worldCloudChart',
    cb: drawPieChart
})

watch(chartType, (newValue) => {
    const chart = getChart()
    if (!chart)
        return
    chart.clear()
    if (newValue === 'wordCloud') drawWordCloudChart(chart)
    else drawPieChart(chart)
})
</script>

<style scoped></style>