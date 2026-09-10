<template>
	<div class="demo-container">
		<ui-select
			v-model="selectedValue"
			:options="options"
			placeholder="请选择"
			@change="handleChange"
		/>
		<h4>禁用</h4>
		<ui-select
			v-model="selectedValue"
			:options="options"
			placeholder="请选择"
			disabled
			@change="handleChange"
		/>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { UiSelect } from '@e-cloud/eslink-plus';

const selectedValue = ref('');

const options = [
	{ value: 'option1', label: '选项1' },
	{ value: 'option2', label: '选项2' },
	{ value: 'option3', label: '选项3', disabled: true },
];

const handleChange = (value) => {
	console.log('选中值:', value);
};
</script>

<style scoped>
.demo-container {
	display: flex;
	flex-direction: column;
	height: auto;
}
</style>
