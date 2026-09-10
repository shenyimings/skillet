# Ui Image Viewer

## 图片查看器组件

基于 Element Plus ImageViewer 组件封装的图片查看器，支持 iframe 环境适配。

## 示例

@[demo vue](./image-viewer-demo1.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| modelValue | `boolean` | `false` | 查看器显示状态 |
| urlList | `string[]` | `[]` | 图片 URL 列表 |
| initialIndex | `number` | `0` | 初始显示图片索引 |
| zIndex | `number` | `2000` | 查看器 z-index |
| teleported | `boolean` | `true` | 是否挂载到 body |
| showProgress | `boolean` | `true` | 是否显示进度条 |

## 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 查看器显示状态更新 | `(value: boolean) => void` |
| close | 查看器关闭事件 | `() => void` |

## 方法

| 方法名 | 说明 | 参数 |
| --- | --- | --- |
| setActiveItem | 设置当前激活的图片 | `(index: number) => void` |

## 特性

- **iframe 支持**：自动处理 iframe 环境下的 z-index 问题
- **进度显示**：支持图片加载进度显示
- **快捷键支持**：支持键盘导航（左右箭头、ESC）
- **响应式设计**：适配不同屏幕尺寸

## 使用说明

组件会自动处理 iframe 环境下的层级问题，确保图片查看器能够正确显示在顶层。
