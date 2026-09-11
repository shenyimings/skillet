# Ui Action

支持禁用态提示的操作按钮组件，有按钮或链接两种形式。

## 示例

### 基础用法

@[demo vue](./action-demo1.vue)

### 按钮样式

@[demo vue](./action-demo2.vue)

## 组件样式

提供两种样式:

- `link`: 链接样式(默认)
- `button`: 按钮样式

```vue
<template>
	<UiAction style="link">链接样式</UiAction>
	<UiAction style="button">按钮样式</UiAction>
</template>
```

## API

### Props

| 参数 | 说明 | 类型 | 默认值 |
| - | - | - | - |
| disabled     | 是否禁用           | `boolean`            | `false`        |
| actionType   | 组件样式类型       | `link \| button` | `link`         |
| tip          | 禁用态下的提示信息 | `string`             | `功能暂不可用` |
| tipPlacement | 提示框的位置       | `string`             | `top`          |
| size         | 按钮形式时的尺寸   | `string`             | `small`        |

### Events

组件透传所有原生事件至内部的 `ui-link` 或 `ui-button` 组件。

### Slots

| 插槽名  | 说明     |
| ------- | -------- |
| default | 组件内容 |
