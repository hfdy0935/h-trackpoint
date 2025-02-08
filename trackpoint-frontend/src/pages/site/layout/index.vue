<template>
  <a-layout class="layout">
    <Header></Header>
    <a-layout-content>
      <router-view></router-view>
    </a-layout-content>
    <a-layout-footer style="text-align: center">
      Ant Design ©2018 Created by Ant UED
    </a-layout-footer>
  </a-layout>
</template>

<script setup lang="ts">
import { useAppStore } from '@/store';
import Header from './header/index.vue'
import { storeToRefs } from 'pinia';

const { bgColor } = storeToRefs(useAppStore())
</script>

<style scoped>
.layout {
  height: 100vh;
  background-color: v-bind(bgColor);
}
</style>
