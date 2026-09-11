<template>
	<div class="demo-container">
		<ui-result
			icon="success"
			title="操作成功"
			sub-title="您的操作已成功完成"
		>
			<template #extra>
				<ui-button type="primary">返回首页</ui-button>
				<ui-button>查看详情</ui-button>
			</template>
		</ui-result>
	</div>
</template>

<script setup lang="ts">
import { UiResult, UiButton } from '@e-cloud/eslink-plus';
</script>

<style scoped>
.demo-container {
	height: 400px;
	position: relative;
}
</style>
