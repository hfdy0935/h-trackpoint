import type { EventParamType, ReqCreateEvent } from '@/type/event';
import type { Rule } from 'ant-design-vue/es/form';



export const eventRules: Record<string, Rule[]> = {
    name: [
        { required: true, message: '事件名不能为空', trigger: 'change' },
    ],
};


const DEFAULT_DATA: ReqCreateEvent = {
    name: '',
    description: '',
    projectIdList: [],
    paramList: []
}

export function getBlankEventData(): ReqCreateEvent {
    return JSON.parse(JSON.stringify(DEFAULT_DATA))
}

/**
 * 创建事件的参数表格
 */
export const columns = [
    {
        title: '参数名',
        dataIndex: 'name',
        key: 'name',
    },
    {
        title: '描述',
        dataIndex: 'description',
        key: 'description',
    },
    {
        title: '类型',
        dataIndex: 'type',
        key: 'type',
    },
]

/**
 * 事件参数类型选项
 */
export const eventParamsTypeOptions: EventParamType[] = ['string', 'number', 'boolean', 'array', 'object']