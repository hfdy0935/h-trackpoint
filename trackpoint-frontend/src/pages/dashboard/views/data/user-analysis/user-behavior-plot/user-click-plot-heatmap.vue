<template>
    <div ref="clickHeatmapRef"></div>
</template>

<script setup lang="ts">
import { useChart } from '@/pages/dashboard/composable/useChart';
import { useUserStore } from '@/store';
import type { RespClickRecord } from '@/type/data/userAnalysis';
import type { Chart } from '@antv/g2';
import { message } from 'ant-design-vue';
import { computed, ref, watch } from 'vue';


const { clickData, opacity, size } = defineProps<{
    clickData: RespClickRecord
    opacity: number
    size: number
}>()
const store = useUserStore()
// 页面图片url
const imageUrl = ref('')
watch(() => clickData, async () => {
    try {
        const resp = await fetch(clickData.src, {
            headers: {
                'Authorization': store.token,
                'Content-Type': 'image/png'
            }
        })
        const content = await resp.blob()
        imageUrl.value = URL.createObjectURL(content)
    } catch {
        message.error('获取图片失败')
    }
}, {
    immediate: true
})

interface IHeatData {
    x: number
    y: number
    value: number
}
/**
 * 热度数据
 */
const heatData = computed<IHeatData[]>(() => {
    // 计算热度
    const xyt = new Map<string, number>()
    clickData.xy?.forEach(([x, y]) => {
        const key = `${x},${y}`
        xyt.set(key, xyt.get(key) ?? 0 + 1)
    })
    const showXYH = []
    // y是点到顶部的，但热力图要的是到底部的
    for (const [key, value] of xyt.entries()) {
        showXYH.push({
            x: +key.split(",")[0],
            y: clickData.wh[1] - (+key.split(",")[1]),
            value
        })
    }
    // 需要添加边界的点，把热力图撑开
    showXYH.push({
        x: 0,
        y: 0,
        value: 0
    })
    showXYH.push({
        x: clickData.wh[0],
        y: clickData.wh[1],
        value: 0
    })
    return showXYH
})
/**
 * 画热力图
 */
const deraHeatmap = (chart: Chart) => {
    chart.axis(false);
    chart
        .image()
        .style('src', imageUrl.value)
        .style('x', '50%')
        .style('y', '50%')
        .style('width', '100%')
        .style('height', '100%')
        .tooltip(false);
    chart
        .heatmap()
        .data(heatData.value)
        .encode('x', 'x')
        .encode('y', 'y')
        .encode('color', 'value')
        .encode('size', size)
        .style('opacity', opacity / 100)
        .tooltip({
            title: '位置详情',
            items: [
                (d: IHeatData) => ({
                    name: 'x',
                    value: d.x
                }),
                (d: IHeatData) => ({
                    name: 'y',
                    value: d.y
                }),
                (d: IHeatData) => ({
                    name: '点击次数',
                    value: d.value
                })
            ]
        }).tooltip(false) // 有点问题，先不显示了
    chart.render();
}
useChart({
    refName: 'clickHeatmapRef',
    cb: deraHeatmap
})
</script>
