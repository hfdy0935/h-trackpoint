<template>
    <div>
        <a-button @click="open = true" type="primary"
            style="background-color: #00b96b;margin: 20px 0 0 20px">注册项目</a-button>
        <a-tabs v-model:activeKey="activeKey" class="tabs" :destroyInactiveTabPane="true">
            <a-tab-pane :key="0" tab="默认事件" :style>
                <DefaultEvent></DefaultEvent>
            </a-tab-pane>
            <a-tab-pane :key="1" tab="自定义事件" :style>
                <CustomEvent :isRegisterSuccess :pid="projectData.id"></CustomEvent>
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
import { computed, ref, watchEffect } from 'vue';
import DefaultEvent from './component/default-event/index.vue';
import CustomEvent from './component/custom-event/index.vue'
import { useAppStore } from '@/store';
import { storeToRefs } from 'pinia';

const { bgColor, textColor } = storeToRefs(useAppStore())
const activeKey = ref(1)

const open = ref(false)
const projectData = ref<{
    id: string,
    key: string
}>({ id: '4d465457-2804-4abe-9783-4f3f032c212a', key: '7bd1d6ee-e024-422d-97c3-4ea5457c08fd' })
// 是否注册成功
const isRegisterSuccess = ref(false)
const style = computed(() => {
    return {
        backgroundColor: bgColor.value,
        color: textColor.value
    }
})
const doRegister = async () => {
    try {
        await register({
            projectId: projectData.value.id,
            projectKey: projectData.value.key
        })
        message.success('注册成功')
        isRegisterSuccess.value = true
        open.value = false
    } catch {
        message.error('注册失败')
    }
}

</script>

<style scoped>
.tabs {
    margin: 10px;
    padding-left: 10px;
    background-color: v-bind(bgColor);
    color: v-bind(textColor)
}
</style>