# Ui Radio Button Group

## 单选按钮组组件

基于 Element Plus Radio Button 封装的单选按钮组组件，支持选项配置和尺寸控制。

## 示例

@[demo vue](./radio-button-group-demo1.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| size | 'large' \| 'default' \| 'small' \| 'mini' | 'default' | 按钮组尺寸 |
| modelValue | string \| number | undefined | 选中的值 |
| options | Array<{ label: string, value: string \| number }> | [] | 选项配置 |

## 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 选值变化事件 | (value: string \| number) |

## 插槽

| 插槽名 | 说明 | 作用域参数 |
| --- | --- | --- |
| label | 自定义选项标签 | { data: { label: string, value: string \| number } } |

## 特性

- **选项配置**：支持通过 options 属性配置选项
- **尺寸控制**：支持多种尺寸预设
- **双向绑定**：支持 v-model 双向数据绑定
- **自定义标签**：支持通过插槽自定义选项显示
- **样式统一**：统一的边框和圆角样式

## 尺寸说明

- **large**: 大尺寸，高度为 `--ui-form-lg-height`
- **default**: 默认尺寸，高度为 `--ui-form-md-height`
- **small**: 小尺寸，高度为 `--ui-form-sm-height`
- **mini**: 迷你尺寸，高度为 `--ui-form-mini-height`

## CSS 类名

- `.ui-radio-button-group` - 按钮组容器
- `.large` - 大尺寸样式
- `.small` - 小尺寸样式
- `.mini` - 迷你尺寸样式
- `.ui-radio-button` - 单个按钮样式
- `.ui-radio-button__inner` - 按钮内部样式

## CSS 变量

- `--ui-form-md-height` - 默认尺寸高度
- `--ui-form-lg-height` - 大尺寸高度
- `--ui-form-sm-height` - 小尺寸高度
- `--ui-form-mini-height` - 迷你尺寸高度
- `--light-button-default-normal-border` - 边框颜色
- `--button-md-radius` - 默认圆角大小
- `--button-lg-radius` - 大尺寸圆角大小
- `--button-sm-radius` - 小尺寸圆角大小
