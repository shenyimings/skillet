# Ui Select

## 选择器组件

基于 Element Plus Select 组件封装的增强选择器组件，支持选项配置和迷你尺寸。

## 示例

@[demo vue](./select-demo1.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| options | `OptionItem[]` | `[]` | 选项配置数组 |
| size | `'large' \| 'default' \| 'small' \| 'mini'` | `'default'` | 选择器尺寸 |
| modelValue | `string \| number \| array` | `-` | 选中值 |
| multiple | `boolean` | `false` | 是否多选 |
| disabled | `boolean` | `false` | 是否禁用 |
| clearable | `boolean` | `false` | 是否可清空 |
| filterable | `boolean` | `false` | 是否可搜索 |
| placeholder | `string` | `-` | 占位文本 |

## 选项配置

```typescript
interface OptionItem {
  value: string | number      // 选项值
  label?: string             // 选项显示文本
  disabled?: boolean         // 是否禁用
  [key: string]: any         // 其他自定义属性
}
```

## 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| change | 选中值变化事件 | (value: any) |
| update:modelValue | 选中值更新事件 | (value: any) |

## 插槽

| 插槽名 | 说明 |
| --- | --- |
| default | 自定义选项内容 |
| prefix | 选择器前缀内容 |
| empty | 无选项时的内容 |

## 尺寸类型

- `large` - 大尺寸
- `default` - 默认尺寸
- `small` - 小尺寸
- `mini` - 迷你尺寸（特殊处理）

## CSS 类名

- `.ui-select--mini` - 迷你尺寸样式
- `.ui-select--multiple` - 多选模式样式
