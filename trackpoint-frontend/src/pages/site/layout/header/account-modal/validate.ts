
import type { Rule } from 'ant-design-vue/es/form';

const checkEmail = async (_rule: Rule, value: string) => {
    if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(value?.trim())) {
        return Promise.reject('邮箱格式不正确');
    }
    return Promise.resolve()
};
const checkpassword = async (_rule: Rule, value: string) => {
    if (!value) return Promise.reject('密码必须由6-12位的数字、英文大小写字母、@、#、_和$组成');
    if (!/^[0-9a-zA-Z$#@_]{6,12}$/.test(value.trim())) {
        return Promise.reject('密码必须由6-12位的数字、英文大小写字母、@、#、_和$组成');
    }
    return Promise.resolve()
};


export const LoginRules: Record<string, Rule[]> = {
    email: [
        { required: true, validator: checkEmail, trigger: 'change' },
    ],
    password: [{ required: true, validator: checkpassword, trigger: 'change' }]
};

export const RegisterRules = {
    ...LoginRules,
    code: [
        {
            required: true,
            message: '验证码不能为空',
            trigger: 'change'
        }
    ]
}
export const UploadPasswordRules = RegisterRules