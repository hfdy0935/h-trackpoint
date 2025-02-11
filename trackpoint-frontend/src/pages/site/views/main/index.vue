<template>
    <div class="box">
        <div class="content">
            <div class="title">
                <span class="typewriter typewriter1">Data Hive</span>&nbsp;
                <span class="typewriter typewriter2">埋点监测平台</span>
            </div>
            <div class="description">
                全方位 一站式监管
            </div>
            <a-button class="login-button" type="primary" @click="doLogin">
                <text name="login" id="login">登录</text>
            </a-button>
            <a-button type="link" @click="doRegister">没有账号？去注册</a-button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { AccountOpEnum } from '@/enum';
import { useAppStore, useUserStore } from '@/store';
import { storeToRefs } from 'pinia';

const { textColor } = storeToRefs(useAppStore())

const { modalShow, op } = storeToRefs(useUserStore())
const doLogin = () => {
    op.value = AccountOpEnum.LOGIN
    modalShow.value = true
};
const doRegister = () => {
    op.value = AccountOpEnum.REGISTER
    modalShow.value = true
};

</script>

<style scoped lang="scss">
.box {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    height: 90vh;

    .content {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        .title {
            width: 100vw;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            align-items: center;
            font-size: 72px;
            font-weight: bold;

            .typewriter {
                color: transparent;
                background-clip: text;
                overflow: hidden;
                white-space: nowrap;
            }

            .typewriter1 {
                background-image: linear-gradient(45deg, #42d392 25%, #4EB4B9);
                animation: typing 3.5s steps(40, end)
            }

            .typewriter2 {
                border-right: 3px solid;
                background-image: linear-gradient(45deg, #4EB4B9 25%, #647eff);
                animation: typing2 7s steps(40, end),
                    blink-caret 0.75s step-end infinite;
            }
        }

        .description {
            margin-bottom: 10px;
            width: 100vw;
            height: 100px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-size: 24px;
            font-weight: bold;
            color: v-bind(textColor)
        }

        .login-button {
            width: 150px;
            height: 45px;
            border-radius: 10px;
            margin-bottom: 10px;
            background-image: linear-gradient(45deg, #42d392 25%, #647eff);
            transition: background-color 0.3s;

            text {
                font-size: 24px;
                font-weight: bold;
            }
        }
    }


    @keyframes typing {
        from {
            max-width: 0;
        }

        to {
            max-width: 50%;
        }
    }

    @keyframes typing2 {
        0% {
            max-width: 0;
        }

        50% {
            max-width: 0;
        }

        to {
            max-width: 50%;
        }
    }

    @keyframes blink-caret {

        from,
        to {
            border-color: transparent
        }

        50% {
            border-color: #42d392
        }
    }

}
</style>
