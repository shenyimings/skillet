<template>
		<UiFilterWrapper
			:filters="filters"
			:params="params"
			@filter-change="handleFilterChange"
			@ready="handleReady"
			@refresh="handleRefresh"
		>
			默认插槽内容区
		</UiFilterWrapper>
</template>

<script setup lang="ts">
import type { UiFilterWrapperFilterConfig } from '@e-cloud/eslink-plus'
import { ref } from 'vue'

const filters: UiFilterWrapperFilterConfig = {
	simple: [
		{
			type: 'comboInput',
			label: '快速筛选',
			field: 'keyword',
			placeholder: '请输入关键字',
			options: [
				{ label: '客户', value: 'customer' },
				{ label: '地址', value: 'address' },
			],
			showFilterIcon: true,
		},
	],
	advanced: [
		{
			label: '客户编号',
			field: 'custCode',
			type: 'input',
			placeholder: '请输入客户编号',
		},
		{
			label: '客户类型',
			field: 'custType',
			type: 'select',
			placeholder: '请选择客户类型',
			options: [
				{ label: '居民', value: 2 },
				{ label: '非居', value: 1 },
			],
		},
		{
			label: '手机号',
			field: 'phone',
			type: 'input',
			placeholder: '请输入手机号',
			attrs: {
				inputMode: 'tel',
				type: 'tel',
			},
		},
		{
			label: '开户日期',
			field: 'openDate',
			type: 'date',
			placeholder: '请选择开户日期',
		},
		{
			label: '用户标签',
			field: 'tagType',
			type: 'select',
			attrs: {
				multiple: true,
				collapseTags: true,
				collapseTagsTooltip: true,
				clearable: true,
			},
			placeholder: '请选择客户标签',
			options: [
				{ label: '低保户', value: 13 },
				{ label: '灰名单', value: 12 },
				{ label: '黑名单', value: 11 },
				{ label: '光荣之家', value: 10 },
			],
		},
	],
}

const params = ref({
	keyword: ['', 'customer'],
})

const handleFilterChange = params => {
	console.log(params)
}

const handleReady = () => {
	console.log('ready')
}

const handleRefresh = () => {
	console.log('refresh')
}
</script>

<style scoped>
.ui-filter-wrapper {
	height: 500px;
}
</style>
