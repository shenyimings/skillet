<template>
	<div class="icon-demo-container">
		<ui-icon name="iconfont-plus icon-plus-close-circle-line" color="#409EFF" :size="16" />
		<ui-icon name="iconfont-plus icon-plus-save-line" color="#67C23A" :size="24" />
		<ui-icon name="iconfont-plus icon-plus-filter-line" color="#F56C6C" :size="32" />
		<ui-icon name="iconfont-plus icon-plus-information-line" color="#909399" :size="48" />
	</div>
</template>

<script setup lang="ts">
import { UiIcon } from '@e-cloud/eslink-plus'
</script>

<style scoped>
@import url("https://download-app.eslink.com/iconfonts/新版PC端公共组件库/v1.0.0/iconfont-plus.css");
.icon-demo-container {
	display: flex;
	gap: 20px;
	align-items: center;
	height: auto;
}
</style>
