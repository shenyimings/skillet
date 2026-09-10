# UiInfoPop 组件

提供一个图标，通过鼠标交互来展示帮助内容或额外信息。

## 示例

### 基础用法

@[demo vue](./info-pop-demo1.vue)

### 弹出位置

@[demo vue](./info-pop-demo2.vue)

### 亮色主题

@[demo vue](./info-pop-demo3.vue)

### 复杂示例

@[demo vue](./info-pop-demo4.vue)

## 属性说明

| 属性名      | 说明                | 类型                        | 默认值        |
| ---------- | ------------------ | -------------------------- | ------------- |
| placement  | 气泡出现的位置  | `top \| bottom \| left \| right \| (top\|bottom\|left\|right)-start \| (top\|bottom\|left\|right)-end` | `top` |
| trigger    | 触发方式       | `hover \| click \| focus \| contextmenu` | `hover` |
| icon       | 图标名称        | `string`           | `iconfont icon-question-line` |
| color      | 图标颜色        | `string`    | `var(--light-button-default-link-icon)` |
| width      | 气泡宽度        | `number \| ${number}`   | `auto` |
| size       | 图标大小        | `number \| ${number}`   |          |
| className  | 图标自定义 class | `string`         |    |
| effect     | 气泡主题        | `light \| dark` | `dark` |
| verticalAlign | 图标垂直对齐方式 | `top \| middle \| bottom \| baseline \| sub \| super`   | `inherit` |
| popperOptions | Popper.js 配置选项 | `object` | `{ modifiers: [...] }` |

## 插槽

| 名称   | 说明         |
| ------ | ------------ |
| 默认   | 气泡内容区域 |

## 注意事项

- 该组件会自动继承父级传递的属性（`v-bind="$attrs"`），可用于自定义更多 Popover 行为。
- 图标依赖 `ui-icon` 组件和 iconfont 字体库。
