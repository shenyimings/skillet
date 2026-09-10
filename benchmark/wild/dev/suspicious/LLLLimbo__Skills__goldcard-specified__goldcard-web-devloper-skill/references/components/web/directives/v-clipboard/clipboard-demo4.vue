<template>
  <div class="demo-section">
    <div class="demo-item">
      <p>基础配置对象：</p>
      <div v-clipboard="{ customContent: '自定义内容', contentType: 'text' }" class="demo-box">
        点击复制配置内容
      </div>
    </div>

    <div class="demo-item">
      <p>高级配置对象：</p>
      <div v-clipboard="{
        customContent: '高级配置内容',
        interactions: [
          { type: 'highlight', options: { className: 'custom-highlight' } },
          { type: 'result-tip', options: { text: '已成功复制' } },
          { type: 'hover-tip', options: { text: '点击复制高级内容' } }
        ]
      }" class="demo-box">
        高级配置对象使用
      </div>
    </div>

    <div class="demo-item">
      <p>多事件类型配置：</p>
      <div v-clipboard="{
        customContent: '多事件配置',
        eventTypes: ['click', 'dblclick'],
        interactions: [
          { type: 'result-tip', options: { text: '双击或点击复制' } }
        ]
      }" class="demo-box">
        支持点击和双击复制
      </div>
    </div>

    <div class="demo-item">
      <p>图片复制配置：</p>
      <div v-clipboard.image="{
        interactions: [
          { type: 'result-tip', options: { text: '图片链接已复制' } }
        ]
      }">
        <img
          src="https://fuss10.elemecdn.com/a/3f/3302e58f9a181d2509f3dc0fa68b0jpeg.jpeg"
          alt="测试图片"
          class="demo-image"
        >
        点击复制图片链接
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

.demo-image {
  width: 100px;
  height: 100px;
  margin: 5px 0;
  cursor: pointer;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.custom-highlight {
  background-color: #f0f0f0;
  border: 2px dashed #1890ff;
}
</style>