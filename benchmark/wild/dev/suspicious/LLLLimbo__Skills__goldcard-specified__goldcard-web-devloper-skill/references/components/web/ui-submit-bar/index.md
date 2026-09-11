# Ui Submit Bar

提供一个固定在底部的提交栏，包含提交和取消按钮，支持确认弹窗功能。

## 示例

### 基础用法

@[demo vue](./submit-bar-demo1.vue)

### 禁用状态

@[demo vue](./submit-bar-demo2.vue)

### 隐藏取消按钮

@[demo vue](./submit-bar-demo3.vue)

### 自定义图标

@[demo vue](./submit-bar-demo4.vue)

### 展示提交确认气泡

@[demo vue](./submit-bar-demo5.vue)

### 左侧插槽内容

@[demo vue](./submit-bar-demo6.vue)

### 自定义按钮类型

@[demo vue](./submit-bar-demo7.vue)

### 自定义按钮文本

@[demo vue](./submit-bar-demo8.vue)

### 提交按钮追加内容

@[demo vue](./submit-bar-demo9.vue)

## 属性

| 属性名 | 说明 | 类型 | 默认值 |
| ------ | ---- | ---- | ------ |
| submitText | 提交按钮文本 | `string` | `'提交'` |
| cancelText | 取消按钮文本 | `string` | `'取消'` |
| submitType | 提交按钮类型 | `'primary' \| 'info' \| 'success' \| 'warning' \| 'danger' \| 'default'` | `'primary'` |
| cancelType | 取消按钮类型 | `'primary' \| 'info' \| 'success' \| 'warning' \| 'danger' \| 'default'` | `'default'` |
| disabled | 提交按钮是否禁用 | `boolean` | `false` |
| hideCancel | 是否隐藏取消按钮 | `boolean` | `false` |
| submitIcon | 提交按钮图标 | `string` | `'iconfont-plus icon-plus-save-line'` |
| cancelIcon | 取消按钮图标 | `string` | `'iconfont-plus icon-plus-close-circle-line'` |
| confirmTitle | 确认弹窗标题 | `string` | `'提交确认'` |
| confirmPlacement | 确认弹窗位置 | `'top' \| 'bottom' \| 'left' \| 'right' \| 'top-start' \| 'top-end' \| 'bottom-start' \| 'bottom-end' \| 'left-start' \| 'left-end' \| 'right-start' \| 'right-end'` | `'top-end'` |

## 插槽

| 名称 | 说明 |
| ---- | ---- |
| default | 提交按钮内容区域 |
| cancel | 取消按钮内容区域 |
| left | 左侧内容区域 |
| confirm | 确认弹窗内容，表示启用确认弹窗功能 |
| cancel-suffix | 取消按钮后缀内容 |
| submit-suffix | 提交按钮后缀内容 |

## 事件

| 事件名 | 说明 | 参数 |
| ------ | ---- | ---- |
| submit | 点击提交按钮时触发 | - |
| cancel | 点击取消按钮时触发 | - |

## 注意事项

- 内容高度超出滚动盒子高度时，该组件会自动固定在页面底部
- 支持国际化文本配置
- 当使用 `#confirm` 插槽时，提交按钮会触发确认弹窗
- 图标依赖 `ui-icon` 组件和 iconfont-plus 字体库