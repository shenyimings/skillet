<template>
	<ui-simple-form v-model="formData" :inputs="inputs" />
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type { UiFormItem } from '@e-cloud/eslink-plus';

const custTypeOptions = [
	{ label: '工商户', value: 0 },
	{ label: '居民户', value: 1 },
];

const custType2Options = [
	{ label: '商业', value: 0, parentId: 0 },
	{ label: '工业', value: 1, parentId: 0 },
	{ label: '公福', value: 2, parentId: 0 },
	{ label: '自用', value: 3, parentId: 0 },
	{ label: '居民', value: 4, parentId: 1 },
	{ label: '低保', value: 5, parentId: 1 },
];

const inputs: UiFormItem[] = [
	{
		label: '客户大类',
		field: 'custType',
		type: 'select',
		options: custTypeOptions,
	},
	{
		label: '客户细类',
		field: 'custType2',
		type: 'select',
		options: custType2Options,
	},
	{
		label: '备注',
		field: 'remark',
		innerType: 'textarea',
		cols: 2,
		computeFrom: {
			fields: ['custType', 'custType2'],
			trigger: 'change',
			computer: (value, custType, custType2) => {
        console.log(value, custType, custType2);
        const custTypeText = custTypeOptions.find((item) => item.value === custType)?.label || '-';
				const custType2Text = custType2Options.find((item) => item.value === custType2)?.label || '-';
				return `客户类型：${custTypeText}/${custType2Text}`;
			},
		},
	},
];

const formData = ref({
	custType: 0,
	custType2: 0,
	remark: '',
});
</script>
