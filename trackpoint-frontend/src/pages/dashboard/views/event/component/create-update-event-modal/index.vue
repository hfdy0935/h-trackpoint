<template>
    <a-button class="create-btn" type="primary" @click="open = true">创建事件</a-button>
    <a-modal v-model:open="open" ok-text="创建" cancel-text="取消" :closable="false"
        :ok-button-props="{ style: { backgroundColor: '#00b96b' } }" title="创建事件" ref="form" @ok="doCreate">
        <a-form :rules="eventRules" :model="data" class="outer-form" ref="form" :label-col="{ span: 4 }">
            <a-form-item label="事件名" name="name" has-feedback :colon="false">
                <a-input v-model:value.trim="data.name" allowClear></a-input>
            </a-form-item>
            <a-form-item label="描述" :colon="false">
                <a-input v-model:value.trim="data.description" allowClear></a-input>
            </a-form-item>
            <a-form-item label="添加到项目" :colon="false">
                <a-select v-model:value="data.projectIdList" mode="multiple" style="width: 100%"
                    :options="selectOptions" allowClear :placeholder="`要把我添加到哪些项目？`">
                </a-select>
            </a-form-item>
            <a-divider />
            <a-form-item label="添加参数" :colon="false">
                <div class="param-title">
                    <a-tooltip title="同一事件中的参数名不能重复">
                        <span>参数名</span>
                    </a-tooltip>
                    <a-tooltip title="想怎么写就怎么写">
                        <span>描述</span>
                    </a-tooltip>
                    <a-tooltip title="上传时类型不符合会失败">
                        <span>类型</span>
                    </a-tooltip>
                </div>
                <a-empty v-if="data.paramList.length === 0"></a-empty>
                <div class="event-param-form-container">
                    <a-form>
                        <a-form-item :colon="false" v-for="(param, index) in data.paramList" :key="index" :label="''">
                            <div class="event-param">
                                <a-input v-model:value="param.name" class="input" allow-clear></a-input>
                            </div>
                        </a-form-item>
                    </a-form>
                    <a-form>
                        <a-form-item :colon="false" v-for="(param, index) in data.paramList" :key="index" :label="''">
                            <div class="event-param">
                                <a-input v-model:value="param.description" class="input" allow-clear></a-input>
                            </div>
                        </a-form-item>
                    </a-form>
                    <a-form>
                        <a-form-item :colon="false" v-for="(param, index) in data.paramList" :key="param.name"
                            :label="''">
                            <div class="event-param">
                                <a-dropdown>
                                    <a type="link" style="width:56px;text-align: center;">{{
                                        param.type }}
                                    </a>
                                    <template #overlay>
                                        <a-radio-group v-model:value="param.type"
                                            style="box-shadow: 0 0 3px #999;border-radius: 4px;padding: 6px;background-color: white;">
                                            <a-radio v-for="op in eventParamsTypeOptions" :key="op" :value="op" :style="{
                                                display: 'flex',
                                                height: '30px',
                                                lineHeight: '30px',
                                            }">{{ op
                                                }}</a-radio>
                                        </a-radio-group>
                                    </template>
                                </a-dropdown>
                                <minus-circle-outlined class="minus-icon" @click=" removeParamItem(index)" />
                            </div>
                        </a-form-item>
                    </a-form>
                </div>
            </a-form-item>
            <a-form-item>
                <a-button type="dashed" @click="addParamItem">
                    <plus-outlined />
                    添加参数
                </a-button>
            </a-form-item>
        </a-form>
    </a-modal>
</template>

<script setup lang="ts">
import { computed, ref, useTemplateRef } from 'vue';
import { eventParamsTypeOptions, getBlankEventData, eventRules } from './data';
import { reqCreateEvent } from '@/api/v1/event';
import { message, type FormInstance } from 'ant-design-vue'
import { useDashboardStore, useEventStore, useProjectStore, useUserStore } from '@/store';
import { MinusCircleOutlined, PlusOutlined } from '@ant-design/icons-vue'
import { storeToRefs } from 'pinia';
import type { ReqCreateEvent } from '@/type/event';


const { refresh: refreshUser } = useUserStore()
const { refresh: refreshEvent } = useEventStore()
const { isProjectPageCached } = storeToRefs(useDashboardStore())
const { refresh: refreshProject } = useProjectStore()
// 创建项目的表单数据
const data = ref<ReqCreateEvent>(getBlankEventData())
// 项目选项
const { projectOptions } = storeToRefs(useEventStore())

/**
 * 项目选项列表
 */
const selectOptions = computed(() => projectOptions.value.map(d => ({ value: d.name })))
const open = ref(false)
/**
 * 表单ref
 */
const formRef = useTemplateRef<FormInstance>('form')

/**
 * 验证参数名
 */
const validateParamNameList = () => new Promise((res, rej) => {
    if (data.value.paramList.some(el => !el.name.trim())) {
        message.warning('参数名不能为空')
        rej()
    }
    const nameList = data.value.paramList.map(el => el.name.trim())
    if (nameList.length !== new Set(nameList).size) {
        message.warning('参数名不能重复')
        rej()
    }
    res('')
})
/**
 * 增加一项参数
 */
const addParamItem = () => {
    validateParamNameList().then(() => {
        data.value.paramList.push({
            name: '',
            description: '',
            type: 'string'
        })
    })
}
/**
 * 移除一项参数
 */
const removeParamItem = (index: number) => {
    data.value.paramList.splice(index, 1)
}
/**
 * 提交
 */
const doCreate = async () => {
    try {
        await formRef.value!.validateFields()
        await validateParamNameList()
    } catch { return }
    try {
        // data中存的是name，找到id传给后端
        const projectIdList = data.value.projectIdList.map(d => projectOptions.value.find(i => i.name === d)!.id)
        const resp = await reqCreateEvent({
            ...data.value,
            projectIdList
        })
        if (resp.code === 200) {
            refreshEvent()
            isProjectPageCached.value && await refreshProject()
            await refreshUser()
            message.success('创建成功')
            open.value = false
            data.value = getBlankEventData()
        } else {
            message.error(resp.msg)

        }
    } catch {
        message.error('创建失败，请检查参数或重试或联系管理员')
    }
}
</script>

<style scoped>
.create-btn {
    margin-top: 6px;
    background-color: var(--green-btn);

    &:hover {
        background-color: var(--green-btn);
    }
}

.outer-form {
    .param-title {
        width: 100%;
        display: flex;
        justify-content: space-evenly;
        margin-top: 6px;
        margin-bottom: 20px;
        border-left: 1px solid #777;

        span {
            cursor: auto;
            user-select: none;
            text-align: center;
        }

        :not(:last-child) {
            width: 120px;
        }

        :nth-child(3) {
            width: 56px;
        }
    }

    .event-param-form-container {
        display: flex;
        justify-content: space-around;

        .event-param {
            display: flex;
            justify-content: space-evenly;

            .input {
                width: 120px;
            }

            .minus-icon {
                transform: translateX(15px);

                &:hover {
                    color: red
                }
            }

        }
    }
}
</style>