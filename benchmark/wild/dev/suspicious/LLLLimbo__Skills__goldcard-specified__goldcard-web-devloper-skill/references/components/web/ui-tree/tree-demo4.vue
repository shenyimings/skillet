<template>
	<UiTree
		:data="treeData"
		:use-native-tree="false"
		:tree-custom="true"
		@node-click="handleNodeClick"
	>
		<template #label-before="{ data }">前插槽</template>
		<template #label-after="{ data }">后插槽</template>
		<template #row-right="{ data }">最右侧插槽</template>
		<template #empty>没有数据</template>
	</UiTree>
</template>
<script setup lang="ts">
import type {
	UiTreeData,
	UiTreeNodeData,
	UiTreeNode,
} from '@e-cloud/eslink-plus';
import { UiTree } from '@e-cloud/eslink-plus';
const treeData: UiTreeData = [
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
const handleNodeClick = (
	data: UiTreeNodeData,
	node: UiTreeNode,
	nodeComponent: any,
	event: MouseEvent
) => {
	console.log('Node clicked接受:', data, node, nodeComponent, event);
};
</script>
