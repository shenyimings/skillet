<template>
	<div class="demo-container">
		<ui-pop-confirm
			title="确认删除"
			message="确定要删除这条数据吗？此操作不可撤销。"
			@confirm="handleConfirm"
			@cancel="handleCancel"
		>
			<template #reference>
				<ui-button type="danger">删除</ui-button>
			</template>
		</ui-pop-confirm>
		<ui-pop-confirm
			@confirm="handleConfirm"
			@cancel="handleCancel"
		>
			<template #reference>
				<ui-button>复杂内容</ui-button>
			</template>

			<template #message>
				<ui-icon icon="iconfont icon-attachment-2"></ui-icon>
				<ui-number>2025.09.20</ui-number>
				<p>确定要删除 {{ text }} 吗？</p>
			</template>
		</ui-pop-confirm>
	</div>
</template>

<script setup lang="ts">
import { UiPopConfirm, UiButton } from '@e-cloud/eslink-plus';

const handleConfirm = () => {
	console.log('用户确认删除');
};

const handleCancel = () => {
	console.log('用户取消删除');
};

const text = '数据';
</script>

<style scoped>
.demo-container {
	height: auto;
}
</style>
