<template>
	<UiButton @click="open">Show message</UiButton>
</template>
<script lang="ts" setup>
import { UiMessage } from '@e-cloud/eslink-plus';

const open = () => {
	UiMessage({
		type: 'success',
		showClose: true,
		message: 'This is a message.',
	});
};
</script>
