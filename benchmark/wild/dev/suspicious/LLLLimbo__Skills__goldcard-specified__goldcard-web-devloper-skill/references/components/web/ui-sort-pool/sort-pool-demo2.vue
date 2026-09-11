<template>
	<div>
		<div class="mode-toggle">
			<ui-button
				:type="checkable ? 'primary' : 'default'"
				@click="toggleCheckable"
				>切换可选择功能</ui-button
			>
			<ui-button
				:type="direction === 'horizontal' ? 'primary' : 'default'"
				@click="toggleDirection"
				>排列方向: {{ direction === 'horizontal' ? '水平' : '垂直' }}</ui-button
			>
		</div>
		<div v-if="checkable" class="mode-toggle">
			<ui-button
				:type="checkableCheck ? 'primary' : 'default'"
				@click="setCheckableChecker"
				>切换元素2可选择状态</ui-button
			>
			<ui-button
				:type="draggableCheck ? 'primary' : 'default'"
				@click="setDraggableChecker"
				>切换元素可拖拽判定函数</ui-button
			>
			<ui-button
				:type="droppableCheck ? 'primary' : 'default'"
				@click="setDroppableChecker"
				>切换元素可放置判定函数</ui-button
			>
		</div>
		<UiSortPool
			ref="sortPool"
			:source="calcSource"
			:checkable="checkable"
			:draggable-check="draggableCheck"
			:droppable-check="droppableCheck"
			:checkable-check="checkableCheck"
			:direction="direction"
			@change="handleSortChange"
		></UiSortPool>
		<p style="margin-bottom: 0;">排序后的数据: {{ sortedText }}</p>
	</div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

const checkable = ref(false);
const sortPool = ref(null);
const source = ref([
	{
		prop: 'element1',
		label: '元素1',
	},
	{
		prop: 'element2',
		label: '元素2',
	},
	{
		prop: 'element3',
		label: '元素3',
	},
	{
		prop: 'element4',
		label: '元素4',
	},
]);

const sortedText = ref('');

const toggleCheckable = () => {
	checkable.value = !checkable.value;
};

const calcSource = computed(() => {
	return !checkable.value
		? source.value
		: source.value.map((item) => ({ ...item, checked: true }));
});

const handleSortChange = (sortedData) => {
	sortedText.value = sortedData.map((item) => item.label).join('、');
};

const draggableCheck = ref(null);
const checkableCheck = ref(null);
const droppableCheck = ref(null);

const setDraggableChecker = () => {
	if (draggableCheck.value) {
		draggableCheck.value = null;
	} else {
		draggableCheck.value = (item) => item.checked !== false;
	}
};

const setCheckableChecker = () => {
	if (checkableCheck.value) {
		checkableCheck.value = null;
	} else {
		checkableCheck.value = (item) => item.prop !== 'element2';
	}
};

const setDroppableChecker = () => {
	if (droppableCheck.value) {
		droppableCheck.value = null;
	} else {
		droppableCheck.value = (_, list) => {
			return list.map((item) => item.checked !== false);
		};
	}
};

const direction = ref('horizontal');

const toggleDirection = () => {
	direction.value = direction.value === 'horizontal' ? 'vertical' : 'horizontal';
};
</script>

<style lang="scss">
.mode-toggle {
	margin-bottom: 15px;
	display: flex;
}
.ui-sort-item {
	padding: 0 12px;
}
</style>
