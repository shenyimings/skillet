# Ui Combo Input

## 组合输入框

同时支持选择和输入。选择框可左可右。

## 示例

### 基础用法

@[demo vue](./combo-input-demo1.vue)

### 选择框在右侧

@[demo vue](./combo-input-demo2.vue)

### 尺寸

@[demo vue](./combo-input-demo3.vue)

### 禁用状态

@[demo vue](./combo-input-demo6.vue)

### 选择框宽度

@[demo vue](./combo-input-demo7.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| v-model | `string \| number` | '' | 输入框的值 |
| v-model:selectValue | `string \| number` | '' | 选择框的值 |
| options | `Array<{ label: string, value: string \| number, disabled?: boolean }>` | `[]` | 选择框的选项 |
| placement | `left \| right` | 'left' | 选择框的位置 |
| size | `large \| default \| small \| mini` | 'default' | 组件尺寸 |
| disabled | `boolean \| true \| false` | `false` | 是否禁用 |
| attrs | `Record<string, any>` | `{}` | 输入框的其他属性 |
| selectAttrs | `Record<string, any>` | `{}` | 选择框的其他属性 |
| selectEvents | `Record<string, any>` | `{}` | 选择框的事件 |
| name | `string[]` | `[]` | 表单字段名 |

## 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| change | 输入框或选择框的值发生变化时触发 | `{ input: string \| number, select: string \| number }` |
| update:modelValue | 输入框值更新时触发 | `(value: string \| number)` |
| update:selectValue | 选择框值更新时触发 | `(value: string \| number)` |

## 方法

| 方法名 | 说明 |
| --- | --- |
| focus | 聚焦输入框 |
| clear | 清空输入及选择值 |

## 插槽

| 插槽名 | 说明 |
| --- | --- |
| input-prefix | 输入框前缀内容 |
| input-suffix | 输入框后缀内容 |
