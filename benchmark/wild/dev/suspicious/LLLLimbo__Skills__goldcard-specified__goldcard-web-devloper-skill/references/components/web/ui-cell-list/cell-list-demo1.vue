<template>
	<UiCellList
		:data="cellData"
		item-direction="vertical"
		decoration="underline"
		decoration-color="red"
	></UiCellList>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { UiCellItem } from '@e-cloud/eslink-plus';

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
]);
</script>
