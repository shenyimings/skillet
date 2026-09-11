# Ui-DatePicker
## 基础用法
<!-- @[demo vue](./demo1.vue) -->

## 日月年
<!-- @[demo vue](./demo2.vue) -->

## API

### Props

| 参数 | 说明 | 类型 | 默认值 |
| - | - | - | - |
| type    | 类型   | `month\|year\|day`                                   | 'day'    |
| v-model    | 当前值   | `string`                                   | --     |

### Events

| 名称  | 描述                    | 类型       |
| ----- | ----------------------- | ---------- |
| change  | 值变化时触发的事件 | `Function` |
| cancel  | 取消时触发的事件 | `Function` |

### Slots

| 插槽名  | 说明     |
| ------- | -------- |
| default | 组件内容 |