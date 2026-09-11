# Ui Code Viewer

代码查看器组件，支持代码高亮显示、复制代码功能，可展示多种语言的代码。

## 示例

@[demo vue](./code-viewer-demo1.vue)

## 组件特性

### 代码高亮

支持多种编程语言的代码高亮显示，包括但不限于 JavaScript、SQL、JSON、HTML、CSS 等。

### 代码复制

提供复制按钮，点击可将代码复制到剪贴板。

## API

### Props

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| code | 要展示的代码内容 | `string` | - |
| lang | 代码语言类型，支持 js, sql, json, html, css, md | `js \| sql \| json \| html \| css \| md \| undefined` | - |

### Events

无

### Slots

无
