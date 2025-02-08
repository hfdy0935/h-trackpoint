<template>
    <a-form :rules :model="data" class="form" ref="form" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
        <a-form-item label="邮箱" name="email" has-feedback :colon="false">
            <a-input placeholder="输入邮箱" v-model:value="data.email" allowClear>
                <template #prefix>
                    <mail-outlined style="margin-right: 20px;" />
                </template>
            </a-input>
        </a-form-item>
        <email-code-fom-item v-model="data.code" :verifyEmail :email="data.email" />
        <a-form-item label="新密码" name="password" has-feedback :colon="false">
            <a-input-password placeholder="输入新密码" v-model:value="data.password" type="password" autocomplete="off"
                allowClear>
                <template #prefix>
                    <lock-outlined style="margin-right: 20px;" />
                </template>
            </a-input-password>
        </a-form-item>
        <a-button class="item" @click="formRef!.resetFields()">重置</a-button>
        <a-button class="item" type="primary" @click="doUpdate">提交</a-button>
    </a-form>
</template>

<script setup lang="ts">
import { message, type FormInstance } from 'ant-design-vue'
import type { ReqUpdatePasswordByEmailCode } from '@/type/user';
import { MailOutlined, LockOutlined, SecurityScanOutlined } from '@ant-design/icons-vue';
import { ref, useTemplateRef } from 'vue';
import { UploadPasswordRules as rules } from './validate';
import { reqUpdatePasswordByEmailCode } from '@/api/v1/user';
import emailCodeFomItem from './email-code-fom-item.vue';

const formRef = useTemplateRef<FormInstance>('form')
const verifyEmail = () => formRef.value!.validateFields(['email'])
const data = ref<ReqUpdatePasswordByEmailCode>({} as ReqUpdatePasswordByEmailCode)
const spinning = defineModel<boolean>('spinning')
const doUpdate = async () => {
    try {
        await formRef.value?.validateFields()
    } catch {
        return
    }
    spinning.value = true
    reqUpdatePasswordByEmailCode(data.value).then(resp => {
        if (resp.code === 200) {
            message.success('修改成功')
            formRef.value?.resetFields()
        } else {
            message.error(resp.msg)
        }
    }).catch(() => {
        message.error('修改失败')
    }).finally(() => {
        spinning.value = false
    })
}
</script>

<style scoped>
.form {
    .item {
        margin: 10px 20px;
    }
}
</style>