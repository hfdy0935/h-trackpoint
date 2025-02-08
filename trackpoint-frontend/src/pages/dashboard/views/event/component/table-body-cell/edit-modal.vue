<template>
    <a-tooltip title="修改">
        <a-button type="primary" @click="open = true">
            <template #icon>
                <edit-outlined />
            </template>
        </a-button>
    </a-tooltip>
    <a-modal v-model:open="open" ok-text="提交" cancel-text="取消" :closable="false"
        :ok-button-props="{ style: { backgroundColor: '#00b96b' } }" title="修改事件" ref="form" @ok="doUpdate">
        <a-form :rules="eventRules" :model="data" class="outer-form" ref="form" :label-col="{ span: 4 }">
            <a-form-item label="事件名" name="name" has-feedback :colon="false">
                <a-input v-model:value.trim="data.name" allowClear></a-input>
            </a-form-item>
            <a-form-item label="描述" :colon="false">
                <a-input v-model:value.trim="data.description" allowClear></a-input>
            </a-form-item>
            <a-form-item label="修改项目" :colon="false">
                <a-transfer v-model:target-keys="data.projectIdList" :data-source="projectSelectionAll"
                    :titles="['未添加', '已添加']" :render="(item: ISelectItem) => item.name" @change="" @selectChange=""
                    @scroll="" />
            </a-form-item>
            <a-divider />
            <a-form-item label="修改参数" :colon="false">
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
import { computed, h, ref, useTemplateRef, watchEffect } from 'vue';
import { eventParamsTypeOptions, eventRules } from './data';
import { reqUpdateEvent } from '@/api/v1/event';
import { message, Modal, type FormInstance } from 'ant-design-vue'
import { useDashboardStore, useEventStore, useProjectStore, useUserStore } from '@/store';
import { MinusCircleOutlined, PlusOutlined, EditOutlined, ExclamationCircleOutlined } from '@ant-design/icons-vue'
import { storeToRefs } from 'pinia';
import type { IEvent, ReqUpdateEvent } from '@/type/event';
import { deepcopy } from '@/util/common';
//  按照数量排序有点问题、分页总数量也有问题
const { id } = defineProps<{
    /**
     * 要修改的事件id
     */
    id: string
}>()
/**
 * 选择器类型
 */
interface ISelectItem {
    key: IEvent['id']
    name: IEvent['name']
}
const { refresh: refreshUser } = useUserStore()
const { customData } = storeToRefs(useEventStore())
const { refresh: refreshEvent } = useEventStore()
const { isProjectPageCached } = storeToRefs(useDashboardStore())
const { refresh: refreshProject } = useProjectStore()

// 当前事件
const currentEvent = computed<IEvent>(() => customData.value.records.find(el => el.id === id)!)
// 初始化表单信息
const initFormData = computed<ReqUpdateEvent>(() => {
    return {
        id: currentEvent.value.id,
        name: currentEvent.value.name,
        description: currentEvent.value.description,
        paramList: currentEvent.value.param_list.map(el => ({ name: el.name, description: el.description, type: el.type })),
        projectIdList: currentEvent.value.project_list.map(item => item.id)
    }
})
const data = ref<ReqUpdateEvent>(deepcopy(initFormData.value))

// 项目选项
const { projectOptions } = storeToRefs(useEventStore())
const projectSelectionAll = computed(() => {
    return projectOptions.value.map(el => ({
        key: el.id,
        name: el.name
    }))
})
const open = ref(false)
/**
 * 表单ref
 */
const formRef = useTemplateRef<FormInstance>('form')

watchEffect(() => {
    if (open.value) {
        data.value = deepcopy(initFormData.value)
    }
}, {
    flush: 'pre'
})

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
const doUpdate = async () => {
    try {
        await formRef.value!.validateFields()
        await validateParamNameList()
    } catch { return }
    Modal.confirm({
        icon: h(ExclamationCircleOutlined),
        content: '确定要保存修改吗？（移除的项目之后将无法上报该事件）',
        okText: '确认',
        cancelText: '取消',
        maskClosable: true,
        async onOk() {
            try {
                const resp = await reqUpdateEvent(data.value)
                if (resp.code === 200) {
                    refreshEvent()
                    isProjectPageCached.value && await refreshProject()
                    await refreshUser()
                    message.success('修改成功')
                    open.value = false
                } else {
                    message.error(resp.msg)

                }
            } catch {
                message.error('修改失败，请检查参数或重试或联系管理员')
            }
        }
    })

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