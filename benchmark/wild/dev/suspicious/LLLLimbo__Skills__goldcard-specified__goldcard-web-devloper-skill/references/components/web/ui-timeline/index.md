# Ui Timeline

## 时间轴组件

一个用于展示时间流程的时间轴组件，支持垂直和水平两种布局方式，可自定义节点样式和内容。

## 示例

### 基础用法

@[demo vue](./timeline-demo1.vue)

### 垂直布局带标签

@[demo vue](./timeline-demo2.vue)

### 垂直左侧布局

@[demo vue](./timeline-demo3.vue)

### 垂直右侧布局

@[demo vue](./timeline-demo4.vue)

### 水平布局

@[demo vue](./timeline-demo5.vue)

### 水平顶端布局

@[demo vue](./timeline-demo6.vue)

### 水平底端布局

@[demo vue](./timeline-demo7.vue)

### 自定义节点内容

@[demo vue](./timeline-demo8.vue)

### 节点状态

@[demo vue](./timeline-demo9.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| data | `UiTimelineItem[]` | `[]` | 时间轴数据 |
| direction | `horizontal \| vertical` | `vertical` | 时间轴排列方向 |

## 插槽

| 插槽名 | 说明 | 作用域数据 |
| --- | --- | --- |
| time | 时间显示区域 | `{ item: UiTimelineItem }` |
| time-before | 时间之前的内容 | `{ item: UiTimelineItem }` |
| time-after | 时间之后的内容 | `{ item: UiTimelineItem }` |
| node | 节点内容 | `{ item: UiTimelineItem }` |
| content | 主要内容区域 | `{ item: UiTimelineItem }` |
| content-before | 内容之前的区域 | `{ item: UiTimelineItem }` |
| content-after | 内容之后的区域 | `{ item: UiTimelineItem }` |

## 类型定义

```ts
interface UiTimelineItem {
  datetime: string // 时间
  content: string // 内容
  state?: 'success' | 'error' | 'warning' | 'info' | 'default' // 节点状态
  title?: string // 标题
  [key: string]: any // 其他自定义属性
}

interface UiTimelineProps {
  data: UiTimelineItem[] // 时间轴数据
  direction?: 'horizontal' | 'vertical' // 排列方向
}
```

## 节点状态

组件内置了以下几种节点状态样式:

- default: 默认蓝色
- success: 成功绿色
- error: 错误红色
- warning: 警告黄色
- info: 信息灰色

## CSS变量

组件提供了以下CSS变量以供定制:

| 变量名 | 默认值 | 说明 |
| --- | --- | --- |
| --ui-timeline-item-align-items | flex-start | 时间轴项目对齐方式 |
| --font-body-md | 14px | 正文字体大小 |
| --font-title-md | 16px | 标题字体大小 |
| --light-text-primary | #303133 | 主要文本颜色 |
| --light-text-secondary | #5f677d | 次要文本颜色 |
| --light-text-title | #5f677d | 标题文本颜色 |
