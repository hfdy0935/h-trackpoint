<template>
    <a-spin :spinning>
        <a-modal v-model:open="modalShow" :footer="null" :bodyStyle="{ textAlign: 'center' }" class="modal"
            destroy-on-close>
            <a-radio-group v-model:value="op" :default-value="AccountOpEnum.LOGIN" button-style="solid"
                class="radio-group">
                <a-radio-button v-for="(v, k) in AccountOpEnum" :value="v" :key="k">
                    {{ v }}
                </a-radio-button>
            </a-radio-group>
            <login-form v-if="op === AccountOpEnum.LOGIN" v-model:spinning="spinning" />
            <register-form v-else-if="op === AccountOpEnum.REGISTER" v-model:spinning="spinning" />
            <update-password-form v-else v-model:spinning="spinning" />
        </a-modal>
    </a-spin>
</template>

<script setup lang="ts">
import { AccountOpEnum } from '@/enum';
import { ref } from 'vue';
import LoginForm from './login-form.vue';
import RegisterForm from './register-form.vue';
import updatePasswordForm from './update-password-form.vue';
import { storeToRefs } from 'pinia';
import { useUserStore } from '@/store';


const { modalShow, op } = storeToRefs(useUserStore())
const spinning = ref(false)


</script>

<style scoped>
.modal {
    display: flex;
    flex-direction: column;

    .radio-group {
        padding: 30px 0;
    }
}
</style>