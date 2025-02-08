<template>
    <a-form :rules :model="data" class="form" ref="form" :label-col="{ span: 4 }" :wrapper-col="{ span: 20 }">
        <a-form-item label=" 邮箱" name="email" has-feedback :colon="false">
            <a-input placeholder="输入邮箱" v-model:value="data.email" allowClear>
                <template #prefix>
                    <mail-outlined style="margin-right: 20px;" />
                </template>
            </a-input>
        </a-form-item>
        <email-code-fom-item v-model="data.code" :verifyEmail :email="data.email" />
        <a-form-item label="昵称" name="nickname" has-feedback :colon="false">
            <a-input placeholder="输入昵称" v-model:value="data.nickname" autocomplete="off" allowClear>
                <template #prefix>
                    <user-outlined style="margin-right: 20px;" />
                </template>
            </a-input>
        </a-form-item>
        <a-form-item label="密码" name="password" has-feedback :colon="false">
            <a-input-password placeholder="输入密码" v-model:value="data.password" type="password" autocomplete="off"
                allowClear>
                <template #prefix>
                    <lock-outlined style="margin-right: 20px;" />
                </template>
            </a-input-password>
        </a-form-item>
        <a-button class="item" @click="formRef!.resetFields()">重置</a-button>
        <a-button class="item" type="primary" @click="doRegister">注册</a-button>
    </a-form>
</template>

<script setup lang="ts">
import { message, type FormInstance } from 'ant-design-vue'
import type { ReqRegister } from '@/type/user';
import { MailOutlined, LockOutlined, UserOutlined } from '@ant-design/icons-vue';
import { ref, useTemplateRef } from 'vue';
import { RegisterRules as rules } from './validate';
import { reqRegister } from '@/api/v1/user';
import { useUserStore } from '@/store';
import emailCodeFomItem from './email-code-fom-item.vue';
import { goToDashBoard } from '../../../../../util/goto';


const store = useUserStore()
const formRef = useTemplateRef<FormInstance>('form')
const data = ref<ReqRegister>({} as ReqRegister)
const spinning = defineModel<boolean>('spinning')


const verifyEmail = () => formRef.value!.validateFields(['email'])

const doRegister = async () => {
    try {
        await formRef.value?.validateFields()
    } catch {
        return
    }
    spinning.value = true
    reqRegister(data.value).then(resp => {
        if (resp.code === 200) {
            store.token = resp.data.token
            message.success('注册成功，即将跳转')
            goToDashBoard(1200)
        } else {
            message.error(resp.msg)
        }
    }).catch(() => {
        message.error('注册失败')
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