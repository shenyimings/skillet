<template>
	<div class="demo-container">
	<UiTable
		:columns="columns"
		:data="data"
		:config="config"
		@action-edit-click="handleEdit"
		@action-delete-click="handleDelete"
		@cell-edit-name-click="handleEditName"
		@selection-change="handleSelectionChange"
	>
		<template #action-left>
			<ui-button type="primary" @click="handleAdd">新增</ui-button>
		</template>
	</UiTable>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { UiTableColumn, UiTableRecord, UiTableConfig } from '@e-cloud/eslink-plus'

const columns = ref<UiTableColumn[]>([
	{
		label: '姓名',
		prop: 'name',
		width: 180,
		display: {
			formatter: 'button',
			type: 'primary',
			action: 'edit-name',
			text: '编辑姓名',
			attrs: {
				size: 'small',
			}
		}
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

const config = ref<UiTableConfig>({
	showPagination: true,
	attrs: {
		border: true,
		stripe: true,
	}
})

const handleEdit = (selection: UiTableRecord[]) => {
	console.log('编辑操作', selection)
}

const handleDelete = (selection: UiTableRecord[]) => {
	console.log('删除操作', selection)
}

const handleEditName = (row: UiTableRecord, column: UiTableColumn) => {
	console.log('编辑姓名', row, column)
}

const handleSelectionChange = (selection: UiTableRecord[]) => {
	console.log('选中记录', selection)
}

const handleAdd = () => {
	console.log('新增操作')
}
</script>


<style lang="scss">
.demo-container {
	height: 400px;
}
</style>
