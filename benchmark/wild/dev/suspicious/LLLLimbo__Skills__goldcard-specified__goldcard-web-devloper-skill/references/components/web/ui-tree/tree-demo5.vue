<template>
	<UiTree
		node-key="id"
		:data="data"
		:show-edit="true"
		:use-native-tree="false"
		@confirm-edit="handleEdit"
	></UiTree>
</template>
<script setup lang="ts">
import { UiTree } from '@e-cloud/eslink-plus';

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

const handleEdit = ({ type, data, value }) => {
	console.log('点击节点', type, data, value);
};
</script>
