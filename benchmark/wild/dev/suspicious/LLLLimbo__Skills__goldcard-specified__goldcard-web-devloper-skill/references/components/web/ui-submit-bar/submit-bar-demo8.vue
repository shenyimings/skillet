<template>
	<div
		style="
			height: 300px;
			position: relative;
		"
	>
		<p>这是一个包含提交栏的容器</p>
		<div style="height: 300px;">内容区域...</div>

		<UiSubmitBar
			submit-text="保存"
			cancel-text="放弃"
			@submit="handleSubmit"
			@cancel="handleCancel"
		/>
	</div>
</template>

<script setup lang="ts">
import { UiSubmitBar, UiMessage } from '@e-cloud/eslink-plus';

const handleSubmit = () => {
	UiMessage({
		message: '保存成功',
		type: 'success',
	});
};

const handleCancel = () => {
	UiMessage({
		message: '操作已取消',
		type: 'info',
	});
};
</script>
