<template>
	<ui-combo-input
		v-model="inputValue"
		v-model:selectValue="selectValue"
		:options="options"
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
];

const handleChange = ({ input, select }) => {
	console.log('输入值:', input);
	console.log('选择值:', select);
};
</script>
