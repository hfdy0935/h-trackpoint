<template>
  <a-config-provider :theme="store.theme">
    <Layout></Layout>
  </a-config-provider>
</template>

<script setup lang="ts">
import Layout from '~site/layout/index.vue'
import { useAppStore } from '@/store';


const store = useAppStore()
</script>
