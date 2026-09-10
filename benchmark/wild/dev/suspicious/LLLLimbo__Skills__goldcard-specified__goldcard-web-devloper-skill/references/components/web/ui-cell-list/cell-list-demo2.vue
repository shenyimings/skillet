<template>
	<UiCellList
		:data="cellData"
		item-direction="vertical"
		align="end"
	></UiCellList>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { UiCellItem } from '@e-cloud/eslink-plus';

const cellData = ref<UiCellItem[]>([
	{
		label: '用户号',
		value: '1100002',
		justify: 'space-between',
	},
	{
		label: '地址描述',
		value: '河北省石家庄市长安区荣盛华府04栋01单元3001室',
		justify: 'space-between',
	},
	{
		label: '管理组织',
		value: '长安区服务站',
		justify: 'space-between',
	},
	{
		label: '片区',
		value: '中山办事处',
		justify: 'space-between',
	},
]);
</script>
