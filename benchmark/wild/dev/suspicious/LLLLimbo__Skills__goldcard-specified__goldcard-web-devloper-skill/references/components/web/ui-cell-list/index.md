# Ui Cell List

一个灵活的单元格列表组件：

1. 支持水平、垂直及其逆序展示
2. 支持数值强调
3. 支持对齐方式

## 示例

### 基础用法

@[demo vue](./cell-list-demo1.vue)

### 标签、数值纵向排列且末端对齐

@[demo vue](./cell-list-demo2.vue)

### 配置列表列数

@[demo vue](./cell-list-demo3.vue)

### 列表纵向排列, 标签、数值末端对齐

@[demo vue](./cell-list-demo4.vue)

### 列表及标签、数值均纵向排列

@[demo vue](./cell-list-demo5.vue)

### 标签、数值均纵向逆序排列

@[demo vue](./cell-list-demo6.vue)

### 列表为空占位，自定义文本

@[demo vue](./cell-list-demo7.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| data | `UiCellItem[]` | `[]` | 单元格数据数组 |
| listDirection | `horizontal \| vertical` | `horizontal` | 列表布局方向 |
| itemDirection | `horizontal \| vertical` | `horizontal` | 单元格内布局方向 |
| listGap | `string` | `16px` | 列表项间距 |
| itemGap | `string` | `8px` | 单元格内标签和值间距 |
| itemInnerGap | `string` | `4px` | 单元格值内部间距 |
| reverse | `boolean \| string` | `false` | 是否反转单元格内元素顺序 |
| align | `start \| center \| end` | `start` | 单元格对齐方式 |
| cols | `number \| string` | `2` | 列数（水平布局时有效） |
| emptyText | `string` | `暂无数据` | 空数据提示文本 |
| decoration | `underline \| underline-dashed \| left-square \| left-dot \| left-circle \| left-line \| left-arrow` | - | 装饰样式 |
| decorationColor | `string` | - | 装饰颜色 |
| decorationSize | `string` | - | 装饰尺寸 |
| labelWidth | `string` | `auto` | 标签宽度 |
| blankText | `string` | `--` | 空值显示文本 |
| showOverflowTooltip | `boolean \| string` | `false` | 是否显示溢出提示 |
| overflowTooltipPlacement | `OverflowTooltipPlacement` | `top` | 溢出提示位置 |

## 单元格项配置

```typescript
interface UiCellItem {
  show?: boolean                    // 是否显示
  label: string                     // 标签文本
  value: any                        // 值
  prefix?: string                   // 值前缀
  suffix?: string                   // 值后缀
  highlight?: boolean               // 是否高亮显示
  span?: number \| string           // 跨列数
  noDecoration?: boolean            // 是否禁用装饰
  align?: 'start' \| 'center' \| 'end'  // 对齐方式
  justify?: 'flex-start' \| 'flex-end' \| 'center' \| 'space-between'  // 主轴对齐
  direction?: 'horizontal' \| 'vertical'  // 单元格内方向
  prop?: string                     // 字段名
  classList?: string[]              // 自定义类名
  blankText?: string                // 空值显示文本
  showOverflowTooltip?: boolean     // 是否显示溢出提示
  overflowTooltipPlacement?: OverflowTooltipPlacement  // 溢出提示位置
  breakWord?: boolean               // 是否换行显示
}
```

## 方法

| 方法名 | 说明 |
| --- | --- |
| updateOverflowStates | 更新溢出状态 |

## 插槽

| 插槽名 | 说明 |
| --- | --- |
| `label-{prop}` | 自定义标签内容 |
| `value-{prop}` | 自定义值内容 |
| `value-prefix-{prop}` | 自定义值前缀内容 |
| `value-suffix-{prop}` | 自定义值后缀内容 |

## 装饰样式

支持以下装饰样式：

- `underline` - 下划线
- `underline-dashed` - 虚线
- `left-square` - 左侧方块
- `left-dot` - 左侧圆点
- `left-circle` - 左侧圆圈
- `left-line` - 左侧线条
- `left-arrow` - 左侧箭头

## CSS 变量

组件提供了以下 CSS 变量以供定制：

- `--cell-list-gap` - 列表项间距
- `--cell-item-gap` - 单元格内间距
- `--cell-item-inner-gap` - 单元格值内部间距
- `--cell-cols` - 列数
- `--decoration-color` - 装饰颜色
- `--decoration-size` - 装饰尺寸
- `--cell-label-width` - 标签宽度

## 主题定制

可以通过覆盖以下 CSS 类来自定义样式：

```scss
.ui-cell-list {
  // 列表容器样式
}

.ui-cell-item {
  // 单元格项样式
}

.cell-label {
  // 标签样式
}

.cell-value {
  // 值区域样式

  &.is-highlight {
    // 高亮样式
  }

  .value-prefix,
  .value-suffix {
    // 前缀后缀样式
  }

  .value-number {
    // 数值样式
  }
}
```
