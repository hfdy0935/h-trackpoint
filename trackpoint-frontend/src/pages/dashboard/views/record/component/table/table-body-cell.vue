<template>
    <template v-if="column.key === TableColumnIndexKey">
        {{ (query.page.pageNum - 1) * query.page.pageSize + index + 1 }}
    </template>
    <div v-else-if="column.key === TableColumnOperationKey" class="operation">
        <a-tooltip title="设备详情">
            <a-button type="primary" @click="openClientModal">
                <template #icon>
                    <desktop-outlined />
                </template>
            </a-button>
        </a-tooltip>
        <a-tooltip title="参数详情">
            <a-button type="primary" @click="openParamsModal" style="margin:5px">
                <template #icon>
                    <book-outlined />
                </template>
            </a-button>
        </a-tooltip>
        <a-tooltip title="删除">
            <a-popconfirm title="确认要删除该上报记录吗？" @confirm="doDelete(record.id)">
                <a-button type="primary" danger>
                    <template #icon>
                        <delete-outlined />
                    </template>
                </a-button>
            </a-popconfirm>
        </a-tooltip>
    </div>
    <template v-else>
        {{ text }}
    </template>
    <a-modal v-model:open="isModalShow" :footer="null" :closable="false"
        :title="modalType === 'client' ? '上报设备' : '上报参数'">
        <a-table :columns :data-source="modalType === 'client' ? clientInfo : paramsInfo" :pagination="false">
        </a-table>
    </a-modal>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { TableColumnIndexKey, TableColumnOperationKey } from './data';
import { useRecordStore } from '@/store';
import { DeleteOutlined, BookOutlined, DesktopOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import { reqDeleteRecord } from '@/api/v1/record';
import { computed, ref } from 'vue';
import { formateLngLat } from '@/util/format';


const { text, record, index } = defineProps<{
    text: any
    record: any
    index: any
    column: any
}>()
const { query } = storeToRefs(useRecordStore())
const { refresh } = useRecordStore()

const doDelete = async (id: string) => {
    try {
        const resp = await reqDeleteRecord(id)
        if (resp.code === 200) {
            message.success('删除成功')
            await refresh()
        } else {
            message.error(resp.msg)
        }
    } catch {
        message.error('删除失败')
    }
}

// 详情对话框
const isModalShow = ref(false)
const modalType = ref<'client' | 'params'>('client')
const columns = computed(() => [
    {
        title: modalType.value === 'client' ? '设备' : '参数',
        dataIndex: 'name',
        key: 'name',
        align: 'center'
    },
    {
        title: '值',
        dataIndex: 'value',
        key: 'value',
        align: 'center'
    },
])
// 详情对话框显示的设备信息
const clientInfo = computed(() => [
    {
        name: '操作系统',
        value: `${record.client.os} ${record.client.os_version}`,
    },
    {
        name: '浏览器',
        value: `${record.client.browser} ${record.client.browser_version}`,
    },
    {
        name: '设备类型',
        value: record.client.device
    },
    {
        name: '位置',
        value: formateLngLat(record.client.lng, record.client.lat)
    }
])
// 参数信息
const paramsInfo = computed(() => Object.entries(record.params).map(([name, value]) => ({
    name, value: typeof value === 'string' ? value : JSON.stringify(value)
})))
const openClientModal = () => {
    modalType.value = 'client'
    isModalShow.value = true
}
const openParamsModal = () => {
    modalType.value = 'params'
    isModalShow.value = true
}
</script>


<style scoped>
.operation {
    min-width: 120px;
}
</style>