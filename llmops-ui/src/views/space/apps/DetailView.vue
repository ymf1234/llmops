<script setup lang="ts">
import { post } from '@/utils/request'

function debug() {
  console.log('debug')
  post('/api/llmops/apps/69567e02-9388-4345-9e38-02f66c59eac0/debug', {
    query: '你好',
  })
}
</script>

<template>
  <a-button type="primary" @click="debug">发起请求</a-button>
</template>

<style scoped></style>
