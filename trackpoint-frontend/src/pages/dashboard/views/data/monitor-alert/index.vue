<template>
    <search-project-event-header />
</template>

<script setup lang="ts">
import { SideMenuNameEnum } from '@/enum';
import SearchProjectEventHeader from '~dashboard/component/search-project-event-header.vue';
defineOptions({
    name: SideMenuNameEnum.MonitorAlert
})
</script>

<style scoped></style>