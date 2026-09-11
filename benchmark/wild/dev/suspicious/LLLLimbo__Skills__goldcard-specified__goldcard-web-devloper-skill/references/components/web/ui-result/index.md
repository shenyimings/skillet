# Ui Result

## 结果页面组件

基于 [==ElResult==](https://element-plus.org/zh-CN/component/result.html) 组件。

调整了不同状态下图标的颜色，修改了`info` 类型的对应图标。继承了原先的属性和插槽，使用方式和 ==ElResult== 没有区别。

## 示例

@[demo vue](./result-demo1.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| icon | `success \| warning \| info \| error` | `info` | 结果图标类型 |

## 插槽

| 插槽名 | 说明 |
| --- | --- |
| icon | 自定义图标 |
| title | 标题内容 |
| sub-title | 副标题内容 |
| extra | 额外操作区域 |

## 图标类型

| 类型 | 图标 | 颜色 |
| --- | --- | --- |
| success | CircleCheckFilled | `--light-success-default` |
| warning | QuestionFilled | `--light-warning-default` |
| info | WarningFilled | `--light-primary-default` |
| error | CircleCloseFilled | `--light-error-default` |

## 特性

- **多种状态**：支持成功、警告、信息、错误四种状态
- **自定义图标**：支持通过插槽完全自定义图标
- **完整布局**：包含图标、标题、副标题、操作区域
- **样式定制**：提供丰富的 CSS 变量和自定义类名
- **响应式设计**：适配不同屏幕尺寸

## CSS 类名

- `.ui-result-component` - 结果页面容器
- `.ui-result__icon` - 图标区域
- `.ui-result__title` - 标题区域
- `.ui-result__subtitle` - 副标题区域
- `.ui-result__extra` - 额外操作区域
- `.success-color` - 成功状态颜色
- `.warning-color` - 警告状态颜色
- `.info-color` - 信息状态颜色
- `.error-color` - 错误状态颜色

## CSS 变量

- `--light-success-default` - 成功状态颜色
- `--light-warning-default` - 警告状态颜色
- `--light-primary-default` - 信息状态颜色
- `--light-error-default` - 错误状态颜色
- `--light-text-title` - 标题文字颜色
- `--light-text-secondary` - 副标题文字颜色
