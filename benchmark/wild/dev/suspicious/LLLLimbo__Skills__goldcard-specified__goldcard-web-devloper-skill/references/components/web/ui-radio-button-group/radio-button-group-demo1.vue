<template>
  <div class="demo-container">
    <ui-radio-button-group
      v-model="selectedValue"
      :options="options"
      size="large"
    />
    <ui-radio-button-group
      v-model="selectedValue"
      :options="options"
    />
    <ui-radio-button-group
      v-model="selectedValue"
      :options="options"
      size="small"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { UiRadioButtonGroup } from '@e-cloud/eslink-plus'

const selectedValue = ref('option1')

const options = [
  { label: '选项一', value: 'option1' },
  { label: '选项二', value: 'option2' },
  { label: '选项三', value: 'option3' }
]
</script>

<style scoped>
.demo-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  align-items: flex-start;
  height: auto;
}
</style>
