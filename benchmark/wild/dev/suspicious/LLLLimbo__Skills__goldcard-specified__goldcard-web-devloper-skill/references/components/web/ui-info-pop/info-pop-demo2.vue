<template>
	<div class="info-pop-demo-container">
		<ui-info-pop placement="bottom-start">这里是提示内容</ui-info-pop>
		<ui-info-pop placement="bottom-end">这里是提示内容</ui-info-pop>
		<ui-info-pop placement="left">这里是提示内容</ui-info-pop>
	</div>
</template>

<script setup lang="ts">
import { UiInfoPop } from '@e-cloud/eslink-plus';
</script>

<style scoped lang="scss">
@import url("https://download-app.eslink.com/iconfonts/AI客服一体化平台/v1.0.0/iconfont.css");
.info-pop-demo-container {
	height: auto;
	display: flex;
	gap: 25px;
}
</style>
