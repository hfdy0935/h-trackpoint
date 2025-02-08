<template>
    <a-tooltip title="修改">
        <a-button type="primary" @click="open = true">
            <template #icon>
                <edit-outlined />
            </template>
        </a-button>
    </a-tooltip>
    <a-modal v-model:open="open" cancel-text="取消" ok-text="提交" :closable="false" centered @ok="doSubmit"
        destroy-on-close>
        <a-form :rules :model="data" ref="form" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
            <a-form-item label="项目名" name="name" has-feedback :colon="false">
                <a-input v-model:value="data.name" placeholder="项目名" allow-clear></a-input>
            </a-form-item>
            <a-form-item label="项目描述" :colon="false">
                <a-input v-model:value="data.description" placeholder="项目描述" allow-clear></a-input>
            </a-form-item>
            <a-form-item label="默认事件" :colon="false">
                <a-transfer v-model:target-keys="addedDefaultEventList" :data-source="defaultEventListAll"
                    :titles="['未添加', '已添加']" :render="(item: ISelectItem) => item.name" @change="" @selectChange=""
                    @scroll="" />
            </a-form-item>
            <a-form-item label="自定义事件" :colon="false">
                <a-transfer v-model:target-keys="addedCustomEventList" :data-source="customEventListAll"
                    :titles="['未添加', '已添加']" :render="(item: ISelectItem) => item.name" @change="" @selectChange=""
                    @scroll="" />
            </a-form-item>
        </a-form>
        <template #title>
            修改项目
            <a-tooltip title="移除事件之后，原事件将无法上报，请确保做好修改">
                <question-circle-outlined style="color:red;margin-bottom: 20px;" />
            </a-tooltip>
        </template>
    </a-modal>
</template>

<script setup lang="ts">
import { EditOutlined, QuestionCircleOutlined, ExclamationCircleOutlined } from '@ant-design/icons-vue'
import { computed, ref, useTemplateRef, watch, watchEffect, h } from 'vue';
import { rules } from './data';
import { storeToRefs } from 'pinia';
import { useDashboardStore, useEventStore, useProjectStore, useUserStore } from '@/store';
import type { IProject } from '@/type/project';
import { message, Modal, type FormInstance } from 'ant-design-vue'
import { deepcopy } from '@/util/common';
import { reqUpdateProject } from '@/api/v1/project';

const { id } = defineProps<{
    /**
     * 项目id
     */
    id: string
}>()
const open = ref(false)
const { user } = storeToRefs(useUserStore())
const { data: projects } = storeToRefs(useProjectStore())
const { refresh: refreshProject } = useProjectStore()
const { refresh: refreshUser } = useUserStore()
const { isEventPageCached } = storeToRefs(useDashboardStore())
const { refresh: refreshEvent } = useEventStore()
const formRef = useTemplateRef<FormInstance>('form')
/**
 * 选择器类型
 */
interface ISelectItem {
    key: IProject['id']
    name: IProject['name']
}
// 当前的项目
const currentProjectData = computed(() => projects.value.records.find(el => el.id === id)!)
// 用来存项目名、项目描述
const data = ref<IProject>(deepcopy(currentProjectData.value))

// 所有默认事件.value
const { eventOptions } = storeToRefs(useProjectStore())
// 所有默认事件
const defaultEventListAll = computed<ISelectItem[]>(() => eventOptions.value.default.map(el => ({
    key: el.id,
    name: el.name,
})))
const addedDefaultEventList_ = computed<string[]>(() => eventOptions.value.default.filter(el => currentProjectData.value.event_list.some(el2 => el2.id === el.id)).map(e => e.id))
// 已添加的默认事件id列表，以默认事件的id为key
const addedDefaultEventList = ref<string[]>(deepcopy(addedDefaultEventList_.value))
// 所有用户自定义事件
const customEventListAll = computed<ISelectItem[]>(() => eventOptions.value.custom.map(el => ({
    key: el.id,
    name: el.name
})))
// 已添加的用户自定义事件
const addedCustomEventList_ = computed<string[]>(() => eventOptions.value.custom.filter(el => currentProjectData.value.event_list.some(el2 => el2.id === el.id)).map(el => el.id))
const addedCustomEventList = ref<string[]>(deepcopy(addedCustomEventList_.value))
const doSubmit = async () => {
    // 验证项目名
    try {
        await formRef.value?.validateFields()
    } catch { return }
    if (addedDefaultEventList.value.length + addedCustomEventList.value.length > user.value.eventNumLimit) {
        message.error(`事件数量超出限制，最多只能添加${user.value.eventNumLimit}个事件`)
        return
    }
    Modal.confirm({
        icon: h(ExclamationCircleOutlined),
        content: '确定要保存修改吗？（如有移除的事件，之后将无法上报）',
        okText: '确认',
        cancelText: '取消',
        maskClosable: true,
        async onOk() {
            try {
                const resp = await reqUpdateProject({
                    id,
                    name: data.value.name,
                    description: data.value.description,
                    defaultEventIdList: addedDefaultEventList.value,
                    customEventIdList: addedCustomEventList.value
                })
                if (resp.code === 200) {
                    message.success('修改成功')
                    await refreshProject()
                    // 缓存了事件页面才请求事件
                    isEventPageCached.value && await refreshEvent()
                    await refreshUser()
                    open.value = false
                } else {
                    message.error(resp.msg)
                }
            } catch {
                message.error('修改失败')
            }
        }
    })
}
watchEffect(() => {
    if (open.value) {
        data.value = deepcopy(currentProjectData.value)
        addedDefaultEventList.value = deepcopy(addedDefaultEventList_.value)
        addedCustomEventList.value = deepcopy(addedCustomEventList_.value)
    }
}, {
    flush: 'pre'
})
</script>
