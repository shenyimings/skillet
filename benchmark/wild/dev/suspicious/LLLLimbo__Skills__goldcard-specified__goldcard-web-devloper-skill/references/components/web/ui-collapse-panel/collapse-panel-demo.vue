<template>
  <ui-collapse-panel
    title="标题"
    v-model:expanded="isExpanded"
    @change="handleChange"
  >
    <div>这里是面板内容</div>
  </ui-collapse-panel>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const isExpanded = ref(false)

const handleChange = (expanded: boolean) => {
  console.log('面板状态:', expanded)
}
</script>
