<template>
    <a-form ref="form" :rules :model="data" class="form">
        <a-form-item label="原密码" name="oriPassword" autocomplete="off">
            <a-input-password allow-clear v-model:value="data.oriPassword"></a-input-password>
        </a-form-item>
        <a-form-item label="新密码" name="newPassword" autocomplete="off">
            <a-input-password allow-clear v-model:value="data.newPassword"></a-input-password>
        </a-form-item>
        <div class="btn">
            <a-button @click="formRef!.resetFields()">重置</a-button>
            <a-button type="primary" @click="doUpdate">提交</a-button>
        </div>
    </a-form>
</template>

<script setup lang="ts">
import type { ReqUpdatePasswordByOri } from '@/type/user';
import { ref, useTemplateRef } from 'vue';
import { checkpassword } from './validte'
import { message, type FormInstance } from 'ant-design-vue'
import type { Rule } from "ant-design-vue/es/form";
import { reqUpdatePasswordByOri } from '@/api/v1/user';
import { useUserStore } from '@/store';


const { logout } = useUserStore()
const formRef = useTemplateRef<FormInstance>('form')
const data = ref<ReqUpdatePasswordByOri>({} as ReqUpdatePasswordByOri)

const validateNew = (_rule: Rule, value: string) => {
    if (value === data.value.oriPassword) {
        return Promise.reject(new Error('新密码不能与原密码相同'))
    }
    return Promise.resolve()
}
const rules: Record<string, Rule[]> =
{
    oriPassword: [{ required: true, validator: checkpassword, trigger: 'change' }],
    newPassword: [{ required: true, validator: validateNew, trigger: 'change' }]
}


const doUpdate = async () => {
    try {
        await formRef.value?.validateFields()
    } catch {
        return
    }
    reqUpdatePasswordByOri({ ...data.value }).then((resp) => {
        if (resp.code === 200) {
            message.success('修改成功，请重新登录')
            logout(false)
        } else {
            message.error(resp.msg)
        }
    }).catch(() => {
        message.error('修改失败')
    })
}
</script>

<style scoped>
.form {
    display: flex;
    flex-direction: column;
    padding: 20px 0;

    .btn {
        display: flex;
        justify-content: space-evenly;
    }
}
</style>