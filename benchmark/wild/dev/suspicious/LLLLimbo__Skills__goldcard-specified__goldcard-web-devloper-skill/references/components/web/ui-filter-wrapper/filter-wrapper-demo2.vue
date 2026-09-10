<template>
		<UiFilterWrapper
			:filters="{ simple: filters.simple }"
			:params="params"
			@filter-change="handleFilterChange"
			@ready="handleReady"
			@refresh="handleRefresh"
		>
			默认插槽内容区
		</UiFilterWrapper>
		<ui-divider></ui-divider>
		<UiFilterWrapper
			:filters="filters2"
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
}

const filters2: UiFilterWrapperFilterConfig = {
	simple: [
		{
			type: 'input',
			label: '快速筛选',
			field: 'customer',
			placeholder: '请输入客户名称',
			showFilterIcon: true,
		},
	],
}

const params = ref({
	keyword: ['', 'customer'],
	customer: ''
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
	height: 70px;
}
</style>