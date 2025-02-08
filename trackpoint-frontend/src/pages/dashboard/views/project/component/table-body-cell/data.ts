import type { Rule } from 'ant-design-vue/es/form';

export const rules: Record<string, Rule[]> = {
    name: [
        { required: true, message: '项目名不能为空', trigger: 'change' },
    ],
};