<template>
	<div class="demo-container">
		<ui-icon-button
			name="iconfont-plus icon-plus-information-line"
			color="#409EFF"
			@click="handleSearch"
		/>
		<ui-icon-button
			name="iconfont-plus icon-plus-filter-3-fill"
			color="#67C23A"
			@click="handleEdit"
		/>
		<ui-icon-button
			name="iconfont-plus icon-plus-filter-line"
			color="#F56C6C"
			@click="handleDelete"
		/>
		<ui-icon-button
			name="iconfont-plus icon-plus-save-line"
			color="#909399"
			@click="handleSetting"
		/>
	</div>
	<div class="demo-container" style="margin-top: 20px;">
		尺寸
		<ui-icon-button
			name="iconfont-plus icon-plus-information-line"
			size="large"
			@click="handleSearch"
		/>
		<ui-icon-button
			name="iconfont-plus icon-plus-information-line"
			@click="handleEdit"
		/>
		<ui-icon-button
			name="iconfont-plus icon-plus-information-line"
			size="small"
			@click="handleDelete"
		/>
		<ui-icon-button
			name="iconfont-plus icon-plus-information-line"
			size="mini"
			@click="handleSetting"
		/>
	</div>
</template>

<script setup lang="ts">
import { UiIconButton } from '@e-cloud/eslink-plus'

const handleSearch = () => {
	console.log('搜索按钮点击')
}

const handleEdit = () => {
	console.log('编辑按钮点击')
}

const handleDelete = () => {
	console.log('删除按钮点击')
}

const handleSetting = () => {
	console.log('设置按钮点击')
}
</script>

<style scoped>
@import url("https://download-app.eslink.com/iconfonts/新版PC端公共组件库/v1.0.0/iconfont-plus.css");
.demo-container {
	display: flex;
	gap: 20px;
	align-items: center;
	height: auto;
}
</style>
