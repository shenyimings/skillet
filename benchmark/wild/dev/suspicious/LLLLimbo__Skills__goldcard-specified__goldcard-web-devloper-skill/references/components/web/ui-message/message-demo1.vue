<template>
	<div class="mb-4">
		<UiButton @click="open1">Show success message</UiButton>
	</div>
	<div class="mb-4">
		<UiButton @click="open2">Show info message</UiButton>
	</div>
	<div class="mb-4">
		<UiButton @click="open3">Show error message</UiButton>
	</div>
	<div class="mb-4">
		<UiButton @click="open4">Show warning message</UiButton>
	</div>
</template>
<script lang="ts" setup>
import { UiMessage } from '@e-cloud/eslink-plus';

const open1 = () => {
	UiMessage({
		type: 'success',
		message: 'This is a message.',
	});
};
const open2 = () => {
	UiMessage({
		message: 'This is a message.',
	});
};
const open3 = () => {
	UiMessage({
		type: 'error',
		message: 'This is a message.',
	});
};
const open4 = () => {
	UiMessage({
		type: 'warning',
		message: 'This is a message.',
	});
};
</script>
