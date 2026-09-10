<template>
	<ui-simple-form
		v-model="formData"
		:inputs="inputs"
		:cols="2"
		@finish="handleFinish"
	/>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const formData = ref({
	basicInfo: {},
	contactInfo: {}
})

const inputs = [
	{
		type: 'step',
		field: 'step1',
		label: '基本信息'
	},
	{
		field: 'name',
		label: '姓名',
		type: 'input',
		placeholder: '请输入姓名'
	},
	{
		field: 'age',
		label: '年龄',
		type: 'number',
		placeholder: '请输入年龄'
	},
	{
		type: 'step',
		field: 'step2',
		label: '联系方式'
	},
	{
		field: 'phone',
		label: '手机号',
		type: 'input',
		placeholder: '请输入手机号码'
	},
	{
		field: 'email',
		label: '邮箱',
		type: 'input',
		placeholder: '请输入邮箱地址'
	},
	{
		type: 'step',
		field: 'step3',
		label: '其他信息'
	},
	{
		field: 'address',
		label: '地址',
		type: 'textarea',
		placeholder: '请输入详细地址',
		span: 2,
		attrs: {
			rows: 3
		}
	}
]

const handleFinish = (values) => {
	console.log('分步表单提交:', values)
	alert('分步表单完成！')
}
</script>