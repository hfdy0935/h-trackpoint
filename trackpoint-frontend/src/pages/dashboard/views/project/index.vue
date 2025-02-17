<template>
    <table-layout>
        <template #header>
            <a-row style="width: 100%;align-items: center;margin-bottom: 6px;">
                <a-col style="margin:5px 0">
                    <a-input class="input-search" v-model:value.trim="query.keyword" allow-clear
                        placeholder="搜索项目名或描述"></a-input>
                </a-col>
                <a-col>
                    <create-project-modal />
                </a-col>
            </a-row>
        </template>
        <a-table :data-source="data.records" :columns="getColumns(query.status)" class="table" :pagination="{
            total: data.total,
            simple: true
        }" @change="pageChange">
            <template #bodyCell="{ text, record, index, column }">
                <table-body-cell :text :record :index :column />
            </template>
            <template #customFilterDropdown="data">
                <custom-filter-dropdown :data ref="filter" />
            </template>
            <template #customFilterIcon="{ column: { dataIndex } }">
                <filter-outlined v-if="dataIndex === 'status'" />
                <calendar-outlined v-else-if="dataIndex === 'create_time'" @click="clickFilterIcon(dataIndex)"
                    :style="{ color: query.createTimePeriod?.start || query.createTimePeriod?.end ? '#1677FF' : '' }" />
                <calendar-outlined v-else-if="dataIndex === 'update_time'" @click="clickFilterIcon(dataIndex)"
                    :style="{ color: query.updateTimePeriod?.start || query.updateTimePeriod?.end ? '#1677FF' : '' }" />
            </template>
        </a-table>
    </table-layout>
</template>

<script setup lang="ts">
import { watch, watchEffect } from 'vue'
import { getColumns } from './data';
import { SideMenuNameEnum } from '@/enum';
import tableBodyCell from './component/table-body-cell/index.vue';
import { storeToRefs } from 'pinia';
import { useProjectStore } from '@/store';
import CustomFilterDropdown from './component/curtom-filter-dropdown.vue'
import CreateProjectModal from './component/create-project-modal/index.vue';
import TableLayout from '../../component/table-layout.vue';
import { CalendarOutlined, RedoOutlined, FilterOutlined } from '@ant-design/icons-vue'
import type { FilterProjectField } from '@/store/module/project';
import { message } from 'ant-design-vue'
defineOptions({
    name: SideMenuNameEnum.Project
})

const { data, query, filterProjectField } = storeToRefs(useProjectStore())
const { refresh } = useProjectStore()
watch(query, () => {
    refresh()
}, {
    immediate: true, deep: true
})

// 点击自定义过滤器图标
const clickFilterIcon = (dataIndex: FilterProjectField) => {
    filterProjectField.value = dataIndex
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
const clickRefresh = () => {
    refresh().then(() => {
        message.success('刷新成功')
    })
}
</script>

<style scoped>
.table {
    width: 100%;
}

.input-search {
    width: 160px;
}

.refresh {
    margin-left: 10px;
    font-size: 16px;
}
</style>