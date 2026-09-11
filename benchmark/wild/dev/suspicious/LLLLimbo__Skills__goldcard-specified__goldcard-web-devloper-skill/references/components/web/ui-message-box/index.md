# Ui Message Box

基于 Element Plus ElMessageBox 封装的增强型消息弹框组件，支持 iframe 环境下的模态框状态管理。

对其打开、关闭事件进行拦截，添加 `postMessage` 事件，通知 ==iframe== 外部进行后续操作

## 示例

@[demo vue](./message-box-demo1.vue)

## 方法

| 方法名 | 说明 | 方法签名 |
| --- | --- | --- |
| alert | 显示警告弹框 | `(message: string, title?: string, options?: ElMessageBoxOptions) => Promise<void>` |
| confirm | 显示确认弹框 | `(message: string, title?: string, options?: ElMessageBoxOptions) => Promise<void>` |
| prompt | 显示输入弹框 | `(message: string, title?: string, options?: ElMessageBoxOptions) => Promise<string>` |

## 配置选项

```typescript
interface ElMessageBoxOptions {
  customClass?: string      // 自定义类名
  modalClass?: string       // 模态框类名
  // 其他 Element Plus ElMessageBox 选项
}
```

## 特性

- **iframe 支持**：自动处理 iframe 环境下的模态框状态
- **安全渲染**：使用 DOMPurify 对消息内容进行安全过滤
- **自定义图标**：支持不同类型的消息弹框显示不同图标
- **样式定制**：提供自定义类名支持

## CSS 类名

- `.ui-message-box` - 弹框容器
- `.ui-message-box__alert` - 警告弹框样式
- `.ui-message-box__confirm` - 确认弹框样式
- `.ui-message-box__prompt` - 输入弹框样式
- `.ui-message-box__message` - 消息内容容器
- `.ui-message-box__message__title` - 消息标题
- `.ui-message-box__message__content` - 消息内容
