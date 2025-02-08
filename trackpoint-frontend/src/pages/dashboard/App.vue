<template>
    <a-config-provider :theme :locale="zhCN">
        <Layout></Layout>
    </a-config-provider>
</template>

<script setup lang="ts">
import Layout from '~dashboard/layout/index.vue'
import { useAppStore, useUserStore } from '@/store';
import { onBeforeMount } from 'vue';
import { storeToRefs } from 'pinia';
import { reqUser } from '@/api/v1/user';
import { message } from 'ant-design-vue'
import { goToPublicPage } from '@/util/goto';
import zhCN from 'ant-design-vue/es/locale/zh_CN';


const { theme } = storeToRefs(useAppStore())
const { user, token } = storeToRefs(useUserStore())
onBeforeMount(async () => {
    try {
        const resp = await reqUser()
        if (resp.code === 200) user.value = resp.data
        else {
            message.error('登录已过期，请重新登录')
            token.value = ''
            goToPublicPage(1000)
        }
    } catch {
        message.error('登录已过期，请重新登录')
        token.value = ''
        goToPublicPage(1000)
    }
})

</script>
