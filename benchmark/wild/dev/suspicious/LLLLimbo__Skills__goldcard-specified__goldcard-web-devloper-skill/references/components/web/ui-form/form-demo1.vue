<template>
	<UiForm
		ref="form"
		:config="formConfig"
		:data="formData"
		@update="handleFormChange"
	>
		<template #addressInfo>
			<UiCellList :data="cellData" item-direction="vertical"></UiCellList>
		</template>
		<template #protocolDetail>
			<UiCellList
				item-direction="vertical"
				empty-text="请选择价格名称"
			></UiCellList>
		</template>
		<template #action>
			<ui-button type="primary" @click="handleFormReset">重置</ui-button>
			<ui-button type="success" @click="handleSubmit">提交</ui-button>
		</template>
		<template #title>
			<h2>开户</h2>
		</template>
	</UiForm>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type {
	UiFormConfig,
	UiFormData,
	UiCellItem,
} from '@e-cloud/eslink-plus';
import formConfigSource from './form-config';

const formConfig = ref<UiFormConfig>({
	platform: 'pad',
	edit: true,
	formItems: formConfigSource,
});

const formData = ref<UiFormData>({
	custName: '王小明',
	custAddress: '北京市海淀区西沙胡同05号',
	custNo: '4219752344',
	custPhone: '15932234323',
	custType: '居民',
	sendTime: '20:00:00',
	industry: ['餐饮'],
	smsTemplate: '<h1>测试短信模板</h1><br><p>测试短信模板内容</p>',
	rate: 4,
	range: 50,
});

const form = ref();

const handleFormChange = (data: UiFormData, field: string, value: any) => {
	console.log('表单更新:', { data, field, value });
};

const handleSubmit = async () => {
	console.log('表单提交:', formData.value);
};

const handleFormReset = () => {
	formData.value = { name: '', age: '', gender: '' };
};

const cellData: UiCellItem[] = [
	{
		label: '用户号',
		value: '1100002',
	},
	{
		label: '地址描述',
		value: '河北省石家庄市长安区荣盛华府04栋01单元3001室',
	},
	{
		label: '管理组织',
		value: '长安区服务站',
	},
	{
		label: '片区',
		value: '中山办事处',
	},
];
</script>
