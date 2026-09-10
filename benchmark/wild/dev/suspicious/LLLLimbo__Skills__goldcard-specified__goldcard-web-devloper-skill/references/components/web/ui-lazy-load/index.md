# Ui Lazy Load

用于内容懒加载的容器组件，当组件进入视窗时才渲染内容，支持自定义加载占位内容。

## 示例

```vue
<template>
  <UiLazyLoad class="lazy-container">
    <!-- 延迟加载的内容 -->
    <ComplexComponent />

    <!-- 自定义加载占位符 -->
    <template #placeholder>
      <div class="loading">Loading...</div>
    </template>
  </UiLazyLoad>
</template>

<script setup lang="ts">
import { UiLazyLoad } from '@e-cloud/eslink-plus'

const handleLoad = () => {
  console.log('内容已加载')
}
</script>

<style>
.lazy-container {
  min-height: 200px;
}
</style>
```

## 属性

组件没有特定属性，但会自动为容器添加 `lazy-loaded` 类名表示内容已加载。

## 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| load | 内容进入视窗并开始渲染时触发 | - |

## 插槽

| 插槽名 | 说明 |
| --- | --- |
| default | 需要懒加载的内容 |
| placeholder | 加载前显示的占位内容 |

## 指令用法

组件也提供了相应的指令 `v-lazy-load` 用于自定义实现：

```vue
<template>
  <div v-lazy-load="options" @lazy-load="handleLoad">
    <!-- 内容 -->
  </div>
</template>

<script setup lang="ts">
import { vLazyLoad } from '@e-cloud/eslink-plus'

const options = {
  threshold: 0.1 // 配置进入视窗的阈值，默认 0.1
}

const handleLoad = () => {
  console.log('元素进入视窗')
}
</script>
```

### 指令配置项

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| threshold | `number` | 0.1 | 触发加载的视窗交叉比例阈值 |

### 指令事件

| 事件名 | 说明 |
| --- | --- |
| lazy-load | 元素进入视窗时触发 |
