<template>
  <div class="demo-section">
    <div class="demo-item">
      <p>复制元素文本内容：</p>
      <div v-clipboard class="demo-box">
        点击这里复制文本内容
      </div>
    </div>

    <div class="demo-item">
      <p>复制自定义内容：</p>
      <div v-clipboard="'自定义内容'" class="demo-box">
        点击这里复制自定义内容
      </div>
    </div>

    <div class="demo-item">
      <p>使用修饰符：</p>
      <div v-clipboard.text.highlight.result-tip class="demo-box">
        复制文本并显示提示
      </div>
    </div>
  </div>
</template>

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