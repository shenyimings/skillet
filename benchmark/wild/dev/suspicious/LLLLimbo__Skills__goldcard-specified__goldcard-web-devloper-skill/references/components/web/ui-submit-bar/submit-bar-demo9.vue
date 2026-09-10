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
			submit-text="收费"
			cancel-text="取消"
			@submit="handleSubmit"
			@cancel="handleCancel"
		>
			<template #submit-suffix>
				<ui-number style="color: inherit">100.00</ui-number>
			</template>
		</UiSubmitBar>
	</div>
</template>

<script setup lang="ts">
import { UiSubmitBar, UiMessage, UiNumber } from '@e-cloud/eslink-plus';

const handleSubmit = () => {
	UiMessage({
		message: '收费成功',
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
