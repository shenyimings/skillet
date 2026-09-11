# Ui Sort Pool

排序池组件，用于对数组项目进行拖拽排序和选择操作。支持传入对象数组，可以通过拖拽方式调整顺序，并返回排序后的数组。通过启用 `checkable` 属性可以进行项目选择，此时仅返回选中的项目。

## 功能特点

- 支持拖拽排序
- 支持项目选择(可选)
- 支持初始数据设置
- 提供排序变更事件
- 支持手动获取排序结果
- 支持水平和垂直方向布局
- 支持自定义拖拽和放置检查
- 支持自定义选择检查
- 提供多个的插槽支持

## 示例

@[demo vue](./sort-pool-demo2.vue)

## API

### 属性

| 参数 | 说明 | 类型 | 默认值 |
| --- | --- | --- | --- |
| source | 源数据数组 | `SourceItem[]` | `[]` |
| checkable | 是否启用选择功能 | `boolean` | `false` |
| showSortAction | 当 `checkable: true` 时，是否显示辅助工具栏，工具栏提供全选、反选功能 | `boolean` | `true` |
| direction | 布局方向 | `'horizontal' \| 'vertical'` | `'horizontal'` |
| gap | 项目间距 | `number \| string` | `0` |
| checkableCheck | 检查项目是否可选择 | `(item: SortedItem \| SourceItem) => boolean` | `undefined` |
| draggableCheck | 检查项目是否可拖拽 | `(item: SortedItem \| SourceItem) => boolean` | `undefined` |
| droppableCheck | 检查项目是否可放置 | `(currentItem: SourceItem \| SortedItem, list: (SortedItem \| SourceItem)[]) => boolean[]` | `undefined` |

### 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| change | 排序或选择变更时触发 | `(sortedData: SortedItem[]) => void` |
| drop | 拖拽放置时触发 | `(dropIndex: number, item: SourceItem, list: SourceItem[]) => void` |
| drag | 拖拽开始时触发 | `(dragIndex: number, item: SourceItem, list: SourceItem[]) => void` |
| check-state-change | 选择状态变更时触发 | `(source: SourceItem[]) => void` |

### 方法

通过 ref 可以获取到组件实例并调用实例方法

| 方法名 | 说明 | 方法签名 |
| --- | --- | --- |
| setData | 设置排序数据 | `(data: SortedItem[]) => void` |
| getData | 获取当前排序数据 | `() => SortedItem[]` |
| swap | 交换两个位置的项目 | `(pickIndex: number, targetIndex: number) => void` |

### 插槽

| 插槽名 | 说明 | 作用域参数 |
| --- | --- | --- |
| `${prop}-before` | 元素前插槽 | `{ model: SourceItem, index: number, isStartItem: boolean, isLastItem: boolean, list: SourceItem[] }` |
| `${prop}` | 元素替代插槽 | `{ model: SourceItem, index: number, isStartItem: boolean, isLastItem: boolean, list: SourceItem[] }` |
| `${prop}-after` | 元素后插槽 | `{ model: SourceItem, index: number, isStartItem: boolean, isLastItem: boolean, list: SourceItem[] }` |
| `list-before` | 排序列表前插槽 | - |
| `list-after` | 排序列表后插槽 | - |
| `check-action` | 选择操作工具栏插槽 | `{ list: SourceItem[], checkedAll: boolean, checked: SourceItem[], unchecked: SourceItem[], handleCheckedAllChange: Function, handleCheckedReverse: Function, checkAllText: string, reverseText: string }` |
| `drag-handle-icon` | 拖拽手柄图标插槽 | `{ model: SourceItem, index: number, isStartItem: boolean, isLastItem: boolean, list: SourceItem[] }` |

### 数据结构

#### 源数据项结构

```typescript
interface SourceItem {
  prop: string;           // 属性标识
  label: string;          // 显示文本
  checked?: boolean;      // 是否选中
  classList?: string[];   // 自定义类名
  [key: string]: any;     // 其他自定义属性
}
```

#### 排序后数据项结构

```typescript
interface SortedItem {
  prop: string;           // 属性标识
  label: string;          // 显示文本
  sort: number;           // 排序序号
  original: SourceItem;   // 原始数据
  [key: string]: any;     // 其他自定义属性
}
```
