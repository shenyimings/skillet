<template>
		<ui-input v-model="coordinate" @click.stop="drawerVisible = true" style="width: 50%">
			<template #prepend>
				<ui-button :icon="Position" @click="drawerVisible = true" />
			</template>
		</ui-input>
		<UiDrawer
			v-model="drawerVisible"
			:scrollable="false"
			:model="true"
			title="选择位置坐标"
			@confirm="handleDialogConfirm"
			@open="handleDialogOpen"
		>
			<UiMarkerSearch
				v-if="drawerVisible"
				ref="mapRef"
				id="map-box1"
				:inChina="inChina"
				style="height: 100%"
				:mapConfig="mapConfig"
			/>
		</UiDrawer>
</template>

<script setup lang="ts">
import type { UiAMap, UiMapbox, AddressObj } from '@e-cloud/eslink-plus'
import { Position } from '@e-cloud/eslink-plus'
import { ref, reactive, computed } from 'vue'

const data = reactive<AddressObj>({
	lng: '120.20986478131961',
	lat: '30.29584227496905',
	address: '杭州火车站公交站',
})
const coordinate = ref(data.lng + ',' + data.lat)
const inChina = ref(true)
const mapRef = ref<UiAMap | UiMapbox>({} as UiAMap | UiMapbox)
const mapConfig = computed(() => {
	return inChina.value
		? { center: undefined, zoom: 15 }
		: { center: [116.39118683763206, 39.90782876528027], zoom: 15 }
})

const drawerVisible = ref(false)

const handleDialogConfirm = () => {
	const { lng, lat, address } = mapRef.value.getAddress()
	coordinate.value = lng && lat ? lng + ',' + lat : ''
	data.lng = lng
	data.lat = lat
	data.address = address
	drawerVisible.value = false
}
const handleDialogOpen = () => {
	if (data.address) {
		setTimeout(() => {
			mapRef.value?.search(data.address, () => {
				mapRef.value?.autoInput.focus()
			})
		}, 500)
	}
}
</script>
