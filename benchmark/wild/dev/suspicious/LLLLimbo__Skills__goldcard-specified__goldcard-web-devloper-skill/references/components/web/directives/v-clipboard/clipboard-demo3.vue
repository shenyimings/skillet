<template>
  <div class="demo-section">
    <div class="demo-item">
      <p>同步函数：</p>
      <div v-clipboard="getCurrentTime" class="demo-box">
        点击复制当前时间
      </div>
    </div>

    <div class="demo-item">
      <p>异步函数：</p>
      <div v-clipboard="fetchApiData" class="demo-box">
        点击复制模拟API数据
      </div>
    </div>

    <div class="demo-item">
      <p>带参数的函数：</p>
      <div v-clipboard="getFormattedData" class="demo-box">
        点击复制用户数据
      </div>
    </div>

    <div class="demo-item">
      <p>函数执行失败提示：</p>
      <div
        v-clipboard.result-tip:{"success":"时间已复制","error":"获取时间失败","empty":"时间数据为空"}="getCurrentTimeWithError"
        class="demo-box"
      >
        点击复制时间（可能失败）
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const user = ref({ id: 12345 })

// 同步函数
const getCurrentTime = () => {
  return `当前时间: ${new Date().toLocaleString()}`
}

// 异步函数
const fetchApiData = async () => {
  // 模拟异步操作
  return new Promise(resolve => {
    setTimeout(() => {
      resolve('这是模拟的API数据内容')
    }, 100)
  })
}

// 带参数的函数
const getFormattedData = () => {
  return `时间: ${new Date().toLocaleString()}`
}

// 可能失败的函数
const getCurrentTimeWithError = () => {
  // 模拟随机失败
  if (Math.random() > 0.5) {
    throw new Error('获取时间失败')
  }
  return `当前时间: ${new Date().toLocaleString()}`
}
</script>

<style scoped>
.demo-box {
  padding: 8px 12px;
  margin: 5px 0;
  cursor: pointer;
  background: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 4px;
  transition: all 0.2s;
}

.demo-box:hover {
  background: #e0e0e0;
  border-color: #999;
}
</style>