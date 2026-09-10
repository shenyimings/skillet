<template>
	<ui-input
		v-model="inputValue"
		placeholder="请输入内容"
		:show-word-limit="true"
		:maxlength="50"
		@validate="handleValidate"
	/>
	<br/>
	<ui-input
		type="textarea"
		v-model="textValue"
		placeholder="请输入内容"
		:show-word-limit="true"
		:maxlength="200"
		@validate="handleTextValidate"
	/>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { UiInput } from '@e-cloud/eslink-plus';

const inputValue = ref('');
const textValue = ref('');

const handleValidate = (isValid: boolean) => {
	console.log('输入验证结果:', isValid);
};

const handleTextValidate = (isValid: boolean) => {
	console.log('文本输入验证结果:', isValid);
};
</script>
