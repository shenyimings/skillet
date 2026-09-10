<template>
	<UiCodeViewer :code="code" lang="js" />
</template>

<script setup lang="ts">
import { ref } from 'vue'

const code = ref(`function hello() {
  console.log('Hello, World!');
}`)
</script>
