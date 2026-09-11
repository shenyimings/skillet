# Ui Select List

## 可选择列表组件

一个用于展示可选择列表的组件，支持单选模式，可自定义列表项渲染。

## 示例

@[demo vue](./select-list-demo1.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| list | `Array<object \| string>` | `[]` | 列表数据，可以是对象数组或字符串数组 |
| labelKey | `string` | `'label'` | 显示文本的键名 |
| idKey | `string` | `''` | 唯一标识的键名，为空时使用 labelKey |
| title | `string` | `''` | 列表标题 |
| modelValue | `object \| string \| null` | `null` | 选中的项 |
| selectFirst | `boolean` | `false` | 是否自动选择第一项 |

## 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 选值变化事件 | `(item: object \| string \| null)` |
| select | 选择项事件 | `(item: object \| string, index: number)` |

## 插槽

| 插槽名 | 说明 | 作用域参数 |
| --- | --- | --- |
| default | 列表前的内容 | - |
| header | 头部区域内容 | - |
| item | 列表项内容 | `{ item: object, index: number }` |
| empty | 空状态内容 | - |

## 特性

- **灵活数据**：支持对象数组和字符串数组
- **自动选择**：支持自动选择第一项
- **自定义渲染**：支持完全自定义列表项显示
- **空状态处理**：支持自定义空状态显示
- **滚动支持**：内置滚动条和悬停效果
- **选中状态**：清晰的选中状态样式

## CSS 类名

- `.ui-select-list` - 列表容器
- `.list-header` - 头部区域
- `.list-content` - 列表内容区域
- `.list-item` - 列表项
- `.active` - 选中状态

## CSS 变量

- `--form-sm-margin` - 间距大小
- `--font-title-md` - 标题字体大小
- `--light-text-primary` - 主要文字颜色
- `--light-list-default-transparent-text` - 列表项默认文字颜色
- `--light-list-hover-transparent-background` - 列表项悬停背景色
- `--light-list-focus-transparent-text` - 选中状态文字颜色
- `--light-list-focus-transparent-background` - 选中状态背景色
- `--form-md-radius` - 圆角大小
- `--gap-10` - 内边距
- `--gap-16` - 内边距
