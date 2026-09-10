<template>
	<UiTree
		:data="treeData"
		:use-native-tree="false"
		:tree-custom="true"
		:before-click="true"
		:before-click-method="handleBeforeClick"
		@node-click="handleNodeClick"
	></UiTree>
</template>
<script setup lang="ts">
import type {
	UiTreeData,
	UiTreeNodeData,
	UiTreeNode,
} from '@e-cloud/eslink-plus';

import { UiTree, UiMessageBox } from '@e-cloud/eslink-plus';
type BeforeClick = (
	data: UiTreeNodeData,
	node: UiTreeNode,
	callback: (allow: boolean) => void,
	event: MouseEvent
) => void;

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
const handleBeforeClick: BeforeClick = (data, node, callback, e) => {
	const { label } = node;
	console.log('before click', label);
	UiMessageBox.alert(`是否切换节点到${label}`, '提示', {
		showCancelButton: true,
		confirmButtonText: '确定',
		cancelButtonText: '取消',
		callback: (action) => {
			if (action === 'confirm') {
				callback(true);
			} else {
				callback(false);
			}
		},
	});
};
const handleNodeClick = (
	data: UiTreeNodeData,
	node: UiTreeNode,
	nodeComponent: any,
	event: MouseEvent
) => {
	console.log('Node clicked接受:', data, node, nodeComponent, event);
};
</script>
