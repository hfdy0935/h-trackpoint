<template>
    <template v-if="column.key === TableColumnIndexKey">
        {{ (query.page.pageNum - 1) * query.page.pageSize + index + 1 }}
    </template>
    <div v-else-if="column.key === TableColumnOperationKey" class="operation">
        <template v-if="query.type === 'custom'">
            <a-tooltip :title="record.status === StatusEnum.DISABLED ? '点击启用' : '点击停用'">
                <a-button class="btn" @click="doUpdateStatus"
                    :style="{ color: 'white', backgroundColor: record.status === StatusEnum.DISABLED ? '#00b96b' : '#888' }">
                    <template #icon>
                        <arrow-up-outlined v-if="record.status === StatusEnum.DISABLED" />
                        <arrow-down-outlined v-else />
                    </template>
                </a-button>
            </a-tooltip>
            <edit-modal :id="record.id" />
        </template>
        <view-modal v-else :id="record.id" />
        <a-tooltip title="删除">
            <a-popconfirm title="会删除该事件所有已上报的事件记录，值会所有项目中的该事件上报请求都会失败" @confirm="doDelete(record.id)">
                <a-button type="primary" danger class="btn">
                    <template #icon>
                        <delete-outlined />
                    </template>
                </a-button>
            </a-popconfirm>
        </a-tooltip>
    </div>
    <template v-else-if="column.dataIndex === TableColumnProjectNumDataIndex">
        <a-tooltip :title="`正常项目${normalNum}个，停用项目${disabledNum}个，总项目${normalNum + disabledNum}个`">
            <div class="event-num">
                <span style="color:#00b96b">{{ normalNum }}</span> / <span style="color:#ff3333">{{ disabledNum
                    }}</span> /
                {{
                    normalNum + disabledNum
                }}
            </div>
        </a-tooltip>
    </template>
    <template v-else-if="column.dataIndex === 'status'">
        <a-tag :color="record.status === StatusEnum.DISABLED ? '#ff3333' : '#00b96b'">
            {{ text === StatusEnum.DISABLED ? '停用' : '正常' }}
        </a-tag>
    </template>
    <template v-else>
        {{ text }}
        <copy-outlined v-if="column.dataIndex === 'name'" class="icon" @click="copy" />
    </template>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { TableColumnIndexKey, TableColumnOperationKey, TableColumnProjectNumDataIndex } from '../data';
import { useDashboardStore, useEventStore, useProjectStore, useUserStore } from '@/store';
import { DeleteOutlined, CopyOutlined, ExclamationCircleOutlined, ArrowDownOutlined, ArrowUpOutlined, BookOutlined } from '@ant-design/icons-vue'
import { message, Modal } from 'ant-design-vue'
import EditModal from './edit-modal.vue';
import ViewModal from './view-modal.vue';
import { copyToClipboard } from '@/util/common';
import { computed, h } from 'vue';
import { StatusEnum } from '@/enum';
import { reqDeleteEvent, reqUpdateEventStatus } from '@/api/v1/event';


const { text, record, index } = defineProps<{
    text: any
    record: any
    index: any
    column: any
}>()

const { refresh: refreshUser } = useUserStore()
const { refresh: refreshEvent } = useEventStore()
const { query, defaultData, customData } = storeToRefs(useEventStore()) // 查询数据
const { isProjectPageCached } = storeToRefs(useDashboardStore())
const { refresh: refreshProject } = useProjectStore()
// 项目数量
const data = computed(() => query.value.type === 'default' ? defaultData.value : customData.value)
const normalNum = computed(() => data.value.records[index].project_list.filter(d => d.status ===
    StatusEnum.NORMAL).length)
const disabledNum = computed(() => data.value.records[index].project_list.filter(d => d.status ===
    StatusEnum.DISABLED).length)
const doDelete = async (id: string) => {
    try {
        const resp = await reqDeleteEvent(id)
        if (resp.code === 200) {
            message.success('删除成功')
            await refreshEvent()
            isProjectPageCached && await refreshProject()
            await refreshUser()
        } else {
            message.error(resp.msg)
        }
    } catch {
        message.error('删除失败')
    }
}


const reqUpdateStatus = async () => {
    const op = record.status === StatusEnum.DISABLED ? '启用' : '停用'
    try {
        const resp = await reqUpdateEventStatus({
            id: record.id,
            status: record.status === StatusEnum.DISABLED ? StatusEnum.NORMAL : StatusEnum.DISABLED
        })
        if (resp.code === 200) {
            message.success(`${op}成功`)
            isProjectPageCached.value && await refreshProject()
            await refreshEvent()
            await refreshUser()
        } else {
            message.error(resp.msg)
        }
    } catch {
        message.error(`${op}失败`)
    }
}

const doUpdateStatus = async () => {
    if (record.status === StatusEnum.DISABLED) {
        await reqUpdateStatus()
    }
    else {
        Modal.confirm({
            icon: h(ExclamationCircleOutlined),
            content: '停用之后，该事件的上报请求将会失败',
            okText: '我确定了',
            cancelText: '我再想想',
            maskClosable: true,
            async onOk() {
                await reqUpdateStatus()
                Modal.destroyAll()
            },
            onCancel() {
                Modal.destroyAll()
            }
        })
    }
}
const copy = async () => {
    copyToClipboard(text).then(() => {
        message.success('成功复制到剪切板')
    }).catch(() => {
        message.error('复制失败，请手动复制')
    })
}
</script>

<style scoped>
.operation {
    min-width: 120px;
}

.btn {
    margin: 5px;
}

.event-num {
    font-size: medium;
}

.icon {
    &:hover {
        color: var(--green-btn)
    }
}
</style>