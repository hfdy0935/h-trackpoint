import { StatusEnum } from "@/enum"
import type { ReqEventList } from "@/type/event"

export const TableColumnIndexKey = 'index'
export const TableColumnOperationKey = 'operation'
export const TableColumnProjectNumDataIndex = 'project_num'
/**
 * 事件列表的列配置
 */
export const getColumns = (query: ReqEventList) => [
    {
        title: '序号',
        key: TableColumnIndexKey,
        filteredValue: [],
    },
    {
        title: '事件名',
        dataIndex: 'name',
        key: 'name',
        filteredValue: [],
    },
    {
        title: '描述',
        dataIndex: 'description',
        key: 'description',
        filteredValue: [],
    },
    {
        title: '状态',
        dataIndex: 'status',
        key: 'status',
        filters: [
            {
                text: '正常',
                value: StatusEnum.NORMAL
            },
            {
                text: '停用',
                value: StatusEnum.DISABLED
            }
        ],
        filteredValue: [StatusEnum.NORMAL, StatusEnum.DISABLED],
        defaultFilteredValue: query.status
    },
    ...query.type === 'default' ? [] : [
        {
            title: '创建时间',
            dataIndex: 'create_time',
            key: 'create_time',
            sorter: true,
            customFilterDropdown: true,
            filteredValue: [],
        },
        {
            title: '修改时间',
            dataIndex: 'update_time',
            key: 'update_time',
            sorter: true,
            customFilterDropdown: true,
            filteredValue: [],
        }
    ],
    {
        title: '关联项目数量',
        dataIndex: TableColumnProjectNumDataIndex,
        key: 'project_num',
        sorter: true,
        filteredValue: [],
    },
    {
        title: '参数数量',
        dataIndex: 'param_num',
        key: 'param_num',
        sorter: true,
        filteredValue: [],
    },
    {
        title: '操作',
        key: TableColumnOperationKey,
        fixed: 'right',
        filteredValue: [],
    },
].map(i => ({ ...i, align: 'center' }))