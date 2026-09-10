<template>
	<div class="empty-demo-list">
		<UiEmpty />
		<UiEmpty type="service" />
		<UiEmpty type="data" />
		<UiEmpty type="auth" />
		<UiEmpty type="choose" />
		<UiEmpty description="自定义描述" />
	</div>
</template>

<style>
.empty-demo-list {
	display: flex;
	flex-wrap: wrap;
	gap: 30px;
	flex: 1;

	.ui-empty {
		width: 30%;
		height: 200px;
	}
}
</style>
