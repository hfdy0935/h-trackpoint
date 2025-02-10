<template>
    <div class="box">
        <div class="content">
        <div class="title">
        <span class="name typewriter">Data Hive 埋点监测平台</span>
        </div>
        <div class="description">
            <span class="description">全方位 一站式监管</span>
        </div>
        </div>
        
        
        <!-- 点击登录-->
        <a-button class="login-button" type="primary" @click="LoginClick">
            <text name="login" id="login">Login</text>
        </a-button>
        <!-- 注册 -->
        <a-link class="register-link" type="primary" @click="RegisterClick">Don't have a account? To register</a-link>
    </div>
</template>

<script setup lang="ts">
import { useAppStore } from '@/store';
import { storeToRefs } from 'pinia';

const { bgColor, textColor } = storeToRefs(useAppStore())
const LoginClick = () => {
    // 这里可以添加更多的登录逻辑
};
const RegisterClick = () => {
    // 这里可以添加更多的注册逻辑
};

</script>

<style scoped lang="scss">
.box {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    height: 90vh;
.content{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    .title {
        // margin-top: 5%;
        width: 100vw;
        height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-size: 72px;
        font-weight: bold;

        .name {
            // margin-bottom: 20px;
            color: transparent;
            background-clip: text;
            background-image: linear-gradient(45deg, #42d392 25%, #647eff);
            position: relative;
            width: fit-content;

            &.typewriter {
                overflow: hidden;
                white-space: nowrap;
                border-right: 3px solid;
                animation: typing 3.5s steps(40, end),
                    blink-caret 0.75s step-end infinite;
            }
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
        color: skyblue;
    
}
}

    .login-button {
        width:150px;
        padding: 15px 20px;
        border-radius: 10px;
        /* 圆角边框 */
        background-image: linear-gradient(45deg, #42d392 25%, #647eff);
        /* 自定义背景颜色 */
        color: white;
        /* 字体颜色 */
        transition: background-color 0.3s;

        /* 添加过渡效果 */
        &:hover {
            background-color: #36b77f;
            /* 悬停时的背景颜色 */
        }
                    // 上下居中
        display: flex;
        justify-content: center;
        align-items: center;
        text{
            font-size: 20px;
            align-items: center;
            font-weight: bold;

        }

    }

    @keyframes typing {
        from {
            width: 0
        }

        to {
            width: 100%
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
