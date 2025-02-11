<template>
    <a-tag v-if="auto" color="green">自动</a-tag>
    <a-tag v-if="manual" color="blue">手动</a-tag>
</template>

<script setup lang="ts">
defineProps<{
    auto?: boolean,
    manual?: boolean
}>()
</script>

<style scoped></style>