# Ui Tree

基于 Element Plus ElTree 封装的增强型树形组件，支持自定义节点渲染和平滑滚动定位。

1. 增加属性：before-click-method
2. 增加树滚动条滚动到指定结点方法
3. 预置插槽：文本前后插槽
4. 预置树编辑、删除
5. 预置树搜索

## 示例

### 基础用法

@[demo vue](./tree-demo1.vue)

### 节点点击前校验

@[demo vue](./tree-demo2.vue)

### 滚动到指定结点

@[demo vue](./tree-demo3.vue)

### 使用插槽

@[demo vue](./tree-demo4.vue)

### 树预置新增、编辑、删除

@[demo vue](./tree-demo5.vue)

### 树预置搜索

@[demo vue](./tree-demo6.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| useNativeTree | `boolean` | `true` | 是否使用原生树形组件 |
| beforeClickMethod | `Function` | `() => {}` | 点击前回调方法 |
| beforeClick | `boolean` | `false` | 是否启用点击前验证 |
| treeCustom | `boolean` | `false` | 是否使用自定义节点渲染 |
| props | `object` | `{ children: 'children', label: 'label' }` | 树形配置 |
| nodeKey | `string` | `id` | 节点唯一标识键名 |

## 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| before-click | 点击前事件 | `(data: object, node: object, callback: Function) => void` |
| node-click | 节点点击事件 | `(data: object, node: object, nodeComponent: object, event: Event) => void` |

## 插槽

| 插槽名 | 说明 | 作用域参数 |
| --- | --- | --- |
| default | 默认节点内容 | `{ node: object, data: object }` |
| label-before | 标签前内容 | `{ data: object }` |
| label-after | 标签后内容 | `{ data: object }` |
| row-right | 行右侧内容 | `{ data: object }` |
| empty | 空状态内容 |  |

## 方法

| 方法名 | 说明 | 参数 |
| --- | --- | --- |
| smoothScrollToTarget | 平滑滚动到指定节点 | `{ id: string, duration?: number }` |

## 特性

- **自定义渲染**: 支持完全自定义节点内容
- **点击控制**: 支持点击前验证和回调
- **平滑滚动**: 支持平滑滚动到指定节点
- **空状态处理**: 支持自定义空状态显示
- **类型安全**: 完整的 TypeScript 类型定义
- **响应式设计**: 适配不同屏幕尺寸

## CSS 类名

- `.tree-container` - 树形容器
- `.custom-tree-node` - 自定义节点容器
- `.ui-tree-node__content` - 节点内容区域
- `.is-current` - 当前选中节点

## 类型定义

```typescript
type UiTreeData = TreeData
type UiTreeNodeData = TreeNodeData
type UiTreeNode = Node

interface UiTreeComponentProps extends TreeComponentProps {
  smoothScrollToTarget: (options: { id: string; duration?: number }) => Promise<void>
}
```
