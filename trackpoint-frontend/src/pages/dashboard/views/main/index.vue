<template>
    <div class="content">
        <div class="text">
            <div class="w1">{{ getTimeOfDay() }}好</div>
            <div class="w2">欢迎来到h-trackpoint埋点控制台</div>
        </div>

        <img src="/src/assets/main.png" alt="" class="main">
    </div>
</template>

<script setup lang="ts">
import { SideMenuNameEnum } from '@/enum';

defineOptions({
    name: SideMenuNameEnum.Main
})
function getTimeOfDay() {
    const now = new Date();
    const hours = now.getHours();

    if (hours >= 0 && hours < 5) {
        return "凌晨";
    } else if (hours < 11) {
        return "早上";
    } else if (hours < 14) {
        return "中午";
    } else if (hours < 19) {
        return "下午";
    } else {
        return "晚上";
    }
}

</script>

<style scoped>
.content {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    align-items: center;
    font-weight: bold;

    .text {
        display: flex;
        flex-direction: column;
        justify-content: space-evenly;

        .w1 {
            font-size: 72px;
            margin-bottom: 20px;
            color: transparent;
            background-clip: text;
            background-image: linear-gradient(45deg, #42d392 25%, #647eff);
            text-align: center;
        }

        .w2 {
            font-size: 28px;
        }
    }

    .main {
        width: 100%;
        max-width: 1200px;
    }

}
</style>