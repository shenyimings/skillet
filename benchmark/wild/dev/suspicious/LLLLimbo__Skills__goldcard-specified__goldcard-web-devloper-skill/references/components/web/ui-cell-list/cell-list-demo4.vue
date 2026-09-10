<template>
	<UiCellList :data="cellData" list-direction="vertical" cols="1" align="end" label-width="100px"></UiCellList>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { UiCellItem } from '@e-cloud/eslink-plus'

const cellData = ref<UiCellItem[]>([
	{
		label: '用户号',
		value: '1100002',
	},
	{
		label: '地址描述',
		value: '河北省石家庄市长安区荣盛华府04栋01单元3001室',
	},
	{
		label: '管理组织',
		value: '长安区服务站',
	},
	{
		label: '片区',
		value: '中山办事处',
	},
])
</script>
