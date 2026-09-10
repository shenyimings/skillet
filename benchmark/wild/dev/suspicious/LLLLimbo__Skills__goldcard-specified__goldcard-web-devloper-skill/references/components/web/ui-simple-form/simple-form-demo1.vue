<template>
	<ui-simple-form
		v-model="formData"
		:inputs="inputs"
		@finish="handleFinish"
		@change="handleChange"
	/>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const formData = ref({
	name: '',
	age: '',
	gender: '',
	phone: ''
})

const inputs = [
	{
		field: 'name',
		label: '姓名',
		type: 'input',
		placeholder: '请输入姓名',
		attrs: {
			maxlength: 20
		}
	},
	{
		field: 'age',
		label: '年龄',
		type: 'number',
		placeholder: '请输入年龄',
		attrs: {
			min: 0,
			max: 150
		}
	},
	{
		field: 'gender',
		label: '性别',
		type: 'radio',
		options: [
			{ label: '男', value: 'male' },
			{ label: '女', value: 'female' }
		],
		defaultValue: 'male'
	},
	{
		field: 'phone',
		label: '手机号',
		type: 'input',
		placeholder: '请输入手机号码',
		attrs: {
			maxlength: 11
		}
	}
]

const handleFinish = (values) => {
	console.log('表单提交数据:', values)
	alert('表单提交成功！')
}

const handleChange = (field, value) => {
	console.log('字段变化:', field, value)
}
</script>