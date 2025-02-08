<template>
    <a-layout class="layout" style="min-height:100vh">
        <a-layout-sider v-model:collapsed="collapsed" collapsible :style :trigger="null" class="sider"
            :collapsed-width="50">
            <h-logo :hiddenTitle="collapsed" class="logo" />
            <side-menu />
        </a-layout-sider>
        <a-layout>
            <a-layout-header class="layout-header" :style>
                <component :is="collapsed ? MenuUnfoldOutlined : MenuFoldOutlined" @click="collapsed = !collapsed" />
                <admin-header></admin-header>
            </a-layout-header>
            <a-layout-content class="layout-content">
                <tab-cache />
                <div class="outlet">
                    <router-view v-slot="{ Component }">
                        <keep-alive :include="tagCache.map(el => el.name)">
                            <Transition mode="out-in">
                                <component :is="Component" />
                            </Transition>
                        </keep-alive>
                    </router-view>
                </div>
            </a-layout-content>
        </a-layout>
    </a-layout>
</template>
<script setup lang="ts">
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useAppStore, useDashboardStore } from '@/store';
import adminHeader from './component/header/index.vue';
import HLogo from '@/components/header/h-logo.vue';
import { MenuUnfoldOutlined, MenuFoldOutlined } from '@ant-design/icons-vue';
import SideMenu from './component/side-menu/index.vue';
import TabCache from './component/tab-cache.vue';

const { bgColor, textColor } = storeToRefs(useAppStore())
const { tagCache } = storeToRefs(useDashboardStore())
const collapsed = ref(false)

const style = computed(() => ({
    backgroundColor: bgColor.value,
    color: textColor.value,
}))
</script>

<style scoped lang="scss">
.layout {
    height: 100vh;

    .sider {
        .logo {
            height: 60px;
            display: flex;
            justify-content: center;
        }
    }

    &-header {
        height: 60px;
        font-size: 18px;
        padding-inline: 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    &-content {
        overflow: auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;

        .outlet {
            width: 100%;
            height: 100%;
            overflow: auto;
        }
    }
}

.v-enter-from,
.v-leave-to {
    opacity: 0;
}

.v-enter-to,
.v-leave-from {
    opacity: 1;
}

.v-enter-active,
.v-leave-active {
    transition: all 0.1s linear;
}
</style>