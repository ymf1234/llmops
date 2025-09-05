<script setup lang="ts">
import { debugApp } from '@/services/app'
import Message from '@arco-design/web-vue/es/message'
import { ref, nextTick } from 'vue'
import { useRoute } from 'vue-router'

// 定义消息类型接口
interface Message {
  role: 'human' | 'ai'
  content: string
}

// 定义交互所需的数据
const query = ref('')
const messages = ref<Message[]>([]) // 为 messages 指定正确的类型
const isLoading = ref(false)
const chatContainer = ref<HTMLElement>()
const route = useRoute() // 获取路由信息

// 滚动到底部
function scrollToBottom() {
  nextTick(() => {
    if (chatContainer.value) {
      try {
        // 检查scrollTo方法是否存在
        if (typeof chatContainer.value.scrollTo === 'function') {
          chatContainer.value.scrollTo({
            top: chatContainer.value.scrollHeight,
            behavior: 'smooth',
          })
        } else {
          // 降级到直接设置scrollTop
          chatContainer.value.scrollTop = chatContainer.value.scrollHeight
        }
      } catch (error) {
        console.warn('滚动到底部失败:', error)
        // 降级到直接设置scrollTop
        try {
          if (chatContainer.value) {
            chatContainer.value.scrollTop = chatContainer.value.scrollHeight
          }
        } catch (fallbackError) {
          console.warn('滚动到底部失败:', fallbackError)
        }
      }
    }
  })
}

// 清空消息
function clearMessage() {
  messages.value = []
}

