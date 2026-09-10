<template>
	<div class="mb-4">
		<UiButton @click="open1"> success notification </UiButton>
	</div>
	<div class="mb-4">
		<UiButton @click="open2"> info notification </UiButton>
	</div>
	<div class="mb-4">
		<UiButton @click="open3"> error notification </UiButton>
	</div>
	<div class="mb-4">
		<UiButton @click="open4"> warning notification </UiButton>
	</div>
</template>

<script lang="ts" setup>
import { UiNotification } from '@e-cloud/eslink-plus';

const open1 = () => {
	UiNotification({
		title: 'Prompt',
		message: 'This is a message that does not automatically close',
		duration: 0,
		type: 'success',
	});
};
const open2 = () => {
	UiNotification({
		title: 'Prompt',
		message: 'This is a message that does not automatically close',
		duration: 0,
	});
};
const open3 = () => {
	UiNotification({
		title: 'Prompt',
		message: 'This is a message that does not automatically close',
		duration: 0,
		type: 'error',
	});
};
const open4 = () => {
	UiNotification({
		title: 'Prompt',
		message: 'This is a message that does not automatically close',
		duration: 0,
		type: 'warning',
	});
};
</script>
