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
			@submit="handleSubmit"
			@cancel="handleCancel"
		/>
	</div>
</template>

<script setup lang="ts">
import { UiSubmitBar } from '@e-cloud/eslink-plus';

const handleSubmit = () => {
	console.log('提交操作');
	alert('数据已保存');
};

const handleCancel = () => {
	console.log('取消操作');
	alert('操作已取消');
};
</script>
