import type { Rule } from "ant-design-vue/es/form";

export const checkpassword = async (_rule: Rule, value: string) => {
    if (!value) return Promise.reject('密码必须由6-12位的数字、英文大小写字母、@、#、_和$组成');
    if (!/^[0-9a-zA-Z$#@_]{6,12}$/.test(value.trim())) {
        return Promise.reject('密码必须由6-12位的数字、英文大小写字母、@、#、_和$组成');
    }
    return Promise.resolve()
};

