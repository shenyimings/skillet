<template>
	<ui-select-list
		v-model="selectedItem"
		:list="items"
		:select-first="true"
		title="选择项列表"
		label-key="name"
		id-key="id"
		@select="handleSelect"
	>
		<template #header>
			<ui-button @click="addItem">添加项</ui-button>
		</template>

		<template #item="{ item }">
			<div class="custom-item">
				<ui-icon name="iconfont-plus icon-plus-information-line" />
				<span>{{ item.name }}</span>
				<span class="description">{{ item.description }}</span>
				<ui-icon
					name="iconfont-plus icon-plus-close-fill"
					class="remove-icon"
					@click="removeItem(item)"
				/>
			</div>
		</template>

		<template #empty>
			<div class="empty-state">暂无数据</div>
		</template>
	</ui-select-list>
	<p style="margin-top: 20px; margin-bottom: 0">
		当前选择: {{ selectedItem?.name || '--' }}
	</p>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { UiSelectList, UiButton, UiIcon } from '@e-cloud/eslink-plus';

const selectedItem = ref(null);
const items = ref([
	{ id: 1, name: '选项一', description: '描述信息' },
	{ id: 2, name: '选项二', description: '描述信息' },
	{ id: 3, name: '选项三', description: '描述信息' },
]);

const handleSelect = (item, index) => {
	console.log('选中项:', item, '索引:', index);
};

const addItem = () => {
	const id = Date.now();
	items.value.push({ id, name: '新选项-' + id, description: '新添加的选项' });
};
const removeItem = (item) => {
	selectedItem.value = null
	items.value = items.value.filter((i) => i.id !== item.id);
};
</script>

<style lang="scss">
.custom-item {
	display: flex;
	align-items: center;
	gap: 10px;

	.remove-icon {
		cursor: pointer;
		margin-left: auto;
	}
}
</style>
