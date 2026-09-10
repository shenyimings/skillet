# Ui Notification

基于 [==ElNotification==](https://element-plus.org/zh-CN/component/notification.html) 组件，添加 `customClass` 固定值 `ui-notification`，修改默认样式<br />
底部添加 ==忽略**、**处理== 默认按钮和点击事件

## 基础用法

@[demo vue](./notification-demo1.vue)

## 参数

```typescript
interface UiNotificationOptions extends Partial<NotificationOptions> {
  showInThisPage?: boolean           // 是否在当前页面中展示
  showFooter?: boolean               // 是否展示底部按钮区域
  ignoreButtonText?: string          // 忽略按钮文字
  showIgnoreButton?: boolean         // 是否显示忽略按钮
  onIgnoreClick?: (instance: NotificationHandle) => void  // 忽略按钮点击事件
  handlerButtonText?: string         // 处理按钮文字
  showHandlerButton?: boolean        // 是否显示处理按钮
  onHandlerClick?: (instance: NotificationHandle) => void // 处理按钮点击事件
}
```

## 方法

| 方法名 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| (default) | 显示通知 | (options: UiNotificationOptions) | NotificationHandle |
| success | 显示成功通知 | (config?: Omit<UiNotificationOptions, 'type'>) | void |
| warning | 显示警告通知 | (config?: Omit<UiNotificationOptions, 'type'>) | void |
| error | 显示错误通知 | (config?: Omit<UiNotificationOptions, 'type'>) | void |
| info | 显示信息通知 | (config?: Omit<UiNotificationOptions, 'type'>) | void |

## 默认配置

```typescript
const notificationDefaults = {
  customClass: 'ui-notification',
  duration: 4500,
  position: 'top-right',
  showClose: true,
  showInThisPage: !isInIframe,       // 根据是否在 iframe 中自动设置
  showFooter: true,
  showIgnoreButton: true,
  ignoreButtonText: '忽略',
  showHandlerButton: true,
  handlerButtonText: '处理'
}
```

## 特性

- **iframe 支持**：自动处理 iframe 环境下的通知展示
- **自定义按钮**：支持添加忽略和处理操作按钮
- **类型安全**：完整的 TypeScript 类型定义
- **样式定制**：提供丰富的 CSS 变量和自定义类名
- **快捷方法**：支持 success/warning/error/info 快捷调用

## CSS 类名

- `.ui-notification` - 通知容器
- `.notification-content` - 通知内容容器
- `.footer` - 底部按钮区域
