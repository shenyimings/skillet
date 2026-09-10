<template>
	<div class="tree-container">
		<UiTree
			ref="treeRef"
			:data="data"
			:show-filter="true"
			:use-native-tree="false"
			filter-field="label"
			@filter="handleFilter"
		>
		</UiTree>
	</div>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import { UiTree } from '@e-cloud/eslink-plus';

const treeRef = ref(null);
const data = [
	{
		id: '1',
		label: 'Level one 1',
		children: [
			{
				id: '1-1',
				label: 'Level two 1-1',
				children: [{ id: '1-1-1', label: 'Level three 1-1-1' }],
			},
		],
		disabled: true,
	},
	{
		id: '2',
		label: 'Level one 2',
		children: [
			{
				id: '2-1',
				label: 'Level two 2-1',
				children: [{ id: '2-1-1', label: 'Level three 2-1-1' }],
			},
			{
				id: '2-2',
				label: 'Level two 2-2',
				children: [
					{
						id: '2-2-1',
						label: 'Level three 2-2-1',
					},
				],
			},
		],
		disabled: false,
	},
	{
		id: '3',
		label: 'Level one 3',
		children: [
			{
				id: '3-1',
				label: 'Level two 3-1',
				children: [{ id: '3-1-1', label: 'Level three 3-1-1' }],
			},
			{
				id: '3-2',
				label: 'Level two 3-2',
				children: [
					{
						id: '3-2-1',
						label: 'Level three 3-2-1',
					},
				],
			},
		],
	},
];

const handleFilter = (list) => {
	console.log(list);
};
</script>
