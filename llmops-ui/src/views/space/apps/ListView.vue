<script setup lang="ts">
import { useCounterStore } from '@/stores/counter'
const counterStore = useCounterStore()
</script>

<template>
  <p>数字是:{{ counterStore.count }}</p>
  <p>双倍数值: {{ counterStore.doubleCount }}</p>
  <p>这里是 AI 应用列表</p>
  <router-link to="/">返回主页</router-link>
</template>

<style scoped></style>
