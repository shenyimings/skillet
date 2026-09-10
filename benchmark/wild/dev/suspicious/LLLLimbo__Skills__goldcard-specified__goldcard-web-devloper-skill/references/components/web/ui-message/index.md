# Ui Message

基于 [==ElMessage==](https://element-plus.org/zh-CN/component/message.html) 组件，调整修改 `plain` 、`customClass` 默认值<br/>
添加底部自动关闭进度条展示，预留设置末尾操作文字属性及其点击事件

## 示例

### 基础用法

@[demo vue](./message-demo1.vue)

### 可关闭的消息提示

@[demo vue](./message-demo2.vue)

## 配置选项

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| message | `string \| VNode \| (() => VNode)` | - | 消息内容 |
| type | `'success' \| 'warning' \| 'info' \| 'error'` | `info` | 消息类型 |
| duration | `number` | `3000` | 显示时长（毫秒） |
| showInThisPage | `boolean` | `!isInIframe` | 是否在当前页面显示 |
| showAction | `boolean` | `false` | 是否显示操作按钮 |
| actionText | `string` | `''` | 操作按钮文本 |
| onActionClick | `Function` | - | 操作按钮点击回调 |
| showCloseProgress | `boolean` | `true` | 是否显示关闭进度条 |
| plain | `boolean` | `true` | 是否为朴素样式 |
| customClass | `string` | `'ui-message'` | 自定义类名 |

## 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| action-click | 操作按钮点击事件 | `() => void` |
| progress-end | 进度条完成事件 | `() => void` |
| resume | 进度条恢复事件 | `() => void` |
| pause | 进度条暂停事件 | `() => void` |

## 方法

| 方法名 | 说明 | 参数 |
| --- | --- | --- |
| UiMessage | 基础消息方法 | `(options: UiMessageOptions) => void` |
| UiMessage.success | 成功消息 | `(config?: UiMessageOptions) => void` |
| UiMessage.warning | 警告消息 | `(config?: UiMessageOptions) => void` |
| UiMessage.info | 信息消息 | `(config?: UiMessageOptions) => void` |
| UiMessage.error | 错误消息 | `(config?: UiMessageOptions) => void` |

## 特性

- **自动关闭进度条**：显示消息关闭的进度
- **鼠标悬停暂停**：鼠标悬停时暂停进度条
- **iframe 支持**：自动处理 iframe 环境下的消息显示
- **操作按钮**：支持在消息中显示操作按钮
- **自定义内容**：支持 VNode 和函数式内容

## CSS 类名

- `.ui-message` - 消息组件根元素
- `.message-content` - 消息内容容器
- `.progress-track` - 进度条轨道
- `.progress-bar` - 进度条
- `.paused` - 进度条暂停状态
