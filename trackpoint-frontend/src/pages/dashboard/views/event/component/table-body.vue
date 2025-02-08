<template>
    <a-table :data-source="data.records" :columns="getColumns(query)" class="table" :pagination="{
        total: data.total,
        simple: true
    }" @change="pageChange">
        <template #bodyCell="{ text, record, index, column }">
            <table-body-cell :text :record :index :column />
        </template>
        <template #customFilterDropdown="data">
            <custom-filter-dropdown :data ref="filter" />
        </template>
        <template #customFilterIcon="{ column }">
            <filter-outlined v-if="column.dataIndex === 'status'" />
            <calendar-outlined v-else-if="column.dataIndex === 'create_time'" @click="clickFilterIcon(column.dataIndex)"
                :style="{ color: query.createTimePeriod?.start || query.createTimePeriod?.end ? '#1677FF' : '' }" />
            <calendar-outlined v-else-if="column.dataIndex === 'update_time'" @click="clickFilterIcon(column.dataIndex)"
                :style="{ color: query.updateTimePeriod?.start || query.updateTimePeriod?.end ? '#1677FF' : '' }" />
        </template>
    </a-table>
</template>

<script setup lang="ts">
import { computed, watchEffect } from 'vue'
import { SideMenuNameEnum } from '@/enum';
import { storeToRefs } from 'pinia';
import { useEventStore } from '@/store';
import { CalendarOutlined, FilterOutlined } from '@ant-design/icons-vue'
import { message } from 'ant-design-vue'
import type { FilterEventField } from '@/store/module/event';
import type { RespEventList } from '@/type/event';
import TableBodyCell from './table-body-cell/index.vue'
import CustomFilterDropdown from './curtom-filter-dropdown.vue'
import { getColumns } from './data'
defineOptions({
    name: SideMenuNameEnum.Event
})


const { defaultData, customData, query, filterEventField } = storeToRefs(useEventStore())
const data = computed<RespEventList>(() => query.value.type === 'default' ? defaultData.value : customData.value)
// 点击自定义过滤器图标
const clickFilterIcon = (dataIndex: FilterEventField) => {
    filterEventField.value = dataIndex
}

const pageChange = (pagination: any, filters: any, sorter: any) => {
    query.value.page = {
        pageNum: pagination.current,
        pageSize: pagination.pageSize
    }
    query.value.orderBy = [{
        field: sorter.field,
        order: sorter.order
    }]
    query.value.status = filters.status || []
}
</script>

<style scoped>
.table {
    width: 100%;
}

.input-search {
    width: 200px;
}

.refresh {
    margin-left: 10px;
    font-size: 16px;
}
</style>