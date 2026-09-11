<template>
	<div class="demo-container">
		<ui-number :size="24" primary>$123,456</ui-number>
		<ui-number success large>99.99%</ui-number>
		<ui-number error>-50</ui-number>
		<ui-number italic>1997.07.01</ui-number>
		<ui-number bold>2025</ui-number>
		<ui-number larger light>￥2000</ui-number>
	</div>
</template>

<script setup lang="ts">
import { UiNumber } from '@e-cloud/eslink-plus';
</script>

<style scoped>
.demo-container {
	height: auto;
	display: flex;
	gap: 25px;
	align-items: flex-end;
}
</style>
