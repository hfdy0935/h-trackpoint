<template>
    <div style="width: 100%;height: 100%;overflow: hidden;">
        <iframe src="/sdk-test/" style="width: 100%;height:100%;"></iframe>
    </div>
</template>

<script setup lang="ts">
import { SideMenuNameEnum } from '@/enum';

defineOptions({
    name: SideMenuNameEnum.Test
})

</script>

<style scoped></style>