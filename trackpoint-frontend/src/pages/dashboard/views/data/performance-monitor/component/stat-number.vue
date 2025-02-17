<template>
    <plot-card title="项目平均时间性能" :spinning>
        <a-row class="row">
            <a-col v-for="(item, index) in showData" :key="index">
                <a-statistic style="margin: 24px;width: 120px;">
                    <template #title>
                        <div style="display: flex;align-items: center;">
                            <a-tooltip :title="item.description">
                                <div class="point" :style="{ backgroundColor: item.pointColor }"></div>
                            </a-tooltip>
                            &emsp;{{
                                item.title
                            }}
                        </div>
                    </template>
                    <template #formatter>
                        <div style="display: flex;">
                            {{ item.avg }}ms
                            <div v-if="showMaxMin"
                                style="font-size: 12px;display: flex;flex-direction: column;margin-left: 2px;">
                                <span style="color: red;">↑&nbsp;{{ item.max }}ms</span>
                                <span style="color: green;">↓&nbsp;{{ item.min }}ms</span>
                            </div>
                        </div>
                    </template>
                </a-statistic>
            </a-col>
        </a-row>
        <a-divider></a-divider>
        <div ref="grapgContainer"></div>
        <template #extra>
            <a-tooltip :title="showMaxMin ? '隐藏最值' : '显示最值'">
                <a-switch v-model:checked="showMaxMin"></a-switch>
            </a-tooltip>
        </template>
    </plot-card>
    <plot-card title="项目平均JS内存占用">
        <a-spin :spinning tip=加载中...>
            <a-statistic style="margin: 30px">
                <template #title>
                    <div style="display: flex;align-items: center;">
                        <a-tooltip :title="'111'">
                            <div class="point" :style="{ backgroundColor: 'red' }"></div>
                        </a-tooltip>
                        &emsp;JS堆内存占用百分比
                    </div>
                </template>
                <template #formatter>
                    <div style="display: flex;">
                        {{ (statData.js_heap_size_used_percent?.avg ?? 0) * 100 + '%' }}
                        <div v-if="showMaxMin1"
                            style="font-size: 12px;display: flex;flex-direction: column;margin-left: 4px;">
                            <span style="color: red;">↑&nbsp;{{ statData.js_heap_size_used_percent?.max * 100 + '%'
                                }}</span>
                            <span style="color: green;">↓&nbsp;{{ statData.js_heap_size_used_percent?.min * 100 + '%'
                                }}</span>
                        </div>
                    </div>
                </template>
            </a-statistic>
        </a-spin>
        <template #extra>
            <a-tooltip :title="showMaxMin1 ? '隐藏最值' : '显示最值'">
                <a-switch v-model:checked="showMaxMin1"></a-switch>
            </a-tooltip>
        </template>
        <div ref="liquidContainer"></div>
    </plot-card>
</template>

<script setup lang="ts">
import { reqPerformanceMonitorStat } from '@/api/v1/data/performanceMonitorStat';
import PlotCard from '@/pages/dashboard/component/plot-card.vue';
import { useChart } from '@/pages/dashboard/composable/useChart';
import type { IPerformanceMonitorItem } from '@/type/data/performanceMonitor';
import { message } from 'ant-design-vue';
import { computed, ref, watchEffect } from 'vue';

const { queryProjectId } = defineProps<{
    queryProjectId: string
}>()

