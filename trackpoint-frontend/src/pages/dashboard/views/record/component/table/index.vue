<template>
    <a-table :data-source="data.records" :columns class="table" :pagination="{
        total: data.total
    }" @change="pageChange">
        <template #bodyCell="{ text, record, index, column }">
            <table-body-cell :text :record :index :column />
        </template>
        <template #customFilterDropdown="data">
            <custom-filter-dropdown :data ref="filter" />
        </template>
        <template #customFilterIcon="{ column }">
            <calendar-outlined v-if="column.dataIndex === 'create_time'"
                :style="{ color: query.createTimePeriod?.start || query.createTimePeriod?.end ? '#1677FF' : '' }" />
        </template>
    </a-table>
</template>

<script setup lang="ts">
import { SideMenuNameEnum } from '@/enum';
import { storeToRefs } from 'pinia';
import { CalendarOutlined } from '@ant-design/icons-vue'
import TableBodyCell from './table-body-cell.vue'
import CustomFilterDropdown from './curtom-filter-dropdown.vue'
import { columns } from './data';
import { useRecordStore } from '@/store/module/record';
defineOptions({
    name: SideMenuNameEnum.Event
})

const { query, data } = storeToRefs(useRecordStore())

const pageChange = (pagination: any, filters: any, sorter: any) => {
    query.value.page = {
        pageNum: pagination.current,
        pageSize: pagination.pageSize
    }
    query.value.orderBy = [{
        field: sorter.field,
        order: sorter.order
    }]
}
</script>

<style scoped>
.table {
    width: 100%;
}
</style>