<template>
  <ui-steps
    :active="active"
    :data="stepsData"
    @change="handleStepChange"
  />
	<UiButton style="margin-top: 25px" @click="next">Next step</UiButton>
</template>
<script lang="ts" setup>
import { ref } from 'vue';

const active = ref(0);

const stepsData = [
  { title: '步骤一', description: '第一步描述' },
  { title: '步骤二', description: '第二步描述' },
  { title: '步骤三', description: '第三步描述' }
]

const next = () => {
	if (active.value++ > 2) active.value = 0;
};

const handleStepChange = (newStep) => {
  console.log('当前步骤:', newStep)
}
</script>
