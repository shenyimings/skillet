# 接入指南

## 安装

### 环境准备

- [Node.js](https://nodejs.org/) 20 及以上版本。
- 配置公司 npm 私域
::: code-tabs
@tab bash
```bash 
npm config set @e-cloud:registry http://npm.eslink.cc
```
:::

### 安装依赖

::: npm-to
```bash
npm install @e-cloud/eslink-threejs --save
```
:::

## 快速开始

::: code-tabs
@tab main.ts
```typescript
import { createApp } from 'vue'
import EslinkPlus from '@e-cloud/eslink-plus'
import '@e-cloud/eslink-plus/dist/style.css'
import App from './App.vue'

const app = createApp(App)

app.use(EslinkPlus)
app.use(directives.permission, { permissions: ['admin', 'my-button2'] })
microAppInit(app, { menus }).then(data => {
	const { lang } = data
	if (lang) {
		updateLocale(lang as Locale)
	}
})
app.mount('#app')
```
:::

## 开发使用

### 引入组件

::: code-tabs
@tab pages/home/index.vue
```vue
<template>
	<h1>Home</h1>
	<UiButton></UiButton>
</template>
<script setup lang="ts">
defineOptions({
	name: 'HomePage',
})
</script>
```
@tab pages/home/index.route.ts
```typescript
export default {
	path: '/',
	component: () => import('../../layout'),
	children: [
		{
			path: 'home',
			component: () => import('./index.vue'),
		},
	],
}
```

:::
