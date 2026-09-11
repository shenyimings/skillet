<template>
  <div class="demo-section">
    <div class="demo-item">
      <p>高亮效果：</p>
      <div v-clipboard.highlight class="demo-box">
        点击时有高亮效果
      </div>
    </div>

    <div class="demo-item">
      <p>悬停提示：</p>
      <div v-clipboard.hover-tip class="demo-box">
        鼠标悬停显示提示
      </div>
    </div>

    <div class="demo-item">
      <p>结果提示：</p>
      <div v-clipboard.result-tip class="demo-box">
        复制后显示成功提示
      </div>
    </div>

    <div class="demo-item">
      <p>组合效果：</p>
      <div v-clipboard.highlight.result-tip.hover-tip class="demo-box">
        完整交互体验
      </div>
    </div>

    <div class="demo-item">
      <p>高级高亮配置：</p>
      <div v-clipboard.highlight:is-copyable@initial,is-copying@copying,is-hover@hover,is-copied@copied class="demo-box">
        高级高亮效果
      </div>
    </div>

    <div class="demo-item">
      <p>自定义提示文本：</p>
      <div v-clipboard.result-tip:已复制.hover-tip:点击复制内容 class="demo-box">
        自定义提示文本
      </div>
    </div>

    <div class="demo-item">
      <p>完整结果提示配置：</p>
      <div v-clipboard.result-tip:{"success":"内容已复制","error":"复制失败，请重试","empty":"没有内容可复制"} class="demo-box">
        完整结果提示
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

/* 高亮样式 */
.is-copyable {
  background-color: #e6f7ff;
  border: 1px solid #91d5ff;
}

.is-hover {
  background-color: #f6ffed;
  border: 1px solid #b7eb8f;
}

.is-copying {
  background-color: #fff2e8;
  border: 1px solid #ffbb96;
  transition: all 0.3s;
}

.is-copied {
  background-color: #f6ffed;
  border: 1px solid #52c41a;
  transition: all 0.3s;
}
</style>