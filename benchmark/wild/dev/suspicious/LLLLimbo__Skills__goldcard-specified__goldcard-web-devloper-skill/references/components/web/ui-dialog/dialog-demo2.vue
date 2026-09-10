<template>
	<div class="demo-container">
		<ui-button @click="dialogVisible = true">自定义底部按钮</ui-button>
		<UiDialog
			v-model="dialogVisible"
			title="自定义底部按钮"
			width="500px"
			:show-confirm-button="true"
			:show-cancel-button="true"
			confirm-button-text="同意"
			cancel-button-text="拒绝"
			@confirm="handleConfirm"
			@cancel="handleCancel"
		>
			<p>这个对话框展示了如何自定义底部按钮的文本。</p>
		</UiDialog>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const dialogVisible = ref(false);

const handleConfirm = () => {
	console.log('用户同意了');
	dialogVisible.value = false;
};

const handleCancel = () => {
	console.log('用户拒绝了');
	dialogVisible.value = false;
};
</script>

<style scoped>
.demo-container {
  height: 400px;
}
</style>
