/**
 * 参数表格列
 */
export const columns = [
    {
        title: '参数名',
        dataIndex: 'name',
        key: 'name',
    },
    {
        title: '类型',
        dataIndex: 'type',
        key: 'type',
    },
    {
        title: '描述',
        dataIndex: 'desc',
        key: 'desc',
    },
].map(el => ({ ...el, align: 'center' }))


export interface TableDataItem {
    name: string
    type: 'string' | 'number' | 'boolean' | 'array' | 'object'
    desc: string
}