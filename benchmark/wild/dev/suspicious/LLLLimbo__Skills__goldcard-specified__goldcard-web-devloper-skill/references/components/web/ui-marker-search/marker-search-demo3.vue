<template>
	<div class="demo-container">
		<UiMarkerSearch
			:inChina="false"
			@ready="ready"
			@marker-click="clickMarker"
			@marker-search="markerSearch"
		></UiMarkerSearch>
	</div>
</template>

<script setup lang="ts">
import { UiMarkerSearch } from '@e-cloud/eslink-plus';

const ready = ({ mapInstance, map }) => {
	console.log('mapInstance', mapInstance, 'map', map);
};
const clickMarker = ({ lng, lat }) => {
	console.log('点击marker', lng, lat);
};
const markerSearch = ({ lng, lat, address }) => {
	console.log('点位', lng, lat, address);
};
</script>

<style scoped>
.demo-container {
	height: 400px;
}
</style>
