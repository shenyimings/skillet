# Ui Form

一个基于 ElementPlus 和 Vant、使用 [Form Making 表单设计器](http://10.200.6.246:7070/) 工具进行管理的表单组件，支持 PC 端和移动端，提供灵活的表单配置和数据管理功能。

![Form Making 表单设计器界面](./images/image.png)

## 示例

@[demo vue](./form-demo1.vue)

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| config | UiFormConfig | - | 表单配置对象 |
| data | UiFormData | {} | 表单数据对象 |

### config 配置

表单配置对象包含以下属性：

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| platform | 'pc' \| 'mobile' \| 'pad' | 'pc' | 表单运行平台 |
| edit | boolean | false | 是否为编辑模式 |
| formItems | UiFormItemConfig | - | 表单项配置对象 |

::: tip

若 `platform` 为 `mobile`，则项目中应显式的引入 [vant](https://develop365.gitlab.io/vant/zh-CN/quickstart/#/zh-CN/quickstart) 以支持移动端表单的渲染。

:::

#### formItems 配置

一般无需关系该配置，仅需将从 Form Making 表单设计器获取的配置 JSON 作为 `formItems` 属性值传入即可。

| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| list | FormItem[] | 表单项配置数组 |
| config | Config | 表单全局配置 |

## 插槽

### 公共插槽

| 插槽名 | 说明 | 作用域参数 |
| --- | --- | --- |
| title | 表单标题区域 | - |
| action | 表单操作按钮区域 | - |

### 字段插槽

每个表单字段都支持以下三种插槽：

| 插槽名 | 说明 | 作用域参数 |
| --- | --- | --- |
| field-[fieldName]-before | 字段前置内容 | `{ field, value, model }` |
| field-[fieldName] | 自定义字段渲染 | `{ field, value, model }` |
| field-[fieldName]-after | 字段后置内容 | `{ field, value, model }` |

参数说明：

- field: 当前字段配置对象
- value: 当前字段的值
- model: 整个表单的数据对象

示例：

```vue
<template>
  <ui-form :config="formConfig">
    <!-- 字段前置内容 -->
    <template #field-name-before="{ value }">
      <span>姓名：{{ value }}</span>
    </template>

    <!-- 自定义字段渲染 -->
    <template #field-custom="{ field, value, model }">
      <div>自定义渲染: {{ value }}</div>
    </template>

    <!-- 字段后置内容 -->
    <template #field-age-after>
      <span>岁</span>
    </template>
  </ui-form>
</template>
```

### 布局插槽

对于布局类型的字段（如表格、子表单、分组等），支持以下插槽：

| 插槽名 | 说明 | 作用域参数 |
| --- | --- | --- |
| layout-[fieldName]-before | 布局前置内容 | `{ field, value, model }` |
| layout-[fieldName]-after | 布局后置内容 | `{ field, value, model }` |

### 自定义空白区域插槽

当使用 blank 类型的表单项时，可以通过插槽自定义内容：

```vue
<template>
  <ui-form :config="formConfig">
    <!-- blank 类型字段的插槽 -->
    <template #customBlank="{ model }">
      <div>自定义内容，表单数据：{{ model }}</div>
    </template>
  </ui-form>
</template>

<script setup>
const formConfig = {
  formItems: {
    list: [
      {
        type: 'blank',
        model: 'customBlank',
        options: {
          width: '100%'
        }
      }
    ]
  }
}
</script>
```

## 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update | 表单数据更新时触发 | (data: UiFormData, field: string, value: any) |

## 方法

| 方法名 | 说明 | 参数 | 返回值 |
| --- | --- | --- | --- |
| reset | 重置表单 | - | void |
| refresh | 刷新表单 | - | void |
| setData | 设置表单数据 | (data: UiFormData) | void |
| getData | 获取表单数据 | (useValidation?: boolean) | Promise\<UiFormData\> |
| hideFields | 隐藏指定字段 | (fields: string[]) | void |
| showFields | 显示指定字段 | (fields: string[]) | void |
| disableFields | 禁用指定字段 | (fields: string[]) | void |
| enableFields | 启用指定字段 | (fields: string[]) | void |
| validate | 验证表单 | (fields?: string) | Promise\<boolean\> |
| getValue | 获取指定字段值 | (field: string) | any |
| getValues | 获取所有字段值 | - | UiFormData |
| setFieldRules | 设置字段验证规则 | (field: string, rules: []) | void |
| setOptions | 设置字段选项数据 | (fields: string[], options: []) | void |
| getOptions | 获取字段选项数据 | (field: string) | [] |
| switchLanguage | 切换表单语言 | (lang: string) | void |

## 国际化

组件内置中英文语言包，默认使用中文。可通过 `switchLanguage` 方法切换语言：

```ts
const formRef = ref()
// 切换到英文
formRef.value.switchLanguage('en')
// 切换到中文
formRef.value.switchLanguage('zh-CN')
```

## 开发模式

在开发环境下，组件右上角会显示一个"表单配置"按钮，点击可跳转至表单设计器页面进行配置。
