<template>
    <section class="container">
        <slot name="header"></slot>
        <slot name="table"></slot>
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

    .header {
        width: 100%;
        display: flex;
        margin-bottom: 20px;
    }

    .table {
        width: 100%;
    }
}
</style>