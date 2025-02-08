<template>
    <a-menu :theme="darkMode" mode="inline" v-model:selectedKeys="sideIds" :items @click="clickMenuItem">
    </a-menu>
</template>

<script setup lang="ts">
import { useAppStore, useDashboardStore } from '@/store';
import { storeToRefs } from 'pinia';
import { watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getItemByKey, items } from './data';

const route = useRoute()
const router = useRouter()
const { darkMode } = storeToRefs(useAppStore())
const { sideIds, tagCache } = storeToRefs(useDashboardStore())

watch(route, (newValue) => {
    const path = newValue.path
    if (route.meta.admin && tagCache.value.every(el => el.path !== path)) {
        const item = getItemByKey(items, path)
        tagCache.value.push({
            path,
            name: item?.name || '',
            label: item?.label || ''
        })
    }
    sideIds.value = [path]
})
const clickMenuItem = ({ key }: { key: any }) => {
    router.push(key)
}

</script>

<style scoped></style>