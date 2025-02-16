<template>
    <a-row class="row">
        <a-col :span="24" :lg="10" style="margin-top: 10px;">
            <a-space wrap :size="20">
                <a-badge v-for="(item, index) in eventList" :count="item.param_list.length">
                    <div class="item" :class="index === selectedEventIndex ? 'selected' : ''"
                        @click="selectedEventIndex = index">
                        <div class="status" :style="{ backgroundColor: item.status === 1 ? '#00b96b' : 'red' }">
                        </div>
                        <div class="name">{{ item.name }}</div>
                    </div>
                </a-badge>
            </a-space>
        </a-col>
        <a-divider class="divider"></a-divider>
        <a-col :span="24" :lg="13" style="margin-top: 20px;">
            <div style="display: flex; justify-content: space-between;">
                <div class="options">
                    <a-form-item label="语言&emsp;" :colon="false">
                        <a-select v-model:value="language" :dropdownMatchSelectWidth="false">
                            <a-select-option value="json">JSON</a-select-option>
                            <a-select-option value="yaml">YAML</a-select-option>
                        </a-select>
                    </a-form-item>
                    <a-form-item label="主题&emsp;" style="margin-left: 8px;" :colon="false">
                        <a-select v-model:value="theme" :dropdownMatchSelectWidth="false">
                            <a-select-option value="vs">vs</a-select-option>
                            <a-select-option value="vs-dark">vs-dark</a-select-option>
                            <a-select-option value="hc-black">hc-black</a-select-option>
                        </a-select>
                    </a-form-item>
                </div>
                <div class="operations">
                    <a-button style="margin-right: 8px;" @click="reset">重置</a-button>
                    <a-button type="primary" @click="doSubmit">上报</a-button>
                </div>
            </div>
            <vue-monaco-editor v-model:value="code" :theme :language :options="{ readOnly: eventList.length === 0 }"
                class="editor"></vue-monaco-editor>
        </a-col>
    </a-row>
</template>

<script setup lang="ts">
import { reqTestEventList } from '@/api/v1/test';
import type { IEvent } from '@/type/event';
import { message } from 'ant-design-vue';
import { computed, ref, watch, watchEffect } from 'vue';
import { storeToRefs } from 'pinia';
import { useAppStore } from '@/store';
import { loader } from '@guolao/vue-monaco-editor';
import { genJSONStrFromIEvent, genYAMLStrFromIEvent, JSONToYAML, YAMLToJSON } from './util';
import { VueMonacoEditor } from '@guolao/vue-monaco-editor';
import { sendEvent } from '@/h-trackpoint/main';
import yaml from 'js-yaml'

loader.config({
    paths: {
        vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.43.0/min/vs',
    },
})

const { isRegisterSuccess, pid } = defineProps<{
    pid: string
    isRegisterSuccess: boolean
}>()
const { darkMode, textColor, bgColor } = storeToRefs(useAppStore())

/**
 * 可选择的自定义事件列表
 */
const eventList = ref<IEvent[]>([])
watchEffect(async () => {
    if (!isRegisterSuccess) return
    try {
        const resp = await reqTestEventList(pid)
        if (resp.code === 200) {
            eventList.value = resp.data
        }
        else message.error(resp.msg)
    } catch {
        message.error('获取自定义事件失败')
    }
})
// 选中的事件索引
const selectedEventIndex = ref(0)
const language = ref<'json' | 'yaml'>('json') // 语言
const theme = ref<'vs' | 'vs-dark' | 'hc-black'>(darkMode.value === 'light' ? 'vs' : 'vs-dark') // 主题
// 编辑器内容
const code = ref<string>('')
const reset = () => {
    const e = eventList.value[selectedEventIndex.value]
    code.value = language.value === 'json' ? genJSONStrFromIEvent(e) : genYAMLStrFromIEvent(e)
}
watch([eventList, selectedEventIndex], ([newEventList]) => {
    newEventList.length && reset()
})

watch(language, (newValue, oldValue) => {
    // 没事件，随便转
    if (eventList.value.length === 0) return
    try {
        if (newValue === 'json' && oldValue === 'yaml') {
            code.value = YAMLToJSON(code.value)
        }
        else if (newValue === 'yaml' && oldValue === 'json') {
            code.value = JSONToYAML(code.value)
        }
    } catch {
        message.error('转换失败，请检查语法错误')
        language.value = oldValue
    }
})
/**
 * 上报
 */
const doSubmit = async () => {
    try {
        const target = language.value === 'json' ? JSON.parse(code.value) : yaml.load(code.value)
        await sendEvent(eventList.value[selectedEventIndex.value].name, target)
        message.success('已上报，可在network查看请求详情')
    } catch (e) {
        message.error(`上报失败，${e}`)
    }
}
</script>

<style scoped>
.row {
    width: 100%;
    color: v-bind(textColor);
    background-color: v-bind(bgColor);

    .item {
        width: 100px;
        height: 30px;
        border-radius: 6px;
        cursor: pointer;
        display: flex;
        align-items: center;
        box-shadow: 0 0 3px #ccc;

        .status {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin: 0 8px;
        }

        .name {
            text-overflow: ellipsis;
            overflow: hidden;
            white-space: nowrap;
        }
    }

    .selected {
        color: white;
        background-color: #1677FF;
    }

    .editor {
        max-width: 96%;
        max-height: 500px;
        overflow-x: auto;
        margin: 20px;
        border-radius: 6px;
    }

    .divider {
        background-color: #ccc;
    }

    @media (min-width: 992px) {
        .divider {
            display: none;
        }
    }

    .options,
    .operations {
        display: flex;
    }
}
</style>