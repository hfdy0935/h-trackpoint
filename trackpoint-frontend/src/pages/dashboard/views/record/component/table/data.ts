export const TableColumnIndexKey = 'index'
export const TableColumnOperationKey = 'operation'
export const TableColumnDetailKey = 'detail'
/**
 * 上报记录列表的列配置
 */
export const columns = [
  {
    title: '序号',
    key: TableColumnIndexKey,
    filteredValue: [],
  },
  {
    title: '上报时间',
    dataIndex: 'create_time',
    key: 'create_time',
    sorter: true,
    customFilterDropdown: true,
    filteredValue: [],
  },
  {
    title: '页面url',
    dataIndex: 'page_url',
    key: 'page_url',
    filteredValue: [],
  },
  {
    title: '操作',
    key: TableColumnOperationKey,
    fixed: 'right',
    filteredValue: [],
  },
].map((i) => ({ ...i, align: 'center' }))
