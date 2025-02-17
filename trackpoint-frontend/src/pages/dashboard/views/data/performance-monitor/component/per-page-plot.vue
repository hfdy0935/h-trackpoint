<template>
    <plot-card title="各页面平均时间性能" :spinning>
        <div ref="grapgContainer"></div>
        <template #extra>
            <a-radio-group v-model:value="direction" button-style="solid">
                <a-radio-button value="h">
                    <bar-chart-outlined />
                </a-radio-button>
                <a-radio-button value="v">
                    <bar-chart-outlined style="transform: rotate(90deg);" />
                </a-radio-button>
            </a-radio-group>
        </template>
    </plot-card>
    <plot-card title="各页面平均JS内存占用" :spinning>
        <div ref="JSGraphContainer"></div>
    </plot-card>
</template>

<script setup lang="ts">
import { reqPerformanceMonitorPerPage } from '@/api/v1/data/performanceMonitorStat';
import { useChart } from '@/pages/dashboard/composable/useChart';
import { BarChartOutlined } from '@ant-design/icons-vue';
import type { IPerformanceMonitorPerPage } from '@/type/data/performanceMonitor';
import { message } from 'ant-design-vue';
import { computed, ref, watch, watchEffect } from 'vue';
import PlotCard from '@/pages/dashboard/component/plot-card.vue';

const { queryProjectId } = defineProps<{
    queryProjectId: string
}>()

// 统计数据
const statData = ref<IPerformanceMonitorPerPage[]>([])
const spinning = ref(true)
watchEffect(async () => {
    if (!queryProjectId) return
    try {
        spinning.value = true
        const resp = await reqPerformanceMonitorPerPage(queryProjectId)
        if (resp.code === 200) statData.value = resp.data
        else {
            message.warning(resp.msg)
            statData.value = []
        }
    } catch {
        message.error('获取项目性能统计信息失败')
        statData.value = []
    } finally {
        spinning.value = false
    }
})

/* ---------------------------------- 时间性能的图 ---------------------------------- */
interface IShowDataItem {
    page_url: string
    name: string
    avg: number
    max: number
    min: number
}
const showData = computed<IShowDataItem[]>(() => statData.value?.reduce((prev, curr) => {
    return [
        ...prev, ...Object.entries(curr.performance).filter(p => p[0] !== 'js_heap_size_used_percent').map(([k, v]) => ({
            page_url: curr.page_url,
            name: k,
            ...v
        }))
    ]
}, [] as IShowDataItem[]) ?? [])
const { getChart } = useChart({
    refName: 'grapgContainer',
    cb(chart) {
        chart
            .interval()
            .data(showData.value)
            .transform({ type: 'stackY' })
            .encode('x', 'page_url')
            .encode('y', 'avg')
            .encode('color', 'name')
            .axis('x', {
                title: '页面url',
                labelFormatter: () => ''
            })
            .axis('y', {
                title: '平均耗时'
            })
            .tooltip({
                title: (d: IShowDataItem) => d.page_url,
                items: [
                    (d: IShowDataItem) => ({
                        name: '最大值',
                        value: d.max + ' ms',
                        channel: 'y',
                    }),
                    (d: IShowDataItem) => ({
                        name: '平均值',
                        value: d.avg + ' ms',
                        channel: 'y',
                    }),
                    (d: IShowDataItem) => ({
                        name: '最小值',
                        value: d.min + ' ms',
                        channel: 'y',
                    }),
                ],
            })
        chart.render();
    }
})
// 图的方向
const direction = ref<'h' | 'v'>('h')
watch([direction], () => {
    getChart()?.coordinate({ transform: direction.value === 'v' ? [{ type: 'transpose' }] : [] })
        .render();
})
/* ---------------------------------- js_heap_size_used_percent的图 ---------------------------------- */
const jsData = computed(() => statData.value.map(p => ({
    page_url: p.page_url,
    name: 'js_heap_size_used_percent',
    ...p.performance.js_heap_size_used_percent
})))
useChart({
    refName: 'JSGraphContainer',
    cb(chart) {
        chart
            .line()
            .data(jsData.value)
            .encode('x', 'page_url')
            .encode('y', 'min')
            .encode('color', 'lightgreen')
            .style('gradient', 'y')
            .tooltip({
                title: (d: IShowDataItem) => d.page_url,
                items: [
                    (d: IShowDataItem) => ({
                        name: '最小值',
                        value: (d.min * 100).toFixed(2) + ' %',
                        channel: 'y',
                    }),
                ],
            }).style('lineWidth', 2)
        chart
            .line()
            .data(jsData.value)
            .encode('x', 'page_url')
            .encode('y', 'max')
            .encode('color', 'red')
            .style('gradient', 'y')
            .tooltip({
                title: (d: IShowDataItem) => d.page_url,
                items: [
                    (d: IShowDataItem) => ({
                        name: '最大值',
                        value: (d.max * 100).toFixed(2) + ' %',
                        channel: 'y',
                    }),
                ]
            }).style('lineWidth', 2)
        chart
            .line()
            .data(jsData.value)
            .encode('x', 'page_url')
            .encode('y', 'avg')
            .encode('color', 'deepskyblue')
            .style('gradient', 'y')
            .tooltip({
                title: (d: IShowDataItem) => d.page_url,
                items: [
                    (d: IShowDataItem) => ({
                        name: '平均值',
                        value: (d.avg * 100).toFixed(2) + ' %',
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
        }).scale('color', { palette: 'turbo' })
        chart.render()
    }
})
</script>

<style scoped>
.point {
    width: 12px;
    height: 12px;
    border-radius: 50%;
}
</style>