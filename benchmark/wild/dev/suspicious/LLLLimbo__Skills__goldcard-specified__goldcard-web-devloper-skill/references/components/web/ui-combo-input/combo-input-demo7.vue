<template>
	<h4 style="margin-top: 0;">自动宽度</h4>
	<ui-combo-input
		v-model="inputValue"
		v-model:selectValue="selectValue"
		:options="options"
		@change="handleChange"
	/>
	<h4>150px</h4>
	<ui-combo-input
		v-model="inputValue"
		v-model:selectValue="selectValue"
		:options="options"
		:select-attrs="{ width: '150px' }"
		@change="handleChange"
	/>
	<h4>80px</h4>
	<ui-combo-input
		v-model="inputValue"
		v-model:selectValue="selectValue"
		:options="options"
		:select-attrs="{ width: '80px' }"
		@change="handleChange"
	/>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const inputValue = ref('');
const selectValue = ref('1');
const options = [
	{ label: '选项1', value: '1' },
	{ label: '选项2', value: '2' },
	{ label: '一个长选项', value: '3' },
];

const handleChange = ({ input, select }) => {
	console.log('输入值:', input);
	console.log('选择值:', select);
};
</script>
