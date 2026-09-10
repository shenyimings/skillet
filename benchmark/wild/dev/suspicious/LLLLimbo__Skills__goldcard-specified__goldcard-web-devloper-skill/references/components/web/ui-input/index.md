# Ui Input

## 输入框组件

基于 Element Plus Input 组件封装的增强输入框组件，支持字数限制、数字输入验证等功能。重写了字数输入字符限制功能，使其输入超出后可继续输入，并触发校验规则。

## 示例

@[demo vue](./input-demo1.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| modelValue | `string \| number` | '' | 输入值 |
| showWordLimit | `boolean` | `false` | 是否显示字数限制 |
| maxlength | `string \| number` | `Number.MAX_SAFE_INTEGER` | 最大输入长度 |

## 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 输入值更新事件 | `(value: string \| number) => void` |
| validate | 输入验证事件 | `(isValid: boolean) => void` |
| input | 输入事件 | `(value: string \| number) => void` |
| compositionstart | 输入法开始事件 | `(event: CompositionEvent) => void` |
| compositionend | 输入法结束事件 | `(event: CompositionEvent) => void` |
| blur | 失去焦点事件 | `(event: FocusEvent) => void` |

## 插槽

| 插槽名 | 说明 |
| --- | --- |
| prepend | 输入框前置内容 |
| append | 输入框后置内容 |
| prefix | 输入框前缀内容 |
| suffix | 输入框后缀内容 |

## 方法

| 方法名 | 说明 |
| --- | --- |
| validate | 验证输入内容 |
| focus | 聚焦输入框 |
| blur | 失焦输入框 |
| clear | 清空输入内容 |

## 计算属性

| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| currentLength | `number` | 当前输入长度 |
| isOverLimit | `boolean` | 是否超过最大长度限制 |

## CSS 类名

- `.ui-input-component` - 组件根元素
- `.word-limit` - 字数限制区域
- `.over-limit` - 超过限制样式
- `.is-disabled` - 禁用状态样式
