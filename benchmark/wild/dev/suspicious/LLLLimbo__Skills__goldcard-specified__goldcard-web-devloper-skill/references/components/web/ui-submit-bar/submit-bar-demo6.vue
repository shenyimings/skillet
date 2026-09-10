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
		>
			<template #left>
				<div style="display: flex; align-items: center; gap: 10px">
					<span>总计: ¥ 256.00</span>
					<el-tag type="info">3件商品</el-tag>
				</div>
			</template>
		</UiSubmitBar>
	</div>
</template>

<script setup lang="ts">
import { UiSubmitBar, UiMessage } from '@e-cloud/eslink-plus'

const handleSubmit = () => {
	UiMessage({
		message: '提交成功',
		type: 'success',
	})
}

const handleCancel = () => {
	UiMessage({
		message: '操作已取消',
		type: 'info',
	})
}
</script>