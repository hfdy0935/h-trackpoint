<template>
    <template v-if="column.key === TableColumnIndexKey">
        {{ (query.page.pageNum - 1) * query.page.pageSize + index + 1 }}
    </template>
    <div v-else-if="column.key === TableColumnOperationKey" class="operation">
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
        <a-tooltip title="删除">
            <a-popconfirm title="会删除该项目所有已上报的记录，且该项目的所有上报请求都会失败！" @confirm="doDelete(record.id)">
                <a-button type="primary" danger class="btn">
                    <template #icon>
                        <delete-outlined />
                    </template>
                </a-button>
            </a-popconfirm>
        </a-tooltip>
    </div>
    <template v-else-if="column.dataIndex === 'status'">
        <a-tag :color="record.status === StatusEnum.DISABLED ? '#ff3333' : '#00b96b'">
            {{ text === StatusEnum.DISABLED ? '停用' : '正常' }}
        </a-tag>
    </template>
    <template v-else-if="column.dataIndex === TableColumnEventNumDataIndex">
        <a-tooltip :title="`正常事件${normalNum}个，停用事件${disabledNum}个，总事件${normalNum + disabledNum}个`">
            <div class="event-num">
                <span style="color:#00b96b">{{ normalNum }}</span> / <span style="color:#ff3333">{{ disabledNum
                    }}</span> /
                {{
                    normalNum + disabledNum
                }}
            </div>
        </a-tooltip>
    </template>
    <template v-else>
        {{ text }}
        <copy-outlined v-if="column.dataIndex === 'id'" class="icon" @click="copy" />
    </template>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { TableColumnEventNumDataIndex, TableColumnIndexKey, TableColumnOperationKey } from '../../data';
import { useDashboardStore, useEventStore, useProjectStore, useUserStore } from '@/store';
import { DeleteOutlined, CopyOutlined, ArrowUpOutlined, ArrowDownOutlined, ExclamationCircleOutlined } from '@ant-design/icons-vue'
import { reqDeleteProject, reqUpdateProjectStatus } from '@/api/v1/project';
import { message, Modal } from 'ant-design-vue'
import EditModal from './edit-modal.vue';
import { copyToClipboard } from '@/util/common';
import { StatusEnum } from '@/enum';
import { computed, h } from 'vue';


const { text, record, index } = defineProps<{
    text: any
    record: any
    index: any
    column: any
}>()

const { refresh: refreshUser } = useUserStore()
const { refresh: refreshProject } = useProjectStore()
const { refresh: refreshEvent } = useEventStore()
const { query, data } = storeToRefs(useProjectStore())
const { isEventPageCached } = storeToRefs(useDashboardStore())
// 事件数量
const normalNum = computed(() => data.value.records[index].event_list.filter(d => d.status ===
    StatusEnum.NORMAL).length)
const disabledNum = computed(() => data.value.records[index].event_list.filter(d => d.status ===
    StatusEnum.DISABLED).length)

const reqUpdateStatus = async () => {
    const op = record.status === StatusEnum.DISABLED ? '启用' : '停用'
    try {
        const resp = await reqUpdateProjectStatus({
            id: record.id,
            status: record.status === StatusEnum.DISABLED ? StatusEnum.NORMAL : StatusEnum.DISABLED
        })
        if (resp.code === 200) {
            isEventPageCached.value && await refreshEvent()
            message.success(`${op}成功`)
            await refreshProject()
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
        // 停用需要确认
        Modal.confirm({
            icon: h(ExclamationCircleOutlined),
            content: '停用之后，该项目的所有上报请求都会失败！',
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
const doDelete = async (id: string) => {
    try {
        const resp = await reqDeleteProject(id)
        if (resp.code === 200) {
            message.success('删除成功')
            await refreshProject()
            await refreshUser()
            isEventPageCached.value && await refreshEvent()
        } else {
            message.error(resp.msg)
        }
    } catch {
        message.error('删除失败')
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
    margin: 6px;
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