<template>
	<UiTimeline :data="updateLogs" align="left">
		<template #default="{ data }">
			<div class="demo-content">
				<h3 v-if="data?.title" class="demo-content-title">
					{{ data.title }}
					<UiButton size="small">详情</UiButton>
				</h3>
				<img
					v-else
					src="http://iph.href.lu/60x60?bg=cccccc"
					class="image-placeholder"
					alt="未知"
				/>
				<div class="demo-content-text">
					<div class="">{{ data.content }}</div>
				</div>
				<div class="demo-content-datetime">{{ data.datetime }}</div>
			</div>
		</template>
	</UiTimeline>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { UiTimelineItem } from '@e-cloud/eslink-plus';

const updateLogs = ref<UiTimelineItem[]>([
	{
		datetime: '2023-08-10 10:00:00',
		content: '新增功能：支持自定义配置',
		title: '张三',
		typeDesc: '业务类型',
	},
	{
		datetime: '2023-08-09 14:30:00',
		content: '修复了一些已知问题',
		typeDesc: '业务类型',
	},
	{
		datetime: '2023-08-08 18:45:00',
		content: '优化了用户体验',
		typeDesc: '业务类型',
	},
	{
		datetime: '2023-08-07 12:15:00',
		content: '发布了初始版本',
		typeDesc: '业务类型',
	},
]);
</script>

<style scoped>
.demo-content {
	display: flex;
	flex-direction: column;
	gap: var(--gap-8);
	padding-top: var(--gap-12);
}

.demo-content-title {
	display: flex;
	align-items: center;
	justify-content: space-between;
	width: 100%;
	margin: 0;
	font-size: 16px;
	font-weight: 600;
}

.demo-content-text {
	padding: var(--gap-20, 20px);
	font-size: var(--font-body-md, 14px);
	line-height: 1.4;
	background-color: var(--light-bg-base, rgba(255, 255, 255, 72%));
	border: 1px solid var(--light-border-split, rgb(220, 225, 238));
	border-radius: var(--radius-lg, 4px);
}

.demo-content-datetime {
	font-size: var(--font-body-md, 14px);
	color: var(--light-text-secondary, rgb(95, 103, 125));
}

.image-placeholder {
	width: 60px;
	height: 60px;
	border-radius: var(--radius-lg);
}
</style>
