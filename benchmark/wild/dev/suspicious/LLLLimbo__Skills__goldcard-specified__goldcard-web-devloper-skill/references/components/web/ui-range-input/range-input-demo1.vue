<template>
	<div>
		<ui-range-input
			v-model="rangeValue"
			:size="'default'"
			:clearable="true"
			:name="['start', 'end']"
			@change="handleRangeChange"
		/>

		<p>当前范围值: [{{ rangeValue[0] }}, {{ rangeValue[1] }}]</p>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const rangeValue = ref([0, 100])

const handleRangeChange = (newRange: string[]) => {
  console.log('范围值变化:', newRange)
}
</script>
