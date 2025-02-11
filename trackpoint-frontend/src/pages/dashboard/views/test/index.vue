<template>
    <div>
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
        <a-modal v-model:open="open" title="注册项目" @ok="doRegister" ok-text="注册"
            @cancel="projectData = { id: '', key: '' }" cancel-text="取消"
            :ok-button-props="{ style: { backgroundColor: '#00b96b' } }">
            <a-form :label-col="{ span: 4 }">
                <a-form-item label="项目id" :colon="false">
                    <a-input v-model:value="projectData.id"></a-input>
                </a-form-item>
                <a-form-item label="项目key" :colon="false">
                    <a-input v-model:value="projectData.key"></a-input>
                </a-form-item>
            </a-form>
        </a-modal>
    </div>
</template>

<script setup lang="ts">
import { message } from 'ant-design-vue';
import { register } from '@/h-trackpoint/main'
import { ref, watchEffect } from 'vue';
import DefaultEvent from './component/default-event/index.vue';
import CustomEvent from './component/custom-event/index.vue'
import { useAppStore } from '@/store';

const { bgColor, textColor } = useAppStore()
const activeKey = ref(1)

const open = ref(false)
const projectData = ref<{
    id: string,
    key: string
}>({ id: '6b810d0f-6951-4721-85c6-9077c16985e0', key: '41301853-21e2-4b84-b708-26d3f4df8996' })

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

</script>

<style scoped>
.tabs {
    margin: 30px;
    padding: 20px;
    background-color: v-bind(bgColor);
    color: v-bind(textColor)
}
</style>