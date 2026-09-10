# Ui Steps

## 步骤条组件

基于 Element Plus ElSteps 封装的增强型步骤条组件，支持自定义图标和状态显示。

## 示例

@[demo vue](./steps-demo1.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| active | `number` | `0` | 当前激活的步骤索引 |
| data | `Array<{ title: string }>` | `[]` | 步骤数据数组 |

## 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| change | 步骤变化事件 | `(active: number) => void` |

## 插槽

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义步骤内容 |

## 步骤状态

- **进行中 (is-process)**: 当前正在进行的步骤
- **已完成 (is-finish)**: 已经完成的步骤
- **等待中 (is-wait)**: 尚未开始的步骤

## 特性

- **状态显示**: 清晰区分进行中、已完成、等待中状态
- **自定义图标**: 支持数字序号和完成图标
- **水平布局**: 水平排列的步骤显示
- **连接线**: 步骤间的连接线样式
- **响应式设计**: 适配不同屏幕尺寸

## CSS 类名

- `.ui-steps-component` - 步骤条容器
- `.ui-step` - 单个步骤
- `.step-label` - 步骤标签容器
- `.step-order` - 步骤序号
- `.step-title` - 步骤标题
- `.is-horizontal` - 水平布局
- `.is-process` - 进行中状态
- `.is-finish` - 已完成状态
- `.is-wait` - 等待中状态
- `.ui-step__head` - 步骤头部
- `.ui-step__line` - 步骤连接线
- `.ui-step__icon` - 步骤图标

## CSS 变量

- `--light-primary-l3` - 步骤序号背景色
- `--light-text-primary` - 主要文字颜色
- `--light-text-title` - 标题文字颜色
- `--light-border-split` - 连接线颜色
- `--light-primary-default` - 进行中状态颜色
- `--light-step-finished-border` - 已完成连接线颜色
- `--font-body-md` - 字体大小
