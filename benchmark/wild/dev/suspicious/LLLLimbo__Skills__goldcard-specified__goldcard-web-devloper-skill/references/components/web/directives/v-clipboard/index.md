# v-clipboard

内容复制指令，可将元素的内容、表单元素的值、自定义内容或函数返回值复制到剪贴板。

## 示例

### 基础用法

@[demo vue](./clipboard-demo1.vue)

### 表单元素复制

@[demo vue](./clipboard-demo2.vue)

### 函数值复制

@[demo vue](./clipboard-demo3.vue)

### 配置对象使用

@[demo vue](./clipboard-demo4.vue)

### 交互效果

@[demo vue](./clipboard-demo5.vue)

## 指令值类型

指令值可以是以下类型之一：

- **字符串**：直接复制该字符串内容
- **配置对象**：包含自定义内容和配置选项
- **函数**：执行函数并复制返回值（支持同步和异步函数）

### 配置对象详细说明

```typescript
interface ClipboardOptions {
  // 内容类型修饰符
	contentType?: ClipboardContentType
	// 事件类型修饰符
	eventTypes?: ClipboardEventType[]
	// 交互效果配置
	interactions?: InteractionConfig[]
	// 自定义内容（优先于元素内容）
	customContent?: string
}

// 剪贴板内容类型
type ClipboardContentType = 'text' | 'image' | 'html'

// 事件类型
type ClipboardEventType = 'click' | 'dblclick' | 'mouseup' | 'mousedown' | 'contextmenu'

// 交互效果类型
type ClipboardInteractionType = 'highlight' | 'result-tip' | 'hover-tip'


// 高亮配置
type HighlightConfig =
	| string
	| Array<{
			className: string
			timing: 'initial' | 'hover' | 'copying' | 'copied'
	  }>

// 提示配置
type TipConfig = string | {
  success?: string
  error?: string
  empty?: string
}

// 交互效果配置（联合类型）
type InteractionConfig =
	| { type: 'highlight'; options?: HighlightConfig }
	| { type: 'result-tip'; text?: TipConfig }
	| { type: 'hover-tip'; text?: TipConfig }
```

#### 配置属性说明

- **`contentType`**: 内容类型，默认为 `'text'`
  - `'text'`: 复制文本内容
  - `'image'`: 复制图片 URL
  - `'html'`: 复制 HTML 内容

- **`eventTypes`**: 触发复制的事件类型，默认为 `['click']`
  - `'click'`: 点击事件
  - `'dblclick'`: 双击事件
  - `'mouseup'`: 鼠标松开事件
  - `'mousedown'`: 鼠标按下事件
  - `'contextmenu'`: 右键菜单事件

- **`interactions`**: 交互效果配置数组，支持以下交互类型：
  - `'highlight'`: 高亮效果
    - `options.className`: 传统高亮类名
    - `options.highlightConfigs`: 高级高亮配置
  - `'result-tip'`: 结果提示
    - `options.text`: 提示文本，默认为 `'复制成功'`
  - `'hover-tip'`: 悬停提示
    - `options.text`: 提示文本，默认为 `'点击复制'`

## 修饰符

该指令支持三类修饰符：内容修饰符、事件修饰符、交互修饰符，三类修饰符可同时使用。

> 内容修饰符不可同时应用多个，比如 `text` 和 `html` 不能同时应用。

### 内容修饰符

若指令值提供了内容，则优先复制指令值的内容，否则复制元素的内容。

- `text`：默认行为，将元素的文本内容复制到剪贴板。
  - 对于表单元素（input、textarea），复制其值
  - 对于复选框（checkbox）：复制格式为 `标签: 已选中/未选中`
  - 对于单选按钮（radio）：仅复制选中项的标签
  - 对于下拉选择框（select）：复制选中选项的文本内容
- `image`：将元素的图片内容复制到剪贴板，若元素本身不是图片，则查找元素内的第一个图片元素。
- `html`：将元素的 HTML 内容复制到剪贴板。

### 事件修饰符

- `stop`：阻止事件冒泡。
- `prevent`：阻止事件默认行为。
- `click`：默认行为，点击元素时触发复制操作。
- `dblclick`：双击元素时触发复制操作。
- `mouseup`：鼠标松开时触发复制操作。
- `mousedown`：鼠标按下时触发复制操作。
- `contextmenu`：右键点击元素时触发复制操作。

### 交互修饰符

- `highlight`：点击元素时，添加一个高亮效果，复制完成后移除高亮效果。
  - 支持通过 `:` 分隔符指定样式类名，通过 `@` 符号指定样式名追加的时机
  - 时机选项：`initial`（初始状态）、`hover`（悬停时）、`copying`（复制中）、`copied`（复制后）
  - 示例：`v-clipboard.highlight:is-copyable@initial,is-copying@copying,is-hover@hover`
  - 也可以通过 options 对象传入：`highlightConfigs` 数组
- `result-tip`：复制完成后，显示一个提示框，提示用户复制结果。
  - 支持通过 `:` 分隔符指定提示内容（仅成功提示）
  - 支持通过 JSON 格式指定完整提示配置（成功、失败、空内容）
  - 示例：`v-clipboard.result-tip:已复制`（仅成功提示）
  - 示例：`v-clipboard.result-tip:{"success":"复制成功","error":"复制失败","empty":"没有内容可复制"}`（完整提示）
  - 也可以通过 options 对象传入：`interactions` 数组中的 `result-tip` 配置
- `hover-tip`：鼠标悬停在元素上时，显示一个提示框，提示用户复制操作。
  - 支持通过 `:` 分隔符指定提示内容
  - 示例：`v-clipboard.hover-tip:点击复制内容`
  - 也可以通过 options 对象传入：`interactions` 数组中的 `hover-tip` 配置

> **注意**：修饰符和 options 对象可以同时使用，options 对象配置的优先级更高。

## 事件

指令会触发以下自定义事件：

- `clipboard-success`：复制成功时触发，包含复制的内容和类型
- `clipboard-error`：复制失败时触发，包含错误信息
