<template>
    <project-event-selector @change="change" />
</template>

<script setup lang="ts">
import { SideMenuNameEnum } from '@/enum';
import ProjectEventSelector from '@/pages/dashboard/component/project-event-selector.vue';

defineOptions({
    name: SideMenuNameEnum.MonitorAlert
})
const change = async (projectId: string, eventId: string) => {

}
</script>

<style scoped></style>