# Ui Button

## 示例

### 基础用法

@[demo vue](./button-demo1.vue)

### 禁用按钮

@[demo vue](./button-demo2.vue)

### 文本按钮

@[demo vue](./button-demo3.vue)

### 加载状态按钮

@[demo vue](./button-demo4.vue)

### 调整尺寸

@[demo vue](./button-demo5.vue)

## API

### Props

| 参数 | 说明 | 类型 | 默认值 |
| - | - | - | - |
| type | 类型         | `'default'\|'primary'\|'info'\|'danger'`                                   | 'default'     |
| disabled | 是否禁用         | `boolean`                                   | false     |
| link     | 是否为链接按钮   | `boolean`                                   | false     |
| round    | 是否为圆角按钮   | `boolean`                                   | false     |
| loading  | 是否为加载中状态 | `boolean`                                   | false     |
| size     | 按钮尺寸         | `'small'\|'default'\|'large'\|'mini'` | 'default' |

### Slots

| 插槽    | 说明           |
| ------- | -------------- |
| default | 自定义默认内容 |
