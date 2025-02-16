<template>
    <a-tag class="tag">截图</a-tag><h-tag auto></h-tag>，每次上报点击事件时会返回这次事件记录的id以及是否需要上传截图，如果需要，会将 document.body ==>
    canvas ==>
    blob
    进行上传
</template>

<script setup lang="ts">
import HTag from './h-tag.vue';

defineEmits<{
    open: [void]
}>()
</script>

<style scoped></style>