<template>
    <a-tooltip title="参数详情">
        <a-button type="primary" class="btn edit-btn" @click="open = true">
            <template #icon>
                <book-outlined />
            </template>
        </a-button>
    </a-tooltip>
    <a-modal v-model:open="open" :closable="false" centered :footer="null" destroy-on-close>
        <a-table :columns :dataSource :pagination="false">
            <template #emptyText>
                暂无参数
            </template>
        </a-table>
    </a-modal>
</template>

<script setup lang="ts">
import { BookOutlined } from '@ant-design/icons-vue'
import { computed, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useEventStore } from '@/store';
import type { IBindParams } from '@/type/event';

const { id } = defineProps<{
    id: string
}>()
const open = ref(false)
const { defaultData } = storeToRefs(useEventStore())
const dataSource = computed<IBindParams[]>(() => defaultData.value.records.find(el => el.id === id)!.param_list)


const columns = [
    {
        title: '参数名',
        dataIndex: 'name',
        key: 'name',
    },
    {
        title: '参数描述',
        dataIndex: 'description',
        key: 'description',
    },
    {
        title: '参数类型',
        dataIndex: 'type',
        key: 'type',
    },
].map(i => ({ ...i, align: 'center' }))
</script>
