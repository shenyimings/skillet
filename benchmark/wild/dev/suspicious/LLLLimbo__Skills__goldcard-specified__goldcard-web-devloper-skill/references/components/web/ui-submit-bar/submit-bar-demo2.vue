<template>
	<div
		style="
			height: 300px;
			position: relative;
		"
	>
		<p>提交按钮禁用示例</p>
		<div style="height: 300px;">内容区域...</div>

		<UiSubmitBar
			disabled
			@submit="handleSubmit"
			@cancel="handleCancel"
		/>
	</div>
</template>

<script setup lang="ts">
import { UiSubmitBar } from '@e-cloud/eslink-plus';

const handleSubmit = () => {
	console.log('带确认的提交操作');
	alert('数据已提交');
};

const handleCancel = () => {
	console.log('取消操作');
};
</script>
