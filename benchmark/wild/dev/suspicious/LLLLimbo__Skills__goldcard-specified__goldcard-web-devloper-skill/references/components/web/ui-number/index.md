# Ui Number

## 数字展示组件

用于展示数字的组件，支持多种样式和尺寸配置。

## 示例

@[demo vue](./number-demo1.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| size | `number \| string` | `-` | 字体大小（像素） |
| primary | `boolean` | `false` | 使用主色调 |
| info | `boolean` | `false` | 使用信息色调 |
| success | `boolean` | `false` | 使用成功色调 |
| warning | `boolean` | `false` | 使用警告色调 |
| error | `boolean` | `false` | 使用错误色调 |
| small | `boolean` | `false` | 小尺寸 |
| smaller | `boolean` | `false` | 更小尺寸 |
| large | `boolean` | `false` | 大尺寸 |
| larger | `boolean` | `false` | 更大尺寸 |
| italic | `boolean` | `false` | 斜体样式 |
| bold | `boolean` | `false` | 粗体样式 |
| light | `boolean` | `false` | 细体样式 |

## 插槽

| 插槽名 | 说明 |
| --- | --- |
| default | 数字内容 |

## 特性

- **字体家族**：使用专门的数字字体 `font-num`
- **颜色主题**：支持多种语义颜色
- **尺寸控制**：支持精确尺寸和预设尺寸
- **样式定制**：支持斜体、粗体、细体等文本样式
- **响应式设计**：适配不同屏幕尺寸

## CSS 变量

- `--input-font-size` - 自定义字体大小
- `--light-text-primary` - 主要文本颜色
- `--light-primary-default` - 主色调
- `--light-info-default` - 信息色调
- `--light-success-default` - 成功色调
- `--light-warning-default` - 警告色调
- `--light-error-default` - 错误色调
- `--font-title-sm` - 小标题字体大小
- `--font-title-min` - 最小标题字体大小
- `--font-title-lg` - 大标题字体大小
- `--font-title-xlg` - 超大标题字体大小

## CSS 类名

- `.ui-number-component` - 数字组件容器
