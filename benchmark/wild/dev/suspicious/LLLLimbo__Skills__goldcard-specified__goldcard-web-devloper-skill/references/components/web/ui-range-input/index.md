# Ui Range Input

## 范围输入组件

用于输入数值范围的组件，包含起始值和结束值两个输入框。

## 示例

@[demo vue](./range-input-demo1.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| modelValue | `[number, number]` | `[0, 0]` | 范围值，格式为 [起始值, 结束值] |
| placement | `left \| right` | `left` | 输入框位置（暂未使用） |
| size | `large \| default \| small \| mini` | `default` | 输入框尺寸 |
| disabled | `boolean \| 'true' \| 'false'` | `false` | 是否禁用 |
| clearable | `boolean \| 'true' \| 'false'` | `true` | 是否可清空 |
| name | `string[]` | `[]` | 输入框名称数组 |

## 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 值变化事件 | `(value: [number, number]) => void` |
| change | 值变化事件 | `(value: [number, number]) => void` |

## 方法

| 方法名 | 说明 | 参数 |
| --- | --- | --- |
| clear | 清空输入值 | `() => void` |

## 特性

- **范围输入**：支持起始值和结束值的范围输入
- **双向绑定**：支持 v-model 双向数据绑定
- **尺寸控制**：支持多种输入框尺寸
- **状态管理**：支持禁用、可清空等状态
- **名称配置**：支持为两个输入框分别设置名称
- **样式统一**：统一的边框和交互样式

## CSS 类名

- `.ui-range-input-component` - 范围输入容器
- `.is-disabled` - 禁用状态
- `.range-input` - 单个输入框样式
- `.is-error` - 错误状态（外部容器）

## CSS 变量

- `--light-form-normal-default-background` - 默认背景颜色
- `--light-form-normal-default-border` - 默认边框颜色
- `--light-form-normal-hover-text` - 悬停文字颜色
- `--light-form-normal-hover-background` - 悬停背景颜色
- `--light-form-normal-hover-border` - 悬停边框颜色
- `--light-form-normal-press-text` - 按下文字颜色
- `--light-form-normal-press-border` - 按下边框颜色
- `--light-form-normal-disable-text` - 禁用文字颜色
- `--light-form-normal-disable-background` - 禁用背景颜色
- `--light-form-normal-disable-border` - 禁用边框颜色
- `--form-md-radius` - 圆角大小
- `--ui-color-danger` - 错误状态颜色
