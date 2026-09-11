<template>
	<div class="demo-container">
		<ui-button @click="showAlert">显示警告框</ui-button>
		<ui-button @click="showConfirm">显示确认框</ui-button>
		<ui-button @click="showPrompt">显示输入框</ui-button>
	</div>
</template>

<script setup lang="ts">
import { UiMessageBox } from '@e-cloud/eslink-plus';

const showAlert = () => {
	UiMessageBox.alert('这是一个警告消息', '警告标题');
};

const showConfirm = () => {
	UiMessageBox.confirm('确定要执行此操作吗？', '确认提示')
		.then(() => {
			console.log('用户确认');
		})
		.catch(() => {
			console.log('用户取消');
		});
};

const showPrompt = () => {
	UiMessageBox.prompt('请输入内容：', '输入提示')
		.then((value) => {
			console.log('用户输入:', value);
		})
		.catch(() => {
			console.log('用户取消');
		});
};
</script>

<style scoped>
.demo-container {
	height: auto;
}
</style>
