# Ui Layout

门户框架顶层布局组件。该组件将页面划分为顶部通栏、左侧边栏及右侧内容区。

## 布局结构

![布局结构](/public/imgs/scheme/identityCenter/1.png)

```vue
<ui-container class="ui-layout-component">
	<ui-header class="ui-layout-header">
		<slot name="layout-header"></slot>
	</ui-header>
	<ui-container class="ui-layout-container">
		<ui-aside>
			<slot name="layout-aside"></slot>
		</ui-aside>
		<ui-container class="ui-layout-content-container">
			<ui-header class="ui-layout-content-container-header">
				<slot name="layout-label"></slot>
			</ui-header>
			<ui-main class="ui-layout-main">
				<slot></slot>
			</ui-main>
		</ui-container>
	</ui-container>
</ui-container>
```

### 插槽

#### layout-header

顶部通栏，用于呈现系统 Logo、应用切换、系统及个人状态等内容。

![顶部通栏](./images/layout-header.png)

#### layout-aside

左侧边栏，一般用于呈现子应用菜单和相关操作。

![左侧边栏](./images/layout-aside.png)

::: info

若该插槽不被应用，`el-aside` 将不参与布局。

:::

#### layout-label

内容区顶部通栏，用于呈现子应用页面标题、面包屑、已打开的标签页及相关操作。若该插槽不被应用，内容区 `el-header` 将不参与布局。

![顶部通栏](./images/layout-label.png)

::: info

若该插槽不被应用，内容区 `el-header` 将不参与布局。

:::

#### 默认插槽

默认插槽主要用于展示子应用、三方系统的业务及系统功能页面。

::: tip

子应用开发时可引入该组件，传入路由清单，模拟门户框架布局。

:::

##### 子应用开发布局组件示例

::: code-tabs
@tab layout/index.ts

```javascript
import dev from './dev.vue'
import pro from './pro.vue'

export default process.env.NODE_ENV === 'development' ? dev : pro
```

@tab layout/dev.vue

```vue
<template>
	<UiLayout>
		<template #layout-aside>
			<ul v-for="item in routes">
				<li v-for="child in item.children">
					<router-link :to="child.path">{{ child.path }}</router-link>
				</li>
			</ul>
		</template>
		<router-view></router-view>
	</UiLayout>
</template>
<script lang="ts" setup>
import { UiLayout } from '@e-cloud/eslink-plus'
import { routes } from '../router'
</script>
```

@tab layout/pro.vue

```vue
<template>
	<router-view></router-view>
</template>
```

:::

## 属性

待定。

## 事件

### aside-minified-change

侧边栏最小化事件。

事件通过 window 事件广播，且通过 postMessage 向子应用进行广播。

::: code-tabs
@tab 事件

```javascript
const handleAsideMinified => e = {
	console.log(e)
	// output: { type: 'aside-minified-change', detail: { minified: true } }
}

window.addEventListener('aside-minified-change', handleAsideMinified)
window.removeEventListener('aside-minified-change', handleAsideMinified)
```

```javascript[postMessage]
window.addEventListener('message', ({ message }) => {
	if (message.command === 'aside-minified') {
		console.log(message)
		// output: { command: 'aside-minified', detail: { minified: true } }
	}
})
```

:::

### 其他事件待定
