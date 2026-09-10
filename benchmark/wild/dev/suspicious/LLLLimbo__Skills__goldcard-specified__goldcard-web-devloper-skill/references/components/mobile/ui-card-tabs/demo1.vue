<template>
	<UiCardTabs v-model="current" :options="list" @change="handlerChange">
		<div style="position: relative" v-if="current === '1'">内容1</div>
		<div style="position: relative" v-if="current === '2'">内容2</div>
	</UiCardTabs>
</template>
<script lang="ts" setup>
import { ref } from 'vue';
import UiCardTabs from '@e-cloud/eslink-plus-uniapp/components/ui-card-tabs/ui-card-tabs.vue';

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
]);
</script>
