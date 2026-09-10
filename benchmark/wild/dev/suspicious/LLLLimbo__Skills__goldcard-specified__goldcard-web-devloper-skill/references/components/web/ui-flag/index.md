# Ui Flag

## 标记组件

简单的标记组件，支持多种颜色类型和自定义内容。

## 示例

@[demo vue](./flag-demo1.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| type | 'default' \| 'primary' \| 'error' \| 'success' \| 'warning' | 'default' | 标记类型 |
| text | string | - | 标记文本内容 |
| weight | number | 1 | 标记边框宽度（像素） |
| gap | number | 8 | 标记与文本之间的间距（像素） |

## 颜色映射

| 类型 | 颜色值 | 说明 |
| --- | --- | --- |
| default | #5f677d | 默认颜色 |
| primary | #426AEA | 主要颜色 |
| error | #D14646 | 错误颜色 |
| success | #64BE7A | 成功颜色 |
| warning | #D8B15B | 警告颜色 |

## 插槽

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义标记内容 |

## CSS 变量

- `--flag-border-color` - 标记边框颜色
- `--flag-border-width` - 标记边框宽度
- `--flag-gap` - 标记与文本之间的间距

## CSS 类名

- `.ui-flag-component` - 组件根元素
- `.text` - 文本内容样式
