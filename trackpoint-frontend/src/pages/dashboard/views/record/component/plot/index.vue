<template>
    <a-tooltip title="记录可视化">
        <bar-chart-outlined style="margin-left: 10px;font-size: large;" @click="router.push('/performance-monitor')" />
    </a-tooltip>
</template>

<script setup lang="ts">
import { BarChartOutlined } from '@ant-design/icons-vue';
import { useRouter } from 'vue-router';

defineOptions({
    name: 'RecordPlot'
})

const router = useRouter()
</script>
