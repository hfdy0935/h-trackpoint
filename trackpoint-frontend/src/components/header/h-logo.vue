<template>
    <div class="logo" @click="router.push('/')">
        <img :src="logo" alt="h-trackpoint" />
        <Transition>
            <span v-if="!hiddenTitle" class="text">Data Hive</span>
        </Transition>
    </div>
</template>

<script setup lang="ts">
import logo from '@/assets/logo.svg'
import { useAppStore } from '@/store';
import { storeToRefs } from 'pinia';
import { useRouter } from 'vue-router';
defineProps<{
    hiddenTitle?: boolean
}>()


const router = useRouter()
const { textColor } = storeToRefs(useAppStore())
</script>

<style scoped>
.logo {
    display: flex;
    align-items: center;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    user-select: none;

    img {
        width: 28px;
        margin-right: 10px;
    }

    .text {
        color: v-bind(textColor);
    }

    .v-enter-active,
    .v-leave-active {
        transition: all 0.3s linear;
    }

    .v-enter-from,
    .v-leave-to {
        transform: translateY(-100px);
        position: fixed;
    }

    .v-enter-to,
    .v-leave-from {
        transform: translateY(0);
    }
}
</style>