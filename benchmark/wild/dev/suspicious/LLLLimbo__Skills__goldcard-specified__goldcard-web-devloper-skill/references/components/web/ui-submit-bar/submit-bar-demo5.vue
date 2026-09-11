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
			submit-text="删除"
			submit-type="danger"
			confirm-title="确认删除"
			confirm-placement="top-end"
			@submit="handleSubmit"
			@cancel="handleCancel"
		>
			<template #confirm>
				<p>确定要删除这条数据吗？此操作不可撤销。</p>
			</template>
		</UiSubmitBar>
	</div>
</template>

<script setup lang="ts">
import { UiSubmitBar, UiMessage } from '@e-cloud/eslink-plus';

const handleSubmit = () => {
	UiMessage({
		message: '删除成功',
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
