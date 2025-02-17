<template>
    <table-layout>
        <template #header>
            <project-event-selector @change="pid => queryProjectId = pid" :showEvent="false" />
        </template>
        <a-row style=" width: 100%;">
            <a-col :spam="24" :lg="12">
                <stat-number :queryProjectId />
            </a-col>
            <a-col :span="24" :lg="12">
                <per-page-plot :queryProjectId />
            </a-col>
        </a-row>
    </table-layout>
</template>

<script setup lang="ts">
import { SideMenuNameEnum } from '@/enum';
import TableLayout from '@/pages/dashboard/component/table-layout.vue';
import { ref } from 'vue';
import StatNumber from './component/stat-number.vue';
import PerPagePlot from './component/per-page-plot.vue';
import ProjectEventSelector from '@/pages/dashboard/component/project-event-selector.vue';

defineOptions({
    name: SideMenuNameEnum.PerformanceMonitor
})

// 查询的项目名
const queryProjectId = ref<string>('')
</script>

<style scoped></style>