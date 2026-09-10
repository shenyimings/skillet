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
npm install @e-cloud/eslink-plus-uniapp --save
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
import UiButton from '@e-cloud/eslink-plus-uniapp/components/ui-button/ui-button.vue'

defineOptions({
	name: 'HomePage',
})
</script>
```
:::
