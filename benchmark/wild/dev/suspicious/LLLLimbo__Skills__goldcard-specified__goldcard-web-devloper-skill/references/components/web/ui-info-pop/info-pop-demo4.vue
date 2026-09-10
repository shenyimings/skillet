<template>
	<div class="info-pop-demo-container">
		<ui-info-pop effect="light" placement="right-start">
			<UiTable :columns="columns" :data="data" use-pure-table></UiTable>
			<p>
				黑血平台
			  <ui-info-pop placement="right">数据来源: ...</ui-info-pop>
			</p>
		</ui-info-pop>
	</div>
</template>

<script setup lang="ts">
import { UiInfoPop, UiTable } from '@e-cloud/eslink-plus';

const columns = [
	{
		label: '姓名',
		prop: 'name',
	},
	{
		label: '年龄',
		prop: 'age',
	},
	{
		label: '地址',
		prop: 'address',
	},
];

const data = [
	{
		name: '张三',
		age: 20,
		address: '中国',
	},
	{
		name: '李四',
		age: 21,
		address: '中国',
	},
];
</script>

<style scoped lang="scss">
@import url("https://download-app.eslink.com/iconfonts/AI客服一体化平台/v1.0.0/iconfont.css");
.info-pop-demo-container {
	height: auto;
	display: flex;
	gap: 25px;
}
</style>
