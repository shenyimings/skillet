# Ui Empty

## 空状态组件

基于 Element Plus Empty 组件封装的空状态组件，支持多种预设类型和自定义配置。

## 示例

@[demo vue](./empty-demo1.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| type | `resource \| service \| data \| auth \| choose \| upload` | `resource` | 空状态类型 |
| image | `string` | - | 自定义图片 URL |
| description | `string` | - | 自定义描述文本 |

## 插槽

| 插槽名 | 说明 |
| --- | --- |
| image | 自定义图片内容 |
| description | 自定义描述内容 |

## 空状态类型

| 类型 | 描述 | 默认图片 | 默认描述 |
| --- | --- | --- | --- |
| resource | 资源不存在 | no-resource.svg | 需要访问的资源不存在 |
| service | 服务器错误 | no-service.svg | 服务器内部错误 |
| data | 无数据 | no-data.svg | 未找到数据 |
| auth | 无权限 | no-auth.svg | 没有权限访问资源 |
| choose | 未选择 | no-choose.svg | 未选择数据 |
| upload | 上传中 | upload.svg | 文件上传中... |

## CSS 变量

组件提供了以下 CSS 变量以供定制：

- `--ui-empty-padding` - 空状态组件内边距

## 样式类

- `.ui-empty-component` - 组件根元素
- `.ui-empty__description` - 描述文本区域
