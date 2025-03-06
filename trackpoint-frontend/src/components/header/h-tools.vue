<template>
    <div class="tools">
        <slot name="before"></slot>
        <a-tooltip :title="darkMode === 'light' ? '亮色模式' : '暗色模式'">
            <img class="theme-icon" :src="darkMode === 'light' ? lightIcon : darkIcon" @click="toggleDarkMode">
        </a-tooltip>
        <a-tooltip title="Github">
            <github-outlined class="github-icon" @click="goToGithub" :color="textColor" />
        </a-tooltip>
        <slot name="after"></slot>
    </div>
</template>

<script setup lang="ts">
import darkIcon from '@/assets/dark-icon.svg'
import lightIcon from '@/assets/light-icon.svg'
import { GithubOutlined } from '@ant-design/icons-vue'
import { storeToRefs } from 'pinia'
import { useAppStore } from '@/store'

const { darkMode, textColor } = storeToRefs(useAppStore())
const { toggleDarkMode } = useAppStore()
const goToGithub = () => {
    window.open('https://github.com/hfdy0935/h-trackpoint')
}
</script>

<style scoped>
.tools {
    display: flex;
    align-items: center;

    .theme-icon {
        width: 22px;
        margin-right: 16px;
        cursor: pointer;
    }

    .github-icon {
        font-size: 20px;

    }
}
</style>