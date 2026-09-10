<template>
	<UiSearch v-model="searchValue" @change="handlerChange" />
</template>
<script lang="ts" setup>
import { ref } from 'vue';
import UiSearch from '@e-cloud/eslink-plus-uniapp/components/ui-search/ui-search.vue';

const searchValue = ref('');
const handlerChange = (value: string) => {
	console.log(value);
};
</script>
