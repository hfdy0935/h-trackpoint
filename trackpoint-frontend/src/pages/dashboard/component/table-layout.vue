<template>
    <section class="container">
        <slot name="header"></slot>
        <slot></slot>
    </section>
</template>

<script setup lang="ts">
</script>

<style scoped>
.container {
    width: 100%;
    height: 90%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
}
</style>