# Ui Collapse Panel

## 折叠面板

基于 Element Plus 的折叠面板组件。

## 示例

@[demo vue](./collapse-panel-demo.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| v-model:expanded | `boolean` | `false` | 面板展开状态 |
| title | `string` | `''` | 面板标题 |
| content | `string` \| `object` |  | 面板内容（也可通过默认插槽传入） |
| disabled | `boolean` | `false` | 是否禁用面板折叠 |

## 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| change | 面板展开状态改变时触发 | `(expanded: boolean) => void` |
| update:expanded | 面板展开状态更新时触发 | `(value: boolean) => void` |

## 插槽

| 插槽名 | 说明 |
| --- | --- |
| default | 面板内容 |
| title | 面板标题 |
| icon | 面板标题右侧的图标 |
