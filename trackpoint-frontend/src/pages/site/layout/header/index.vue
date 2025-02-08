<template>
    <div class="container">
        <h-logo />
        <a-menu v-model:selectedKeys="current" class="menu" mode="horizontal" :items :theme="darkMode"
            @click="clickTab" />
        <h-tools />
    </div>
    <account-modal ref="modal" />
</template>

<script setup lang="tsx">
import { computed } from 'vue'
import { HomeFilled, HomeOutlined, AppstoreOutlined, AppstoreFilled } from '@ant-design/icons-vue'
import { message, type MenuProps } from 'ant-design-vue'
import { storeToRefs } from 'pinia'
import { useAppStore, useUserStore } from '@/store'
import AccountModal from './account-modal/index.vue'
import HTools from '@/components/header/h-tools.vue'
import HLogo from '@/components/header/h-logo.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const { bgColor } = storeToRefs(useAppStore())
const { publicTabKey: current } = storeToRefs(useUserStore())
const items = computed<MenuProps['items']>(() => [
    {
        key: '/',
        icon: () => current.value.includes('home') ? <HomeFilled /> : <HomeOutlined />,
        label: '首页'
    },
    {
        key: '/dashboard',
        icon: () => <div>
            {current.value.includes('dashboard') ? <AppstoreFilled /> : <AppstoreOutlined />}
            <span class='dashboard'>控制台</span>
        </div>
    }
])
const { darkMode } = storeToRefs(useAppStore())


const clickTab = async ({ key }: { key: string }) => {
    router.push(key)
}

</script>

<style scoped lang="scss">
.container {
    width: 100vw;
    height: 60px;
    padding: 0 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;

    .menu {
        flex: 1;
        display: flex;
        justify-content: center;
        background-color: v-bind(bgColor);
    }
}
</style>