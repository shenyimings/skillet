<template>
	<UiSidebar
		v-model="current"
		:options="list"
		@change="handlerChange"
	></UiSidebar>
</template>
<script lang="ts" setup>
import { ref } from 'vue';
import UiSidebar from '@e-cloud/eslink-plus-uniapp/components/ui-sidebar/ui-sidebar.vue';

const handlerChange = (val: string) => {
	console.log(val);
};
const current = ref('1');
const list = ref([
	{
		label: '选项一',
		value: '1',
	},
	{
		label: '选项二',
		value: '2',
	},
	{
		label: '选项三',
		value: '3',
	},
]);
</script>