// 统计数据
const statData = ref<IPerformanceMonitorItem>({} as IPerformanceMonitorItem)
const spinning = ref(true)
// 总时间
const maxTotal = computed<number>(() => statData.value.dns !== undefined ? +(statData.value.dns.max + statData.value.tcp.max + statData.value.request.max + statData.value.response.max + statData.value.processing.max + statData.value.load_event_duration.max).toFixed(2) : 0)
const minTotal = computed<number>(() => statData.value.dns !== undefined ? +(statData.value.dns.min + statData.value.tcp.min + statData.value.request.min + statData.value.response.min + statData.value.processing.min + statData.value.load_event_duration.min).toFixed(2) : 0)
const avgTotal = computed<number>(() => statData.value.dns !== undefined ? +(statData.value.dns.avg + statData.value.tcp.avg + statData.value.request.avg + statData.value.response.avg + statData.value.processing.avg + statData.value.load_event_duration.avg).toFixed(2) : 0)
// 选择项目改变
watchEffect(async () => {
    if (!queryProjectId) return
    try {
        spinning.value = true
        const resp = await reqPerformanceMonitorStat(queryProjectId)
        if (resp.code === 200) statData.value = resp.data
        else {
            message.warning(resp.msg)
            statData.value = {} as IPerformanceMonitorItem
        }
    } catch {
        message.error('获取项目性能统计信息失败')
        statData.value = {} as IPerformanceMonitorItem
    } finally {
        spinning.value = false
    }
})
// 是否显示最大最小值
const showMaxMin = ref(false)
// 显示的数据
const showData = computed<{
    title: string
    description: string
    min: number
    avg: number
    max: number
    pointColor: string
}[]>(() => [
    {
        title: 'Total',
        description: '',
        min: minTotal.value ?? 0,
        avg: avgTotal.value ?? 0,
        max: maxTotal.value ?? 0,
        pointColor: 'transparent'
    },
    {
        title: 'DNS',
        description: 'DNS 查询花费的时间。如果是重用连接或是使用了本地 DNS 数据缓存的话，此值为 0。',
        min: statData.value.dns?.min ?? 0,
        avg: statData.value.dns?.avg ?? 0,
        max: statData.value.dns?.max ?? 0,
        pointColor: '#2389FF'
    },
    {
        title: 'TCP',
        description: '建立 TCP 连接花费的时间。如果是走 HTTPS 协议，中间还多一步 TLS 协商生成会话密钥的过程。',
        min: statData.value.tcp?.min ?? 0,
        avg: statData.value.tcp?.avg ?? 0,
        max: statData.value.tcp?.max ?? 0,
        pointColor: '#0DCCCC'
    },
    {
        title: 'Request',
        description: '从开始发起请求，到接收到第一个字节的响应数据，中间经历的时间。',
        min: statData.value.request?.min ?? 0,
        avg: statData.value.request?.avg ?? 0,
        max: statData.value.request?.max ?? 0,
        pointColor: '#F18E56'
    },
    {
        title: 'Response',
        description: '从接受第一个字节的响应数据到接收最后一个字节的响应数据中间经历的时间，也可以认为是资源下载时间。',
        min: statData.value.response?.min ?? 0,
        avg: statData.value.response?.avg ?? 0,
        max: statData.value.response?.max ?? 0,
        pointColor: '#D787FF'
    },
    {
        title: 'Processing',
        description: '渲染页面花费的时长。如果数值很大，那么你可能就要考虑去优化文档结构或是资源大小了。',
        min: statData.value.processing?.min ?? 0,
        avg: statData.value.processing?.avg ?? 0,
        max: statData.value.processing?.max ?? 0,
        pointColor: '#7F6BFF'
    },
    {
        title: 'Load Event',
        description: '当浏览器完成页面中所有的资源加载的时候，会触发一个 load 事件. 在这个阶段，你可以在事件处理函数中，添加额外的处理逻辑。',
        min: statData.value.load_event_duration?.min ?? 0,
        avg: statData.value.load_event_duration?.avg ?? 0,
        max: statData.value.load_event_duration?.max ?? 0,
        pointColor: '#68C738'
    }
])
/* ----------------------------------- 玫瑰图 ---------------------------------- */
interface GraphDataItem {
    name: string
    value: number
    color: string
}
const graphData = computed<GraphDataItem[]>(() => showData.value.filter(s => s.title !== 'Total').map(s => ({
    name: s.title,
    value: s.avg,
    color: s.pointColor
})))
useChart({
    refName: 'grapgContainer',
    cb(chart) {
        chart.coordinate({ type: 'polar', innerRadius: 0.2 })
            .interval()
            .data(graphData.value)
            .encode('x', 'name')
            .encode('y', 'value')
            .encode('color', 'value')
            .scale('x', { padding: 0 })
            .scale('color', {
                range: ['#2389FF', '#0DCCCC', '#F18E56', '#D787FF', '#7F6BFF', '#68C738']
            })
            .axis(false)
            .tooltip({
                title: (d: GraphDataItem) => d.name,
                items: [
                    (d: GraphDataItem) => ({
                        name: d.name,
                        value: d.value,
                        channel: 'y',
                    }),
                ],
            })
            .legend({
                color: false,
            })
            .state('active', { stroke: '#999', lineWidth: 1, zIndex: 101 })
            .state('inactive', { opacity: 0.5, zIndex: 100 })
            .style({
                lineWidth: 1,
                stroke: '#fff',
                radius: 10,
            });
        chart.interaction('elementHighlight', true);
        chart.render();
    }
})

/* ----------------------------------- 水滴图 ---------------------------------- */
const showMaxMin1 = ref(false)
useChart({
    refName: 'liquidContainer',
    options: { height: 300 },
    cb(chart) {
        chart.liquid().data(statData.value.js_heap_size_used_percent?.avg ?? 0).style({
            shape: 'pin', // Build-in shapes: rect, circle, pin, diamond, triangle.
            contentFill: '#fff',
            outlineBorder: 4,
            outlineDistance: 8,
            waveLength: 128,
        });
        chart.render();
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