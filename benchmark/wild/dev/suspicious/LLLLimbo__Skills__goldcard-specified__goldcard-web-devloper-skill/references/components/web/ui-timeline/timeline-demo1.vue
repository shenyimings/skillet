<template>
	<UiTimeline :data="updateLogs" />
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
.demo-container {
	padding: 20px;
}
</style>
