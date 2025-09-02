import { defineStore } from 'pinia'
import { ref } from 'vue'

// 初始值
const initAccount = {
  name: 'maitrox',
  email: 'maitrox@gmail.com',
  avatar: '',
}

export const userAccountStore = defineStore('account', () => {
  // 1. 定义数据
  const account = ref({ ...initAccount })

  // 2. 函数/动作
  function update(params: Partial<typeof initAccount>) {
    Object.assign(account.value, params)
  }

  function clear() {
    account.value = { ...initAccount }
  }

  return { account, update, clear }
})