// 发送消息
async function send() {
  //1. 获取用户输入的消息, 并校验是否存在
  if (!query.value) {
    Message.error('请输入问题')
    return
  }

  // 2. 当上一条没有结束时,不允许发送新得请求
  if (isLoading.value) {
    Message.warning('请等待当前消息发送完成')
    return
  }

  try {
    isLoading.value = true
    // 3. 提取用户的信息
    const humanQuery = query.value.trim()
    messages.value.push({
      role: 'human',
      content: humanQuery,
    })

    // 清空输入框
    query.value = ''

    // 滚动到底部
    scrollToBottom()

    // 发送 api 请求 cd9f121d-ac48-44fd-87cc-8a2ec3426c17
    const response = await debugApp(route.params.app_id as string, humanQuery)

    const content = response.data.content

    messages.value.push({
      role: 'ai',
      content: content,
    })

    // 滚动到底部
    scrollToBottom()
  } catch (error) {
    Message.error(error instanceof Error ? error.message : '请求失败')
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <!-- 最外层容器,高度盛满整个浏览器屏幕 -->
  <div class="min-h-screen">
    <!-- 顶部导航栏 -->
    <header class="flex items-center h-[74px] bg-gray-100 border-b border-gray-200">
      顶部导航栏
    </header>

    <!-- 底部内容区域 -->
    <div class="flex flex-row h-[calc(100vh-74px)]">
      <!-- 左侧的编排 -->
      <div class="w-2/3 bg-gray-50 h-full">
        <header class="flex items-center h-16 border-b border-gray-200 px-7 text-xl text-gray-700">
          应用编排
        </header>

        <div class="flex flex-row h-[calc(100%-4rem)]">
          <div class="flex-1 border-r border-gray-200 p-6">人设与回复逻辑</div>
          <div class="flex-1 p-6">应用能力</div>
        </div>
      </div>

      <!-- 右侧调试与预览 -->
      <div class="flex flex-col w-1/3 bg-white h-full">
        <header
          class="flex items-center h-16 px-4 text-xl bg-white border-b border-gray-200 shadow-sm"
        >
          调试与预览
        </header>
        <!-- 调试对话界面 -->
        <div ref="chatContainer" class="flex-1 min-h-0 px-6 py-4 overflow-x-hidden overflow-y-auto">
          <!-- 消息列表 -->
          <div v-for="message in messages" :key="message.content" class="mb-6">
            <!-- AI消息 - 左对齐 -->
            <div v-if="message.role === 'ai'" class="flex flex-row gap-2">
              <!-- AI头像 -->
              <a-avatar :style="{ backgroundColor: '#00d0b6' }" class="flex-shrink-0" :size="30">
                <icon-apps />
              </a-avatar>
              <!-- AI消息内容 -->
              <div class="flex flex-col gap-2">
                <div class="font-semibold text-gray-700">AI</div>
                <div
                  class="max-w-max bg-gray-100 text-gray-900 border border-gray-200 px-4 py-3 rounded-2xl leading-5"
                >
                  {{ message.content }}
                </div>
              </div>
            </div>

            <!-- 人类消息 - 右对齐 -->
            <div v-else class="flex flex-row-reverse gap-2">
              <!-- 人类头像 -->
              <a-avatar :style="{ backgroundColor: '#3370ff' }" class="flex-shrink-0" :size="30">
                <icon-user />
              </a-avatar>
              <!-- 人类消息内容 -->
              <div class="flex flex-col gap-2 items-end">
                <div class="font-semibold text-gray-700">人类</div>
                <div class="max-w-max bg-blue-700 text-white px-4 py-3 rounded-2xl leading-5">
                  {{ message.content }}
                </div>
              </div>
            </div>
          </div>

          <!-- 当没任何消息的时候显示 -->
          <div
            v-if="!messages.length"
            class="mt-[200px] flex flex-col items-center justify-center gap-2"
          >
            <a-avatar :size="70" shape="square" :style="{ backgroundColor: '#00d0b6' }">
              <icon-apps />
            </a-avatar>
            <div class="text-2xl font-semibold text-gray-900">聊天机器人</div>
          </div>
          <!-- AI 加载状态 -->
          <div v-if="isLoading" class="flex flex-row gap-2 mb-6">
            <!-- 头像 -->
            <a-avatar :style="{ backgroundColor: '#00d0b6' }" class="flex-shrink-0" :size="30">
              <icon-apps />
            </a-avatar>
            <!-- 实际消息 -->
            <div class="flex flex-col gap-2">
              <div class="font-semibold text-gray-700">AI</div>
              <div
                class="max-w-max bg-gray-100 text-gray-900 border border-gray-2 px-4 py-3 rounded-2xl leading-5"
              >
                <icon-loading />
              </div>
            </div>
          </div>
        </div>

        <!-- 底部输入框 -->
        <div class="w-full flex-shrink-0 flex flex-col border-t border-gray-200 bg-gray-50">
          <!-- 输入框容器 -->
          <div class="p-3 sm:p-4 md:p-6">
            <!-- 输入框组件 -->
            <div class="flex items-center gap-2 sm:gap-3 md:gap-4">
              <!-- 清除按钮 -->
              <a-button
                class="flex-shrink-0 hidden sm:flex"
                type="text"
                shape="circle"
                @click="clearMessage"
              >
                <template #icon>
                  <icon-empty size="16" :style="{ color: '#374751' }" />
                </template>
              </a-button>

              <!-- 输入框主体 -->
              <div
                class="h-[40px] sm:h-[44px] md:h-[50px] flex items-center gap-2 px-3 sm:px-4 flex-1 min-w-0 border border-gray-200 rounded-full bg-white hover:border-gray-300 focus-within:border-blue-500 transition-colors"
              >
                <input
                  type="text"
                  placeholder="输入你的问题..."
                  class="flex-1 min-w-0 outline-none text-sm sm:text-base bg-transparent placeholder-gray-400"
                  v-model="query"
                  @keyup.enter="send"
                />
                <!-- 右侧按钮组 -->
                <div class="flex items-center gap-1 flex-shrink-0">
                  <!-- 附件按钮 -->
                  <a-button type="text" shape="circle" size="small" class="hover:bg-gray-100">
                    <template #icon>
                      <icon-plus />
                    </template>
                  </a-button>

                  <!-- 发送按钮 -->
                  <a-button
                    type="primary"
                    shape="circle"
                    size="small"
                    class="bg-blue-600 hover:bg-blue-700 border-blue-600 hover:border-blue-700"
                    @click="send"
                  >
                    <template #icon>
                      <icon-send />
                    </template>
                  </a-button>
                </div>
              </div>
            </div>
          </div>

          <!-- 底部提示文字 -->
          <div class="text-center text-gray-400 text-xs pb-3 px-4">
            <span class="sm:inline">内容由 AI 生成，无法确保真实准确，仅供参考。</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
