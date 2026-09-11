<template>
	<ui-simple-form
		v-model="formData"
		:inputs="inputs"
	/>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { UiFormItem } from '@e-cloud/eslink-plus'

const inputs: UiFormItem[] = [
  {
    label: '客户大类',
    field: 'custType',
    type: 'select',
    options: [
      { label: '工商户', value: 0 },
      { label: '居民户', value: 1 },
    ],
    link: [
      {
        field: 'custType2',
        trigger: 'change',
        filter: (option, value) => {
          return value === option.parentId
        }
      },
      {
        field: 'time',
        trigger: 'change',
        visible: value => value === 1
      },
    ],
  },
  {
    label: '客户细类',
    field: 'custType2',
    type: 'select',
    rule: 'required',
    options: [
      { label: '商业', value: 0, parentId: 0 },
      { label: '工业', value: 1, parentId: 0 },
      { label: '公福', value: 2, parentId: 0 },
      { label: '自用', value: 3, parentId: 0 },
      { label: '居民', value: 4, parentId: 1 },
      { label: '低保', value: 5, parentId: 1 },
    ],
  },
  {
    label: '预约时间',
    field: 'time',
    type: 'datetime',
  },
]

const formData = ref({
  custType: 0,
  custType2: 0,
  time: '',
})
</script>
