<template>
	<ui-tree
		:data="treeData"
		:props="treeProps"
		:tree-custom="true"
		:use-native-tree="false"
		node-key="id"
		@node-click="handleNodeClick"
	>
		<template #label-before="{ data }">
			<ui-icon name="folder" />
		</template>

		<template #label-after="{ data }">
			<span class="node-count">({{ data.children?.length || 0 }})</span>
		</template>

		<template #row-right="{ data }">
			<ui-button size="mini" @click="editNode(data)">编辑</ui-button>
		</template>

		<template #empty>
			<div class="empty-tree">暂无数据</div>
		</template>
	</ui-tree>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { UiTree, UiIcon, UiButton } from '@e-cloud/eslink-plus';

const treeData = ref([
	{
		id: 1,
		label: '节点一',
		children: [
			{ id: 2, label: '子节点1-1' },
			{ id: 3, label: '子节点1-2' },
		],
	},
	{ id: 4, label: '节点二' },
]);

const treeProps = {
	children: 'children',
	label: 'label',
};

const handleNodeClick = (data, node, nodeComponent, event) => {
	console.log('节点点击:', data);
};

const editNode = (data) => {
	console.log('编辑节点:', data);
};
</script>
