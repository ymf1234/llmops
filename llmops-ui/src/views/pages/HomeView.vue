<script setup lang="ts">
import { useCounterStore } from '@/stores/counter'
import { userAccountStore } from '@/stores/account'
const counterStore = useCounterStore()
const accountStore = userAccountStore()

function updateNmae() {
  accountStore.update({ name: '新名字' })
}
</script>

<template>
  <p>这里是主页</p>
  <p>数字是:{{ counterStore.count }}</p>
  <p>双倍数值: {{ counterStore.doubleCount }}</p>
  <a-button type="primary" @click="counterStore.increment">数值+1</a-button>

  <p>当前登录的账号是: {{ accountStore.account.name }}</p>
  <p>当前登录的邮箱是: {{ accountStore.account.email }}</p>
  <a-button type="primary" @click="updateNmae">更新名字</a-button>
  <a-button type="primary" @click="accountStore.clear">重置</a-button>
  <router-link to="/space/apps">跳到应用列表</router-link>
</template>

<style scoped></style>
