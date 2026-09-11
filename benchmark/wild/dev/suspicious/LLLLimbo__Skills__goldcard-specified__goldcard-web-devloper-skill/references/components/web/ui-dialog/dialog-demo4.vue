<template>
	<div class="demo-container">
		<ui-button @click="handleOpenDialog">UiDialog</ui-button>
		<UiDialog
			v-model="dialogVisible"
			title="自定义头部"
			width="500"
			is-title-ellipsis
			:scrollbar-options="scrollbarOptions"
			:only-show-close-button="false"
			@confirm="handleDialogfConfirm"
			@cancel="handleDialogCancel"
			@open="handleDialogOpen"
			@close="handleDialogClose"
		>
			<div style="height: 800px">自定义内容</div>
		</UiDialog>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const dialogVisible = ref(false);
const scrollbarOptions = {
	maxHeight: '30vh',
};
const handleOpenDialog = () => {
	dialogVisible.value = true;
};
const handleDialogfConfirm = () => {
	console.log('UidDialog 确定按钮点击');
};
const handleDialogCancel = () => {
	console.log('UidDialog 取消按钮点击');
};
const handleDialogOpen = () => {
	console.log('UiDialog 打开');
};
const handleDialogClose = () => {
	console.log('UiDialog 关闭');
};
</script>

<style scoped>
.demo-container {
  height: 400px;
}
</style>
