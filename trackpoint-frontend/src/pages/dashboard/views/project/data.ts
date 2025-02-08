import { StatusEnum } from "@/enum"

export const TableColumnIndexKey = 'index'
export const TableColumnOperationKey = 'operation'
export const TableColumnEventNumDataIndex = 'event_num'
/**
 * 项目列表的列配置
 */
export const getColumns = (defaultFilteredValue: StatusEnum[]) => {
    return [
        {
            title: '序号',
            key: TableColumnIndexKey,
            filteredValue: []
        },
        {
            title: 'id',
            dataIndex: 'id',
            key: 'id',
            filteredValue: []
        },
        {
            title: '项目名',
            dataIndex: 'name',
            key: 'name',
            filteredValue: []
        },
        {
            title: '描述',
            dataIndex: 'description',
            key: 'description',
            filteredValue: []
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
            defaultFilteredValue,
            filteredValue: defaultFilteredValue
        },
        {
            title: '创建时间',
            dataIndex: 'create_time',
            key: 'create_time',
            sorter: true,
            customFilterDropdown: true,
            filteredValue: []
        },
        {
            title: '修改时间',
            dataIndex: 'update_time',
            key: 'update_time',
            sorter: true,
            customFilterDropdown: true,
            filteredValue: []
        },
        {
            title: '关联事件数量',
            dataIndex: TableColumnEventNumDataIndex,
            key: 'event_num',
            sorter: true,
            filteredValue: []
        },
        {
            title: '操作',
            key: TableColumnOperationKey,
            fixed: 'right',
            filteredValue: []
        },
    ].map(i => ({ ...i, align: 'center' }))
}