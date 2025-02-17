<template>
    <div ref="clickHeatmapRef"></div>
</template>

<script setup lang="ts">
import { useChart } from '@/pages/dashboard/composable/useChart';
import { useUserStore } from '@/store';
import type { RespClickRecord } from '@/type/data/userAnalysis';
import { message } from 'ant-design-vue';


const { clickData } = defineProps<{
    clickData: RespClickRecord
}>()
const store = useUserStore()
const reqImage = async (url: string) => {
    try {
        const resp = await fetch(url, {
            headers: {
                'Authorization': store.token,
                'Content-Type': 'image/png'
            }
        })
        const content = await resp.blob()
        return URL.createObjectURL(content)
    } catch {
        message.error('获取图片失败')
    }
}
useChart({
    refName: 'clickHeatmapRef',
    async cb(chart) {
        // 没点不画图
        if (clickData.xy?.length === 0) {
            chart?.clear()
            return
        }
        const url = await reqImage(clickData.src)
        // 计算热度
        const xyt = new Map<string, number>()
        clickData.xy?.forEach(([x, y]) => {
            const key = `${x},${y}`
            xyt.set(key, xyt.get(key) ?? 0 + 1)
        })
        const showXYH = []
        for (const [key, value] of xyt.entries()) {
            showXYH.push({
                x: +key.split(",")[0],
                y: +key.split(",")[1],
                value
            })
        }
        // 加一个边界，以适应比例？
        showXYH.push({
            x: clickData.wh[0],
            y: clickData.wh[1],
            value: 1
        })
        console.log(showXYH);

        chart.axis(false);
        chart
            .image()
            .style(
                'src',
                url
            )
            .style('x', '50%')
            .style('y', '50%')
            .style('width', '100%')
            .style('height', '100%')
            .tooltip(false);
        chart
            .heatmap()
            .data(showXYH)
            .encode('x', 'x')
            .encode('y', 'y')
            .encode('color', 'value')
            .style('opacity', 0.4)
            .tooltip(false);
        chart.render();
    }
})

</script>
