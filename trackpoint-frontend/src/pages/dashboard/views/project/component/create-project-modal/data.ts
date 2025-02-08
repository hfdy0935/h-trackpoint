import type { ReqCreateProject } from '@/type/project';
import type { Rule } from 'ant-design-vue/es/form';



export const rules: Record<string, Rule[]> = {
    name: [
        { required: true, message: '项目名不能为空', trigger: 'change' },
    ],
};


const DEFAULT_DATA: ReqCreateProject = {
    name: '',
    description: '',
    defaultEventIdList: [],
    customEventIdList: []
}

export function getDefaultData() {
    return JSON.parse(JSON.stringify(DEFAULT_DATA))
}