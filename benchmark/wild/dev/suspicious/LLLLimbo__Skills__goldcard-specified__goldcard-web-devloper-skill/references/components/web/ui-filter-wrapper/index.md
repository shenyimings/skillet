# Ui Filter Wrapper

## 筛选器包装组件

一个用于包装和管理筛选器的复合组件，支持简单筛选和高级筛选模式。

## 示例

### 高级筛选

@[demo vue](./filter-wrapper-demo1.vue)

### 仅简单筛选

@[demo vue](./filter-wrapper-demo2.vue)

### 插槽使用示例

@[demo vue](./filter-wrapper-demo3.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| filters | UiFilterWrapperFilterConfig | {} | 筛选器配置，包含简单筛选和高级筛选的字段配置 |
| params | UiFilterWrapperParams | {} | 筛选器初始参数值 |
| showRefresh | boolean | true | 是否显示刷新按钮 |
| hideFilterBar | boolean | false | 是否隐藏顶部筛选工具条 |
| showAdvanced | boolean | true | 是否显示高级筛选器 |
| mode | 'simple' \| 'advanced' \| 'complex' | 'complex' | 筛选器模式 |
| customFilters | string[] | [] | 自定义筛选器字段 |

## 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| error | 错误事件 | (error: Error) |
| ready | 组件就绪事件 | () |
| refresh | 刷新事件 | (params: UiFilterWrapperParams) |
| filterChange | 筛选条件变更事件 | (params: UiFilterWrapperParams) |
| filterReset | 高级筛选器重置事件 | () |
| filterToggleChange | 高级筛选器显示/隐藏切换事件 | () |

## 插槽

| 插槽名 | 说明 |
| --- | --- |
| default | 主要内容区域 |
| simple-filter-left | 简单筛选器左侧内容 |
| simple-filter-right | 简单筛选器右侧内容 |
| top-right | 顶部栏右侧内容 |

## 类型定义

```ts
interface UiFilterWrapperFilterConfig {
  simple?: [SimpleFilterItem, SimpleFilterItem?] // 简单筛选配置，最多支持2个
  advanced?: UiFilterItem[] // 高级筛选配置
  rules?: FormRules // 表单验证规则
}

interface UiFilterWrapperParams<T extends UiFilterWrapperFilterConfig> {
  [key: string]: string \| number \| boolean \| Array<string \| number> \| Date \| null \| undefined
}
```

## 方法

| 方法名 | 说明 |
| --- | --- |
| validate | 表单验证 |
| clearValidate | 清除验证 |

## 样式变量

组件提供了以下 CSS 变量以供定制：

| 变量名 | 默认值 | 说明 |
| --- | --- | --- |
| --ui-filter-wrapper-base-gap | 12px | 基础间距 |
| --aside-width | 270px | 侧边栏宽度 |
