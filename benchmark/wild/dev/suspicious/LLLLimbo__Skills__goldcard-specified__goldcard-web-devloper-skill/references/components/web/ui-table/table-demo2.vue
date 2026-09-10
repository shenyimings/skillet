<template>
	<div class="demo-container">
	<UiTable
		:columns="columns"
		:data="data"
		usePureTable
	/>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { UiTableColumn, UiTableRecord } from '@e-cloud/eslink-plus'

const columns = ref<UiTableColumn[]>([
	{
		label: '姓名',
		prop: 'name',
		width: 180,
	},
	{
		label: '年龄',
		prop: 'age',
		width: 120,
		display: {
			formatter: 'progress',
			type: 'success',
		}
	},
	{
		label: '地址',
		prop: 'address',
		minWidth: 300,
	},
])

const data = ref<UiTableRecord[]>([
	{
		name: '王小明',
		age: 18,
		address: '北京市海淀区',
	},
	{
		name: '张小红',
		age: 20,
		address: '上海市浦东新区',
	},
	{
		name: '李小白',
		age: 25,
		address: '广州市天河区',
	},
])
</script>


<style lang="scss">
.demo-container {
	height: 200px;
}
</style>
