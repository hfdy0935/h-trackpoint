<template>
    <div ref="chart" class="ring-gauge"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import * as echarts from 'echarts';

const props = defineProps({
    title: String, // 图表标题
    value: Number, // 当前值
    max: { // 最大值
        type: Number,
        default: 100,
    },
    color: { // 环形颜色
        type: String,
        default: '#5470C6',
    },
});

const chart = ref<HTMLElement | null>(null);
let chartInstance: echarts.ECharts | null = null;

onMounted(() => {
    if (chart.value) {
        chartInstance = echarts.init(chart.value);
        renderChart();
    }
});

onBeforeUnmount(() => {
    if (chartInstance) {
        chartInstance.dispose();
    }
});

const renderChart = () => {
    if (!chartInstance) return;

    const option = {
        series: [
            {
                type: 'gauge',
                center: ['50%', '50%'],
                startAngle: 180,
                endAngle: 0,
                min: 0,
                max: props.max,
                splitNumber: 10,
                progress: {
                    show: true,
                    width: 15,
                    itemStyle: {
                        color: props.color,
                    },
                },
                axisLine: {
                    lineStyle: {
                        width: 15,
                        color: [[1, '#EEE']],
                    },
                },
                axisTick: {
                    show: false,
                },
                splitLine: {
                    show: false,
                },
                axisLabel: {
                    show: false,
                },
                detail: {
                    valueAnimation: true,
                    formatter: '{value}%',
                    fontSize: 20,
                    color: 'auto',
                    offsetCenter: [0, '70%'],
                },
                data: [
                    {
                        value: props.value,
                        name: props.title,
                    },
                ],
            },
        ],
    };

    chartInstance.setOption(option);
};
</script>

<style scoped>
.ring-gauge {
    width: 100%;
    height: 200px;
}
</style> 