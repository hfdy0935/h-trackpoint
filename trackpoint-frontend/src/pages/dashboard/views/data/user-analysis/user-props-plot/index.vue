<template>
    <a-row style="width:100%">
        <a-col :span="24" :xl="12">
            <user-props-plot :data :get-field="d => d.os + ' ' + d.os_version" title="操作系统类型" :spinning />
        </a-col>
        <a-col :span="24" :xl="12">
            <user-props-plot :data :get-field="d => d.browser + ' ' + d.browser_version" title="浏览器类型" :spinning />
        </a-col>
        <a-col :span="24" :xl="12">
            <user-props-plot :data :get-field="d => d.device" title="设备类型" :spinning />
        </a-col>
        <a-col :span="24" :xl="12">
            <user-distribution-plot :data />
        </a-col>
    </a-row>
</template>

<script setup lang="ts">
import { reqUserAnalysisUserList } from '@/api/v1/data/userAnalysis';
import type { IClient } from '@/type/data/userAnalysis';
import { message } from 'ant-design-vue';
import { ref, watchEffect } from 'vue';
import UserPropsPlot from './user-props-plot.vue';
import UserDistributionPlot from './user-distribution-plot/index.vue';



const { queryProjectId } = defineProps<{
    queryProjectId: string
}>()

const data = ref<IClient[]>([])
const spinning = ref(true)
watchEffect(async () => {
    if (!queryProjectId) return
    try {
        spinning.value = true
        const resp = await reqUserAnalysisUserList(queryProjectId)
        if (resp.code === 200) {
            data.value = resp.data
        } else {
            message.error(resp.msg)
        }
    } catch {
        message.error('获取用户信息失败')
    } finally {
        spinning.value = false
    }
})

</script>

<style scoped></style>