<template>
    <div class="box">
        <div class="title">
            <span class="name">h-trackpoint</span>
            <span class="prop">埋点平台</span>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useAppStore } from '@/store';
import { storeToRefs } from 'pinia';

const { bgColor, textColor } = storeToRefs(useAppStore())
</script>

<style scoped lang="scss">
.box {
    display: flex;
    flex-direction: column;

    .title {
        margin-top: 160px;
        margin-bottom: 100px;
        width: 100vw;
        height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-size: 72px;
        font-weight: bold;

        .name {
            margin-bottom: 20px;
            color: transparent;
            background-clip: text;
            background-image: linear-gradient(45deg, #42d392 25%, #647eff);
        }

        .prop {
            font-size: 96px;
            color: v-bind(textColor);
            background-color: v-bind(bgColor);
        }
    }
}
</style>
