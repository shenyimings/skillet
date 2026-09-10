# Ui Aside Filter

## 侧边筛选器

页面侧边栏的筛选器组件，支持表单项配置、折叠展开等功能。

## 示例

![侧边栏筛选器](./images/image.png)

```vue
<template>
  <UiAsideFilter
    :filters="inputs"
    :params="params"
    title="高级筛选"
    @confirm="handleConfirm"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { UiSimpleFormItemValue } from '@e-cloud/eslink-plus'

const inputs = [
  {
    field: 'name',
    label: '姓名',
    type: 'input',
    placeholder: '请输入姓名',
    attrs: {
      clearable: true
    }
  },
  {
    field: 'openDate',
    label: '开户日期',
    type: 'daterange',
    startPlaceholder: '请选择起始日期',
    endPlaceholder: '请选择结束日期',
    attrs: {
      valueFormat: 'YYYY-MM-DD'
    }
  }
]

const params = ref({
  name: '张三',
  openDate: ['2022-01-01', '2022-01-31']
})

const handleConfirm = (values: Record<string, UiSimpleFormItemValue>) => {
  console.log('确认:', values)
}
</script>
```

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| filters | FilterItem[] | [] | 表单项配置数组 |
| params | Record<string, UiSimpleFormItemValue> | {} | 表单的初始值 |
| foldable | boolean \| string | true | 是否可折叠 |
| title | string | '筛选器' | 筛选器标题 |
| showReset | boolean | true | 是否显示重置按钮 |
| showConfirm | boolean | true | 是否显示过滤按钮 |
| confirmText | string | '确定' | 确认按钮文本 |
| resetText | string | '重置' | 重置按钮文本 |
| showSave | boolean | true | 是否展示保存并过滤按钮 |
| saveAndConfirmText | string | '保存并过滤' | 保存并过滤按钮文本 |

## 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| change | 表单值变化时触发 | (values: Record<string, UiSimpleFormItemValue>) |
| confirm | 点击过滤按钮时触发 | (values: Record<string, UiSimpleFormItemValue>) |
| save | 点击保存并过滤按钮时触发 | (values: Record<string, UiSimpleFormItemValue>) |
| reset | 点击重置按钮时触发 | - |

## 方法

| 方法名 | 说明 |
| --- | --- |
| handleReset | 重置表单 |

## 插槽

| 插槽名 | 说明 |
| --- | --- |
| actions | 底部操作按钮区域 |
