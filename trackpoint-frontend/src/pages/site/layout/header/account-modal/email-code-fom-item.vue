<template> <a-form-item label="验证码" name="code" :colon="false">
        <a-input-search placeholder="输入验证码" v-model:value="code" allowClear>
            <template #prefix>
                <security-scan-outlined style="margin-right: 20px;" />
            </template>
            <template #enterButton>
                <a-button type="primary" :loading :disabled="isCountdown" @click="clickSendCodeBtn">{{ isCountdown ?
                    remaining : '发送'
                    }}</a-button>
            </template>
        </a-input-search>
    </a-form-item>

</template>

<script setup lang="ts">
import { message } from 'ant-design-vue'
import { SecurityScanOutlined } from '@ant-design/icons-vue';
import { ref } from 'vue';
import { reqSendEmailCode } from '@/api/v1/user';
import { useCountdown } from '@vueuse/core';
import { EMAIL_CODE_EXPIRATION_TIME } from '@/constant';


const { email = '', verifyEmail } = defineProps<{
    email?: string, verifyEmail(): Promise<{
        [key: string]: any;
    }>
}>()

const code = defineModel<string>()
const isCountdown = ref(false)
const loading = ref(false)

// 倒计时
let { remaining, start, reset } = useCountdown(EMAIL_CODE_EXPIRATION_TIME, {
    onComplete() {
        reset()
        isCountdown.value = false
    }
})
const clickSendCodeBtn = async () => {
    verifyEmail().then(async () => {
        try {
            loading.value = true
            const resp = await reqSendEmailCode(email)
            if (resp.code === 200) {
                message.success('发送成功')
                start()
                isCountdown.value = true
            }
            else {
                message.error(resp.msg)
            }
        } catch {
            message.error('发送失败')
        } finally {
            loading.value = false
        }
    }).catch(() => { })
}
</script>

<style scoped></style>