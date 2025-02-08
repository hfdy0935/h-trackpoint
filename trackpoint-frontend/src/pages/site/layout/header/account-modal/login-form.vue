<template>
    <a-form :rules="LoginRules" :model="loginData" class="form" ref="form" :label-col="{ span: 4 }"
        :wrapper-col="{ span: 20 }">
        <a-form-item label="邮箱" name="email" has-feedback :colon="false">
            <a-input placeholder="输入邮箱" v-model:value.trim="loginData.email" allowClear>
                <template #prefix>
                    <mail-outlined style="margin-right: 20px;" />
                </template>
            </a-input>
        </a-form-item>
        <a-form-item label="密码" name="password" has-feedback :colon="false">
            <a-input-password placeholder="输入密码" v-model:value.trim="loginData.password" type="password"
                autocomplete="off" allowClear>
                <template #prefix>
                    <lock-outlined style="margin-right: 20px;" />
                </template>
            </a-input-password>
        </a-form-item>
        <a-button class="item" @click="formRef!.resetFields()">重置</a-button>
        <a-button class="item" type="primary" @click="doLogin">登录</a-button>
    </a-form>
</template>

<script setup lang="ts">
import { message, type FormInstance } from 'ant-design-vue'
import type { ReqLogin } from '@/type/user';
import { MailOutlined, LockOutlined } from '@ant-design/icons-vue';
import { ref, useTemplateRef } from 'vue';
import { LoginRules } from './validate';
import { reqLogin } from '@/api/v1/user';
import { useUserStore } from '@/store';
import { goToDashBoard } from '../../../../../util/goto';

const store = useUserStore()
const formRef = useTemplateRef<FormInstance>('form')
const loginData = ref<ReqLogin>({} as ReqLogin)
const spinning = defineModel<boolean>('spinning')
const doLogin = async () => {
    // 先验证字段
    try {
        await formRef.value?.validateFields()
    } catch {
        return
    }
    spinning.value = true
    reqLogin(loginData.value).then(resp => {
        if (resp.code === 200) {
            store.token = resp.data.token
            message.success('登录成功，即将跳转')
            goToDashBoard(1200)
        } else {
            message.error(resp.msg)
        }
    }).catch(() => {
        message.error('登录失败')
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