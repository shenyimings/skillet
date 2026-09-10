<template>
	<div class="demo-container">
		<ui-button @click="dialogVisible = true">自定义底部插槽</ui-button>
		<UiDialog
			v-model="dialogVisible"
			title="自定义底部插槽"
			width="500px"
			:show-footer="true"
		>
			<p>这个对话框展示了如何使用自定义底部插槽。</p>

			<template #footer-right="{ confirm, cancel }">
				<ui-button @click="cancel">取消</ui-button>
				<ui-button type="primary" @click="confirm">确定</ui-button>
				<ui-button type="success" @click="handleCustomAction"
					>自定义操作</ui-button
				>
			</template>
			<template #footer-left>
				<ui-button>上一步1</ui-button>
			</template>
		</UiDialog>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const dialogVisible = ref(false);

const handleCustomAction = () => {
	console.log('自定义操作');
};

const handleConfirm = () => {
	console.log('确认操作');
	dialogVisible.value = false;
};

const handleCancel = () => {
	console.log('取消操作');
	dialogVisible.value = false;
};
</script>

<style scoped>
.demo-container {
  height: 400px;
}
</style>
