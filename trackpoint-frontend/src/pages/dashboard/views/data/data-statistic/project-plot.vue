<template>
    <a-card title="各项目的事件数量" class="card">
        <div ref="container" class="container"></div>
    </a-card>
</template>

<script setup lang="ts">
import { reqProjectStat } from '@/api/v1/data';
import type { IProjectStat } from '@/type/data/stat/project';
import { Chart } from '@antv/g2';
import { message } from 'ant-design-vue';
import { computed, onBeforeUnmount, onMounted, ref, useTemplateRef, watchEffect } from 'vue'


/**
 * 项目统计数据
 */
const data = ref<IProjectStat[]>([])

/* -------------------------------------------------------------------------- */

/**
 * 图上显示的数据
 */
interface IChartData {
    project_name: string
    name: 'default_count' | 'custom_count'
    count: number
}
const chartData = computed<IChartData[]>(() => {
    return data.value.reduce((prev, curr) => {
        return [...prev, {
            project_name: curr.name,
            name: 'default_count',
            count: curr.default_count,
        }, {
            project_name: curr.name,
            name: 'custom_count',
            count: curr.custom_count,
        }]
    }, [] as IChartData[])
})
/**
 * 根据类型获取标题数组，第一个是对应的title，第二个不是，第三个是颜色
 * @param s 
 */
const getInfoByType = (s: IChartData['name']): { title: string, color: string } => {
    if (s === 'default_count') return { title: '默认事件', color: '#2288FF' }
    else return { title: '自定义事件', color: '#0DCCCC' }
}
onMounted(async () => {
    try {
        const resp = await reqProjectStat()
        if (resp.code === 200) {
            data.value = resp.data
        } else {
            message.error(resp.msg)
        }
    } catch {
        message.error('获取项目信息失败')
    }
})


const domRef = useTemplateRef<HTMLDivElement>('container')
let chart: Chart;
watchEffect(() => {
    if (domRef.value) {
        chart = new Chart({ container: domRef.value, autoFit: true })
        chart.interval().data(chartData.value)
            .encode('x', 'project_name').encode('y', 'count').encode('color', 'name')
            .transform({ type: 'stackY' }).interaction('elementHighlight', { background: true })
            .axis('x', {
                title: '项目',
            }).axis('y', {
                title: '事件数量'
            }).legend({
                color: {
                    itemLabelText({ id }: { id: string }) {
                        return getInfoByType(id as IChartData['name']).title
                    }
                }
            }).tooltip({
                items: [
                    // 默认事件
                    (d) => {
                        return {
                            name: getInfoByType('default_count').title,
                            color: getInfoByType('default_count').color,
                            value: chartData.value.find(el => el.project_name === d.project_name && el.name === 'default_count')?.count ?? 0
                        }
                    },
                    // 自定义事件
                    (d) => {
                        return {
                            name: getInfoByType('custom_count').title,
                            color: getInfoByType('custom_count').color,
                            value: chartData.value?.find(el => el.project_name === d.project_name && el.name === 'custom_count')?.count ?? 0
                        }
                    }
                ]
            })
        chart.render()
    }
})
onBeforeUnmount(() => {
    chart?.destroy()
})

</script>

<style scoped>
.card {
    max-width: 500px;
}
</style>