<template>
	<div
		style="
			height: 300px;
			position: relative;
		"
	>
		<p>隐藏取消按钮</p>
		<div style="height: 300px;">内容区域...</div>

		<UiSubmitBar
			hideCancel
			@submit="handleSubmit"
			@cancel="handleCancel"
		/>
	</div>
</template>

<script setup lang="ts">
import { UiSubmitBar } from '@e-cloud/eslink-plus';

const handleSubmit = () => {
	console.log('提交订单');
	alert('订单提交成功');
};

const handleCancel = () => {
	console.log('返回操作');
};
</script>
