<template>
	<ui-panel
		title="面板标题"
		:border="true"
		:scrollable="true"
		@action="handleFullScreen"
	>
		<template #header-right>
			<ui-button size="small" style="margin-left: auto"
				>自定义操作</ui-button
			>
		</template>

		<div>面板内容区域</div>

		<template #footer>
			<div style="text-align: right">
				<ui-button>确定</ui-button>
				<ui-button type="default">取消</ui-button>
			</div>
		</template>
	</ui-panel>
</template>

<script setup lang="ts">
import { UiPanel, UiButton } from '@e-cloud/eslink-plus';

const handleFullScreen = () => {
	console.log('全屏操作');
};
</script>
