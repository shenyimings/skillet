# Ui Panel

通用的面板容器组件，支持头部、内容区域、底部区域和禁用状态。

1. √ todo: 标题栏：返回、标题、动作按钮、内容区（滚动区），可隐藏
2. ~~todo: 支持基于外层容器的分栏栅格布局~~
3. √ 背景、圆角

## 示例

@[demo vue](./panel-demo1.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| title | `string` | '' | 面板标题 |
| border | `boolean` | `false` | 是否显示边框 |
| showHeader | `boolean` | `true` | 是否显示头部 |
| headerClass | `string` | '' | 头部自定义类名 |
| showAction | `boolean` | `true` | 是否显示操作按钮 |
| showFooter | `boolean` | `false` | 是否显示底部 |
| footerClass | `string` | '' | 底部自定义类名 |
| scrollable | `boolean` | `false` | 内容是否可滚动 |
| disabled | `boolean` | `false` | 是否禁用面板 |
| disabledText | `string` | '' | 禁用状态提示文本 |

## 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| action | 操作按钮点击事件 | (e: Event) => void |

## 插槽

| 插槽名 | 说明 |
| --- | --- |
| default | 面板主要内容 |
| header | 头部内容，覆盖默认标题 |
| header-right | 头部右侧内容 |
| footer | 底部内容 |
| mask | 禁用状态遮罩内容 |

## 特性

- **灵活布局**：支持头部、内容、底部分离
- **滚动支持**：内置滚动条支持
- **禁用状态**：支持禁用状态和自定义遮罩
- **边框样式**：可选边框样式
- **操作按钮**：内置全屏操作按钮
- **响应式设计**：适配不同屏幕尺寸

## CSS 类名

- `.ui-panel` - 面板容器
- `.header` - 头部区域
- `.title` - 标题样式
- `.action` - 操作按钮
- `.body` - 内容区域
- `.footer` - 底部区域
- `.mask` - 禁用状态遮罩
- `.mask-text` - 禁用状态提示文本

## CSS 变量

- `--light-bg-base` - 面板背景颜色
- `--radius-xlg` - 圆角大小
- `--light-border-split` - 边框颜色
- `--light-text-title` - 标题文字颜色
- `--light-icon-link` - 操作按钮颜色
- `--light-fill-disabled` - 禁用状态背景色
- `--light-fill-dark` - 禁用状态提示背景色
- `--body-md` - 禁用状态提示文字大小
