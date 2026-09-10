# Ui Drawer

基于 [==ElDrawer==](https://element-plus.org/zh-CN/component/drawer.html) 组件。
添加`ui-drawer`、`ui-drawer-header`、`ui-drawer-body`、`ui-drawer-footer` 固定样式值，覆盖默认样式；预置底部footer ==取消**、**确定== 按钮

## 示例

### 基础用法

@[demo vue](./drawer-demo1.vue)

==UiDrawer**将 `modal`、`close-on-press-escape` 和 `close-on-click-modal` 默认值设置为 **false==，减少弹窗误关闭的可能性，可根据实际需求自行设置。<br/>
预置底部 ==取消**、**确定== 按钮，并添加了对应的响应事件

### 内容区域使用ElScrollbar包裹

内容区域高度超过自动出现滚动条
内容区域默认使用 ==ElScrollbar== 包裹，可以通过设置 `scrollbar-options` 对象属性，控制内容区域的高度、滚动条等属性，具体配置属性参考[ElScrollbar 配置属性](https://element-plus.org/zh-CN/component/scrollbar.html#attributes)

```vue
<template>
	<ui-button @click="handleOpen">UiDrawer</ui-button>
	<UiDrawer v-model="drawerVisible" title="提示" width="500">
		<div style="height: 500px">自定义内容</div>
	</UiDrawer>
</template>

<script lang="ts" setup>
const drawerVisible = ref(false)
const handleOpen = () => {
	drawerVisible.value = true
}
</script>
```

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| modelValue | boolean | false | 抽屉显示状态 |
| title | string | - | 抽屉标题 |
| showInThisPage | boolean | - | 是否在当前页面显示 |
| scrollable | boolean | true | 是否可滚动 |
| scrollbarOptions | object | {} | 滚动条配置选项 |
| isTitleEllipsis | boolean | false | 标题是否显示省略号 |
| showFooter | boolean | true | 是否显示底部 |
| showConfirmButton | boolean | true | 是否显示确认按钮 |
| confirmButtonType | string | 'primary' | 确认按钮类型 |
| confirmButtonText | string | '确定' | 确认按钮文本 |
| showCancelButton | boolean | true | 是否显示取消按钮 |
| cancelButtonType | string | '' | 取消按钮类型 |
| cancelButtonText | string | '取消' | 取消按钮文本 |
| size | string \| number | '50%' | 抽屉尺寸 |
| modal | boolean | true | 是否显示模态背景 |
| closeOnPressEscape | boolean | true | 是否可通过 ESC 关闭 |
| closeOnClickModal | boolean | true | 是否可通过点击模态背景关闭 |

## 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update:modelValue | 抽屉显示状态更新 | (value: boolean) |
| open | 抽屉打开事件 | () |
| close | 抽屉关闭事件 | () |
| confirm | 确认按钮点击事件 | () |
| cancel | 取消按钮点击事件 | () |

## 插槽

| 插槽名 | 说明 |
| --- | --- |
| default | 抽屉主要内容 |
| header | 自定义头部内容 |
| footer | 自定义底部内容 |

## 方法

| 方法名 | 说明 |
| --- | --- |
| handleClose | 手动关闭抽屉 |

## CSS 类名

- `.ui-drawer-component` - 组件根元素
- `.ui-drawer-header` - 头部区域
- `.ui-drawer-body` - 内容区域
- `.ui-drawer-footer` - 底部区域
- `.fn-text` - 文本省略样式
