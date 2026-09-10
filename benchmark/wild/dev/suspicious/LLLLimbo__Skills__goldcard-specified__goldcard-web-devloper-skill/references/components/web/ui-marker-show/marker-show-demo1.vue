<template>
	<div class="demo-container">
		<UiMarkerShow
			ref="mapRef"
			@ready="ready"
			@marker-click="clickMarker"
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
	// 调整地图视图以适配所有标记点
	mapInstance.setFitView(
		markerList, // 覆盖物数组
		false, // 动画过渡到制定位置
		[60, 60, 60, 60], // 周围边距，上、下、左、右
		16 // 最大 zoom 级别
	);
};

const clickMarker = ({ lng, lat }) => {
	console.log('点击marker', lng, lat);
};
</script>

<style scoped lang="scss">
.demo-container {
	height: 400px;
}
</style>
