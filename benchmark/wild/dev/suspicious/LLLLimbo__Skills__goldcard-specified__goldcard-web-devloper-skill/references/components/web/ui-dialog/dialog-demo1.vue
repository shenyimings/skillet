<template>
	<div class="demo-container">
		<ui-button @click="dialogVisible = true">打开对话框</ui-button>
		<UiDialog
			v-model="dialogVisible"
			title="基础对话框"
			width="500px"
			@confirm="handleConfirm"
			@cancel="handleCancel"
		>
			<p>这是一个基础的对话框示例。</p>
			<p>对话框内容区域可以使用任何Vue组件和HTML元素。</p>
		</UiDialog>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const dialogVisible = ref(false)

const handleConfirm = () => {
	console.log('确认操作')
	dialogVisible.value = false
}

const handleCancel = () => {
	console.log('取消操作')
	dialogVisible.value = false
}
</script>

<style scoped>
.demo-container {
  height: 400px;
}
</style>
