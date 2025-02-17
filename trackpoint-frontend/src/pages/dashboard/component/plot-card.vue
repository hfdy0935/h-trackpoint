<template>
    <a-spin :spinning tip="加载中...">
        <a-card style="margin: 10px;min-height: 500px;" :bodyStyle="{ padding: '10px' }">
            <template #title>
                <slot name="title">{{ title }}</slot>
            </template>
            <slot></slot>
            <template #extra>
                <slot name="extra"></slot>
            </template>
        </a-card>
    </a-spin>
</template>

<script setup lang="ts">
defineProps<{
    title?: string
    spinning?: boolean
}>()
</script>

<style scoped></style>