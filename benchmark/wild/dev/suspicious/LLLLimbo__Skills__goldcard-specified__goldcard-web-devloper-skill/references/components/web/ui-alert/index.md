# Ui Alert

基于 [==ElAlert==](https://element-plus.org/zh-CN/component/alert.html) 组件<br/>
调整了不同状态下图标的颜色，对应图标保持一致性<br/>
修改标题和描述文字样式，优化文字内容显示布局问题

## 示例

### 基础用法

@[demo vue](./alert-demo1.vue)

### 只显示 title

@[demo vue](./alert-demo2.vue)

### 只显示 description

@[demo vue](./alert-demo3.vue)

### 不显示图标

@[demo vue](./alert-demo4.vue)

### 不可关闭

@[demo vue](./alert-demo5.vue)

### 透明背景

@[demo vue](./alert-demo6.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| type | 'success' \| 'warning' \| 'info' \| 'error' | 'info' | 警告类型 |
| title | string | - | 警告标题 |
| description | string | - | 警告描述 |
| showIcon | boolean | true | 是否显示图标 |
| closable | boolean | true | 是否可关闭 |
| transparent | boolean | false | 是否透明背景 |
| effect | 'light' \| 'dark' | 'light' | 主题样式 |

## 插槽

| 插槽名 | 说明 |
| --- | --- |
| title | 自定义标题内容 |
| default | 自定义描述内容 |
| icon | 自定义图标内容 |
| follow | 跟随内容（在描述后显示） |

## CSS 变量

组件提供了以下 CSS 变量以供定制：

- `--ui-alert-title-with-description-font-size` - 带描述的标题字体大小
- `--ui-alert-description-font-size` - 描述字体大小

## 样式类

- `.ui-alert-component` - 组件根元素
- `.transparent` - 透明样式
- `.no-close` - 无关闭按钮样式
- `.no-title` - 无标题样式
- `.no-description` - 无描述样式
- `.ui-alert--success` - 成功类型样式
- `.ui-alert--error` - 错误类型样式
- `.ui-alert--warning` - 警告类型样式
- `.ui-alert--info` - 信息类型样式
