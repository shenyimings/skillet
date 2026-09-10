<template>
	<div class="demo-container">
		<div>
			<ui-info-pop> 这里是提示内容 </ui-info-pop>
			<ui-info-pop color="orange"> 这里是提示内容 </ui-info-pop>
			<ui-info-pop color="#FF6600"> 这里是提示内容 </ui-info-pop>
		</div>
		<div>
			<ui-info-pop icon="iconfont icon-attachment-2">
				这里是提示内容
			</ui-info-pop>
			<ui-info-pop size="24"> 这里是提示内容 </ui-info-pop>
		</div>
		<div>
			点击弹出 <ui-info-pop trigger="click"> 这里是提示内容 </ui-info-pop>
		</div>
	</div>
</template>

<script setup lang="ts">
import { UiInfoPop } from '@e-cloud/eslink-plus';
</script>

<style scoped lang="scss">
@import url('https://download-app.eslink.com/iconfonts/AI客服一体化平台/v1.0.0/iconfont.css');
.demo-container {
	height: auto;
	display: flex;
	flex-direction: column;
	gap: 15px;

	& > div {
		display: flex;
		gap: 25px;
	}
}
</style>
