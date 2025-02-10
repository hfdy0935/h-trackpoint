<template>
    <a-button @click="open = true" type="primary"
        style="background-color: #00b96b;margin: 20px 0 0 20px">注册项目</a-button>
    <a-tabs v-model:activeKey="activeKey" class="tabs">
        <a-tab-pane :key="1" tab="默认事件">
            <DefaultEvent></DefaultEvent>
        </a-tab-pane>
        <a-tab-pane :key="2" tab="自定义事件" force-render>
            <CustomEvent></CustomEvent>
        </a-tab-pane>
    </a-tabs>
    <a-modal v-model:open="open" title="注册项目" @ok="doRegister" ok-text="注册" @cancel="projectData = { id: '', key: '' }"
        cancel-text="取消" :ok-button-props="{ style: { backgroundColor: '#00b96b' } }">
        <a-form :label-col="{ span: 4 }">
            <a-form-item label="项目id" :colon="false">
                <a-input v-model:value="projectData.id"></a-input>
            </a-form-item>
            <a-form-item label="项目key" :colon="false">
                <a-input v-model:value="projectData.key"></a-input>
            </a-form-item>
        </a-form>
    </a-modal>
</template>

<script setup lang="ts">
import { message } from 'ant-design-vue';
import { register } from '@/h-trackpoint/main'
import { ref, watchEffect } from 'vue';
import DefaultEvent from '../component/default-event/index.vue';
import CustomEvent from '../component/custom-event/index.vue'
import useTheme from '../composable';

const { bgColor, textColor } = useTheme()
const activeKey = ref(1)

const open = ref(false)
const projectData = ref<{
    id: string,
    key: string
}>({ id: '', key: '' })

const doRegister = async () => {
    try {
        await register({
            projectId: projectData.value.id,
            projectKey: projectData.value.key
        })
        message.success('注册成功')
        open.value = false
    } catch {
        message.error('注册失败')
    }
}
// 偷个懒，不每次都输入了
// watchEffect(async () => {
//     try {
//         await register({
//             projectId: 'ec07d8ba-b2ea-4c6d-a8ad-731afe7b7b60',
//             key: 'afeef9a5-b468-47bd-bb35-323de6eb501d'
//         })
//         message.success('注册成功')
//         open.value = false
//     } catch (e) {
//         message.error('注册失败')
//     }
// })
</script>

<style scoped>
.tabs {
    margin: 30px;
    padding: 20px;
    background-color: v-bind(bgColor);
    color: v-bind(textColor)
}
</style>