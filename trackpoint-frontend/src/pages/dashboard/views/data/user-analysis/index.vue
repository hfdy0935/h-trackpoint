<template>
    <a-tabs v-model:activeKey="activeKey" style="padding: 20px;">
        <a-tab-pane key="1">
            <template #tab>
                用户分布可视化
            </template>
            <project-event-selector @change="pid => queryProjectId = pid" :show-event="false" />
            <user-props-plot :queryProjectId />
        </a-tab-pane>
        <a-tab-pane key="2">
            <template #tab>
                用户行为可视化
            </template>
            <user-hehavior-plot />
        </a-tab-pane>
    </a-tabs>
</template>

<script setup lang="ts">
import { SideMenuNameEnum } from '@/enum';
import { ref } from 'vue';
import UserPropsPlot from './user-props-plot/index.vue'
import UserHehaviorPlot from './user-behavior-plot/index.vue'
import ProjectEventSelector from '@/pages/dashboard/component/project-event-selector.vue';


defineOptions({
    name: SideMenuNameEnum.UserAnalysis
})

// 查询的项目名
const queryProjectId = ref<string>('')
const activeKey = ref("1")
</script>

<style scoped></style>