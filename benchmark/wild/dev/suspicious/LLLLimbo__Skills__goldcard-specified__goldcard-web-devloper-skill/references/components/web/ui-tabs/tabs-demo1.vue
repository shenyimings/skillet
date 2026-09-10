<template>
	<UiTabs v-model="activeName" @tab-click="handleClick">
		<UiTabPane label="Tab 1" name="first">Content of Tab Pane 1</UiTabPane>
		<UiTabPane label="Tab 2" name="second">Content of Tab Pane 2</UiTabPane>
	</UiTabs>
</template>
<script lang="ts" setup>
import { ref } from 'vue';
import type { TabsPaneContext } from 'element-plus';

const activeName = ref('first');

const handleClick = (tab: TabsPaneContext, event: Event) => {
	console.log(tab, event);
};
</script>
