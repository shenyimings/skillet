<template>
	<ui-button @click="handleClick('100')">滚动到末尾</ui-button>
	<ui-button @click="handleClick('1')">滚动到开始</ui-button>
	<div style="height: 200px">
		<UiTree ref="treeRef" :data="treeData2" :use-native-tree="false"></UiTree>
	</div>
</template>
<script setup lang="ts">
import { ref, nextTick } from 'vue';
import type { UiTreeData, UiTreeComponentProps } from '@e-cloud/eslink-plus';
import { UiTree } from '@e-cloud/eslink-plus';

const generateTreeData = (count: number): UiTreeData => {
	const data: UiTreeData = [];
	for (let i = 1; i <= count; i++) {
		data.push({
			id: i.toString(),
			label: `Level one ${i}`,
		});
	}
	return data;
};

const treeData2: UiTreeData = generateTreeData(100);
const treeRef = ref<UiTreeComponentProps | null>(null);
const handleClick = (id: string) => {
	nextTick(() => {
		treeRef.value?.smoothScrollToTarget({
			id,
			duration: 500,
		});
	});
};
</script>
