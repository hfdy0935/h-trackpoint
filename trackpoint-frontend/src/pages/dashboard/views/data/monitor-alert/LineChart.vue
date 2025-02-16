<template>
    <div ref="chart" class="line-chart"></div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted, onBeforeUnmount } from 'vue';
  import * as echarts from 'echarts/core';
  import { LineChart } from 'echarts/charts';
  import {
    TitleComponent,
    TooltipComponent,
    GridComponent,
    DataZoomComponent,
  } from 'echarts/components';
  import { CanvasRenderer } from 'echarts/renderers';
  import type { ECharts, EChartsOption } from 'echarts';
  
  // 注册必要的组件
  echarts.use([
    TitleComponent,
    TooltipComponent,
    GridComponent,
    DataZoomComponent,
    LineChart,
    CanvasRenderer
  ]);
  
  const props = defineProps<{
    data: [string, number][];
    title: string;
  }>();
  
  const chart = ref<HTMLElement | null>(null);
    let chartInstance: any = null;
    onMounted(() => {
  if (chart.value) {
    chartInstance = echarts.init(chart.value) as any;
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
  
    const option: EChartsOption = {
      title: {
        text: props.title,
        left: 'center',
        textStyle: {
          fontSize: 16,
          color: '#333',
        },
      },
      tooltip: {
        trigger: 'axis',
        formatter: (params: any) => { // 使用 any 类型避免复杂类型定义
          if (Array.isArray(params)) {
            return params.map((param) => `${param.name}<br>${param.value}`).join('<br>');
          }
          return `${params.name}<br>${params.value}`;
        },
      },
      xAxis: {
        type: 'category',
        data: props.data.map((item) => item[0]),
      },
      yAxis: {
        type: 'value',
        name: '报错数量',
      },
      series: [
        {
          name: 'JS 报错',
          type: 'line',
          data: props.data.map((item) => item[1]),
          color: '#FF6700',
          smooth: true,
          lineStyle: {
            width: 2,
          },
          itemStyle: {
            borderColor: '#FF6700',
            borderWidth: 2,
          },
        },
      ],
    };
  
    chartInstance.setOption(option);
  };
  </script>
  
  <style scoped>
  .line-chart {
    width: 100%;
    height: 300px;
  }
  </style>