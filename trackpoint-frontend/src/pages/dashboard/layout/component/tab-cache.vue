<template>
    <div class="container" v-if="tagCache.length">
        <template v-for="(item, idx) in tagCache" :key="item.path">
            <a-dropdown :trigger="['contextmenu']">
                <a-tag :closable="tagCache.length !== 1" @close="closeTag(item)" @click="router.push(item.path)"
                    class="tag" @contextmenu="currTagIdx = idx" :style="calcTagColor(item.path)">
                    <template #icon>
                        <component :is="SideMenuIcon[item.name as SideMenuKey]" />
                    </template>
                    <span class="title">{{ item.label }}</span>
                </a-tag>
                <template v-if="tagCache.length > 1" #overlay>
                    <a-menu>
                        <a-menu-item key="1" :disabled="tagCache.length <= 1" @click="closeOthers">关闭其他</a-menu-item>
                        <a-menu-item key="3" :disabled="idx === 0" @click="closeBefore">关闭之前</a-menu-item>
                        <a-menu-item key="4" :disabled="idx === tagCache.length - 1"
                            @click="closeAfter">关闭之后</a-menu-item>
                    </a-menu>
                </template>
            </a-dropdown>
        </template>
    </div>
</template>

<script setup lang="ts">
import { SideMenuIcon, type SideMenuKey } from '@/enum';
import { useAppStore, useDashboardStore } from '@/store';
import type { TagCacheItem } from '@/store/module/dashboard';
import { storeToRefs } from 'pinia';
import { ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';


const route = useRoute()
const router = useRouter()
const { bgColor, textColor } = storeToRefs(useAppStore())
const { tagCache } = storeToRefs(useDashboardStore())


const closeTag = (item: TagCacheItem) => {
    // 如果关闭的是当前显示的tag
    // 优先找后面的
    if (route.path === item.path) {
        const index = tagCache.value.findIndex(el => el.path === item.path)
        if (index === tagCache.value.length - 1) {
            router.push(tagCache.value[index - 1].path)
        } else {
            router.push(tagCache.value[index + 1].path)
        }
    }
    tagCache.value = tagCache.value.filter(el => el.path !== item.path)
}
const calcTagColor = (path: string) => ({
    backgroundColor: path === route.path ? '#1677FF' : '',
    color: path === route.path ? 'white' : ''
})

// 当前右键tag的索引
const currTagIdx = ref<number>(-1)
const closeOthers = () => {
    const item = tagCache.value[currTagIdx.value]
    router.push(item.path)
    tagCache.value = [item]
}
const closeBefore = () => {
    tagCache.value.splice(0, currTagIdx.value)
    const currPaths = tagCache.value.map(el => el.path)
    // 如果原来在之前，被关了，切换到当前右键点击的tag
    if (!currPaths.includes(route.path)) router.push(tagCache.value[currTagIdx.value - 1].path)
}
const closeAfter = () => {
    tagCache.value.splice(currTagIdx.value + 1)
    const currPaths = tagCache.value.map(el => el.path)
    if (!currPaths.includes(route.path)) router.push(tagCache.value[currTagIdx.value].path)
}
</script>

<style scoped>
.container {
    width: 100%;
    height: 48px;
    overflow-y: hidden;
    background-color: white;
    margin-top: 10px;
    color: v-bind(textColor);
    background-color: v-bind(bgColor);
    display: flex;
    align-items: center;

    .tag {
        font-weight: bold;
        margin: 4px;
        line-height: 24px;

        cursor: pointer;

    }

}
</style>