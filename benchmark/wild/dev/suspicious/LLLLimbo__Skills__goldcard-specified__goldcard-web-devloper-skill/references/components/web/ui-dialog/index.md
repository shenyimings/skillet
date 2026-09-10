# Ui Dialog

基于 Element Plus Dialog 组件封装的对话框组件。

## 示例

### 基础用法

@[demo vue](./dialog-demo1.vue)

### 自定义底部按钮

@[demo vue](./dialog-demo2.vue)

### 使用插槽

@[demo vue](./dialog-demo3.vue)

### 滚动条配置

@[demo vue](./dialog-demo4.vue)

## 属性

| 属性 | 说明            | 类型    | 默认值    |
| ---- | -------------- | ------- | --------- |
| is-title-ellipsis           | 弹窗标题文字超出显示省略号 默认换行显示 | `Boolean` | `false`     |
| close-on-press-escape       | 原 ElDialog 属性 修改默认值为 ==false== | `Boolean` | `false`     |
| close-on-click-modal        | 原 ElDialog 属性 修改默认值为 ==false== | `Boolean` | `false`     |
| show-footer                 | ==优先级最高== 控制整个底部是否展示     | `Boolean` | `true`      |
| show-confirm-button         | 是否展示底部右侧 ==确定== 按钮          | `Boolean` | `true`      |
| confirm-button-type         | ==确定== 按钮类型                       | `String`  | `primary` |
| confirm-button-text         | ==确定== 按钮文字                       | `String`  | `确定`    |
| show-cancel-button          | 是否展示底部右侧 ==取消== 按钮          | `Boolean` | `true`      |
| cancel-button-type          | ==取消== 按钮类型                       | `String`  | `primary` |
| cancel-button-text          | ==取消== 按钮文字                       | `String`  | `取消`    |
| only-show-close-button      | 仅展示底部中间 ==关闭== 按钮 底部左右两侧插槽失效               | `Boolean` | `false`     |
| close-button-text           | 底部 ==关闭== 按钮文字                  | `String`  | `关闭`    |
| close-button-type           | 底部 ==关闭== 按钮类型                  | `String`  | ''        |
| loading | 确认按钮加载状态 | `Boolean` | `false` |
| scrollbar-options           | 内容区域使用 ElScrollbar 包裹，[配置项参考](https://element-plus.org/zh-CN/component/scrollbar.html#attributes) | `Object`  | -         |
| [继承属性](https://element-plus.org/zh-CN/component/dialog.html#attributes) | 继承 ElDialog 属性                      | -       | -         |

## 事件

同 ==ElDialog== [事件](https://element-plus.org/zh-CN/component/dialog.html#%E4%BA%8B%E4%BB%B6)

| 名称    | 描述         | 类型     |
| ------- | ------------------------------------ | -------- |
| update:modelValue | 对话框显示状态更新 | `(value: boolean) => void` |
| open | 对话框打开事件 | `() => void` |
| close | 对话框关闭事件 | `() => void` |
| confirm | ==新增**：底部**确定== 按钮点击事件 | `Function` |
| cancel  | ==新增**：底部**取消== 按钮点击事件 | `Function` |

## 方法

同 ==ElDialog== [方法](https://element-plus.org/zh-CN/component/dialog.html#exposes)

| 名称          | 描述       | 类型     |
| ------------- | ---------- | -------- |
| resetPosition | 重置位置   | `Function` |
| handleClose   | 关闭对话框 | `Function` |

## 插槽

同 ==ElDialog== [插槽](https://element-plus.org/zh-CN/component/dialog.html#slots)

| 名称 | 描述 |
| --------- | -------------------------------- |
| default | 对话框主要内容 |
| header | 自定义头部内容 |
|footer| 底部整个内容插槽 当设置了该插槽，下方 ==left**、**center**、**right== 插槽内容都将被覆盖 |
| footer-left | ==新增**footer左侧插槽 `onlyShowCloseButton` 为**false== 时生效 |
| footer-center | ==新增**footer中间插槽 `onlyShowCloseButton` 为**true== 时生效 |
| footer-right | ==新增**footer右侧插槽 `onlyShowCloseButton` 为**false== 时生效|

## CSS 类名

- `.ui-dialog-component` - 组件根元素
- `.ui-dialog-header` - 头部区域
- `.ui-dialog-body` - 内容区域
- `.ui-dialog-footer` - 底部区域
- `.footer-left` - 底部左侧
- `.footer-align-center` - 底部居中
- `.fn-text` - 文本省略样式
