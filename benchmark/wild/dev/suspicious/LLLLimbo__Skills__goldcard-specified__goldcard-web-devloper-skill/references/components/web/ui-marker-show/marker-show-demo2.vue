<template>
	<div class="demo-container">
		<UiMarkerShow
			ref="mapRef"
			:inChina="false"
			language="en"
			@ready="ready"
		></UiMarkerShow>
	</div>
</template>

<script setup lang="ts">
import { UiMarkerShow } from '@e-cloud/eslink-plus';
import { reactive, ref } from 'vue';

const mapRef = ref(null);
const list = reactive([
	{
		text: '测试文本',
		iconOptions: {
			width: 24,
			height: 29,
		},
		position: [116.397428, 39.90923],
		textStyle: {
			'font-size': '12px',
		},
		otherOptions: {},
	},
]);

const ready = ({ mapInstance, map }) => {
	const markerList = [];
	list.forEach((item) => {
		const marker = mapRef.value.addMarker(mapInstance, item);
		markerList.push(marker);
	});
	mapRef.value.fitMapboxView(mapInstance, markerList);
};
</script>

<style scoped lang="scss">
.demo-container {
	height: 400px;
}
</style>
