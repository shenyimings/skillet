# Ui Pop Confirm

## 弹出确认框组件

基于 Element Plus Popconfirm 封装的增强型弹出确认框组件，支持自定义消息内容和操作按钮。

## 示例

@[demo vue](./pop-confirm-demo1.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| title | `string` | `操作提醒` | 确认框标题 |
| message | `string` | '' | 确认消息内容 |
| icon | `string` \| `Object` | `WarningFilled` | 图标组件 |
| iconColor | `string` | `var(--light-error-default, #D14646)` | 图标颜色 |
| cancelButtonType | `string` | '' | 取消按钮类型 |
| cancelButtonText | `string` | `取消` | 取消按钮文字 |
| confirmButtonType | `string` | `primary` | 确认按钮类型 |
| confirmButtonText | `string` | `确定` | 确认按钮文字 |

## 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| confirm | 确认按钮点击事件 | `(event: MouseEvent) => void` |
| cancel | 取消按钮点击事件 | `(event: MouseEvent) => void` |

## 插槽

| 插槽名 | 说明 | 作用域参数 |
| --- | --- | --- |
| reference | 触发元素 | - |
| message | 消息内容 | - |
| actions | 操作按钮区域 | `{ confirm: (event: MouseEvent) => void, cancel: (event: MouseEvent) => void }` |

## 作用域参数

- `confirm` - 确认函数，调用后触发 confirm 事件
- `cancel` - 取消函数，调用后触发 cancel 事件

## 特性

- **安全渲染**：使用 DOMPurify 对消息内容进行安全过滤
- **自定义样式**：提供丰富的 CSS 变量和自定义类名
- **灵活插槽**：支持完全自定义消息内容和操作按钮
- **类型安全**：完整的 TypeScript 类型定义
- **响应式设计**：适配不同屏幕尺寸

## CSS 类名

- `.ui-pop-confirm` - 确认框容器
- `.ui-pop-confirm-no-message` - 无消息内容时的样式
- `.ui-popconfirm__main` - 主要内容区域
- `.ui-popconfirm__icon` - 图标样式
- `.ui-popper__arrow` - 箭头样式
- `.ui-popconfirm__action` - 操作区域
- `.message` - 消息内容样式
- `.footer` - 底部按钮区域

## CSS 变量

- `--light-bg-base` - 背景颜色
- `--light-primary-l2` - 渐变背景色
- `--font-title-md` - 标题字体大小
- `--light-text-title` - 标题文字颜色
- `--font-body-md` - 消息内容字体大小
- `--light-text-primary` - 消息内容文字颜色
- `--radius-md` - 圆角大小
