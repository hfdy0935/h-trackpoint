<template>
    <a-button class="btn" type="primary" @click="open = true">创建项目</a-button>
    <a-modal v-model:open="open" ok-text="创建" cancel-text="取消" :closable="false"
        :ok-button-props="{ style: { backgroundColor: '#00b96b' } }" title="创建项目" ref="form" @ok="doCreate">
        <a-form :rules :model="data" class="form" ref="form" :label-col="{ span: 6 }">
            <a-form-item label="项目名" name="name" has-feedback :colon="false">
                <a-input v-model:value.trim="data.name" allowClear></a-input>
            </a-form-item>
            <a-form-item label="项目描述" :colon="false">
                <a-input v-model:value.trim="data.description" allowClear></a-input>
            </a-form-item>
            <a-form-item label="添加默认事件" :colon="false">
                <a-badge-ribbon title="查看事件管理获取更多详情">
                    <a-select v-model:value="data.defaultEventIdList" mode="multiple" style="width: 100%"
                        :options="selectOptionsDefault" allowClear placeholder="选择需要的默认事件">
                    </a-select>
                    <template #text>
                        <span style="font-weight: bolder;">?</span>
                    </template>
                </a-badge-ribbon>
            </a-form-item>
            <a-form-item label="添加自定义事件" :colon="false">
                <a-badge-ribbon title="查看事件管理获取更多详情">
                    <a-select v-model:value="data.customEventIdList" mode="multiple" style="width: 100%"
                        :options="selectOptionsCustom" allowClear placeholder="选择需要的自定义事件">
                    </a-select>
                    <template #text>
                        <span style="font-weight: bolder;">?</span>
                    </template>
                </a-badge-ribbon>
            </a-form-item>
        </a-form>
    </a-modal>
    <a-modal v-model:open="resModalShow" :footer="null" :closable="false" @cancel="confirmBeforeDestroy">
        <div class="create-res-info">
            <div class="key"><idcard-outlined />&emsp;id</div> <code>{{ createResp.id }} &emsp;<copy-outlined class="icon"
                @click="copy(createResp.id)" /></code>
        </div>
        <div class="create-res-info">
            <div class="key"><lock-outlined />&emsp;key</div> <code>{{ createResp.key }} &emsp;<copy-outlined class="icon"
                @click="copy(createResp.key)" /></code>
        </div>
        <template #title>
            请保存好你的key，<span style="color:red;font-weight: bolder;">只显示一次</span>
        </template>
    </a-modal>
</template>

<script setup lang="ts">
import type { ReqCreateProject, RespCreateProject } from '@/type/project';
import { computed, ref, useTemplateRef, watchEffect, h } from 'vue';
import { getDefaultData, rules } from './data';
import { message, Modal, type FormInstance } from 'ant-design-vue'
import { reqCreateProject } from '@/api/v1/project';
import { useDashboardStore, useEventStore, useProjectStore, useUserStore } from '@/store';
import { LockOutlined, IdcardOutlined, CopyOutlined, ExclamationCircleOutlined } from '@ant-design/icons-vue'
import { copyToClipboard } from '@/util/common';
import { storeToRefs } from 'pinia';


const { user } = storeToRefs(useUserStore())
const { refresh: refreshUser } = useUserStore()
const { refresh: refreshProject } = useProjectStore()
const { refresh: refreshEvent } = useEventStore()
const { isEventPageCached } = storeToRefs(useDashboardStore())
// 创建项目的表单数据
const data = ref<ReqCreateProject>(getDefaultData())
// 事件选项
const { eventOptions } = storeToRefs(useProjectStore())
/**
 * 默认事件列表
 */
const selectOptionsDefault = computed(() => eventOptions.value.default.map(d => ({ value: d.name })))
/**
 * 自定义事件列表
 */
const selectOptionsCustom = computed(() => eventOptions.value.custom.map(d => ({ value: d.name })))
const open = ref(false)
/**
 * 表单ref
 */
const formRef = useTemplateRef<FormInstance>('form')
// 创建结果
const createResp = ref<RespCreateProject>({ id: '', key: '' })
// 显示创建成功结果的对话框
const resModalShow = ref(false)
/**
 * 复制到剪贴板
 * @param s 
 */
const copy = async (s: string) => {
    copyToClipboard(s).then(() => {
        message.success('成功复制到剪切板')
    }).catch(() => {
        message.error('复制失败，请手动复制')
    })
}

/**
 * 创建成功后，关闭之前确认保存了key
 */
const confirmBeforeDestroy = () => {
    Modal.confirm({
        icon: h(ExclamationCircleOutlined),
        content: '确定保存好项目的key了吗？，仅显示一次',
        okText: '确认',
        cancelText: '取消',
        onOk: () => {
            Modal.destroyAll()
            createResp.value = { id: '', key: '' }
        },
        onCancel() {
            resModalShow.value = true
        }
    })
}
/**
 * 提交
 */
const doCreate = async () => {
    try {
        await formRef.value!.validateFields()
    } catch { return }
    if (data.value.defaultEventIdList.length + data.value.customEventIdList.length > user.value.eventNumLimit) {
        message.error(`事件数量超出限制，最多只能添加${user.value.eventNumLimit}个事件`)
        return
    }
    try {
        // data中存的是name，找到id传给后端
        const defaultEventIdList = data.value.defaultEventIdList.map(d => eventOptions.value.default.find(i => i.name === d)!.id)
        const customEventIdList = data.value.customEventIdList.map(d => eventOptions.value.custom.find(i => i.name === d)!.id)
        const resp = await reqCreateProject({
            ...data.value,
            defaultEventIdList,
            customEventIdList
        })
        if (resp.code === 200) {
            createResp.value = resp.data
            await refreshProject()
            await refreshUser()
            // 缓存了事件页面才请求事件
            isEventPageCached.value && await refreshEvent()
            message.success('创建成功')
            open.value = false
            resModalShow.value = true
            data.value = getDefaultData()
        } else {
            message.error(resp.msg)

        }
    } catch {
        message.error('创建失败，请重试或联系管理员')
    }
}
</script>

<style scoped>
.btn {
    margin-left: 10px;
    background-color: var(--green-btn);

    &:hover {
        background-color: var(--green-btn);
    }
}

.create-res-info {
    display: flex;
    margin: 40px 20px;

    .key {
        width: 80px;
    }

    .icon:hover {
        color: var(--green-btn)
    }
}
</style>