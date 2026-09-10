<template>
	<ui-button @click="handleOpenDrawer">UiDrawer</ui-button>
	<ui-button @click="handleOpenDrawer400">UiDrawer 自定义宽度</ui-button>
	<ui-button @click="handleOpenDrawerFooter">UiDrawer 自定义按钮</ui-button>
	<UiDrawer
		v-model="drawerVisible"
		title="高级搜索"
		@confirm="handleDialogfConfirm"
		@cancel="handleDialogCancel"
		@open="handleDialogOpen"
		@close="handleDialogClose"
	>
		<div>自定义内容</div>
	</UiDrawer>
	<UiDrawer
		v-model="drawerVisible400"
		title="高级搜索"
		size="400px"
		@confirm="handleDialogfConfirm"
		@cancel="handleDialogCancel"
		@open="handleDialogOpen"
		@close="handleDialogClose"
	>
		<div>自定义内容</div>
	</UiDrawer>
	<UiDrawer
		v-model="drawerVisibleFooter"
		title="高级搜索"
		@open="handleDialogOpen"
		@close="handleDialogClose"
	>
    <p>抽屉内容</p>

    <template #footer>
      <ui-button plain @click="handleCancel">放弃</ui-button>
      <ui-button type="info" @click="handleConfirm">保存</ui-button>
    </template>
	</UiDrawer>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { UiDrawer } from '@e-cloud/eslink-plus';

const drawerVisible = ref(false);
const drawerVisible400 = ref(false);
const drawerVisibleFooter = ref(false);
const handleOpenDrawer = () => {
	drawerVisible.value = true;
};
const handleOpenDrawer400 = () => {
	drawerVisible400.value = true;
};
const handleOpenDrawerFooter = () => {
	drawerVisibleFooter.value = true;
};
const handleDialogfConfirm = () => {
	console.log('UidDialog 确定按钮点击');
};
const handleDialogCancel = () => {
	console.log('UidDialog 取消按钮点击');
};
const handleDialogOpen = () => {
	console.log('UiDialog 打开');
};
const handleDialogClose = () => {
	console.log('UiDialog 关闭');
};

const handleConfirm = () => {
  console.log('确认操作')
  drawerVisibleFooter.value = false
}

const handleCancel = () => {
  console.log('取消操作')
  drawerVisibleFooter.value = false
}
</script>
