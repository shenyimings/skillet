# Ui Simple Form

一个易用的表单组件，支持分步表单、表单分段、多种输入控件类型，支持字段关联、计算字段属性。

## 示例

### 基础用法

@[demo vue](./simple-form-demo1.vue)

### 组件关联

@[demo vue](./simple-form-demo3.vue)

### 计算属性

@[demo vue](./simple-form-demo4.vue)

### 分步表单

@[demo vue](./simple-form-demo2.vue)

## 组件特点

### 预置常用功能

1. ~~内置表单提交、重置动作~~
2. 支持表单分步、分区
3. 预置常用表单校验规则，支持自定义
4. 表单域支持 `computeFrom` `link` 关联特性
5. 表单域支持：按钮、前后插槽

::: code-tabs

@tab 分步

```typescript
export default [
  {
    type: 'step',
    label: '基础信息',
    step: 'info',
  },
  ...
  {
    type: 'step',
    label: '地址信息',
    step: 'address',
  },
  ...
  {
    type: 'step',
    label: '表具信息',
    step: 'meter',
  },
  ...
]
```

@tab 分区

```typescript
export default [
  {
    type: 'split',
    label: '基础信息',
    foldable: false,
  },
  ...
  {
    type: 'split',
    label: '地址信息',
  },
  ...
  {
    type: 'split',
    label: '表具信息',
  },
  ...
]
```

:::

#### 表单域关联

::: code-tabs

@tab computeFrom

```typescript
import type { UiFormItem } from '@e-cloud/eslink-plus'
const formFields: UiFormItem[] = [
  {
    label: '客户大类',
    field: 'custType',
    type: 'select',
    options: [],
  },
  {
    label: '客户细类',
    field: 'custType2',
    type: 'select',
    options: [],
  },
  {
    label: '备注',
    field: 'remark',
    innerType: 'textarea',
    computeFrom: {
      fields: ['custType', 'custType2'],
      trigger: 'change',
      computer: (custType, custType2) => {
        return `客户类型：${custType.option.label}/${custType2.option.label}`
      }
    },
  },
]

export default formFields
```

@tab link

```typescript
import type { UiFormItem } from '@e-cloud/eslink-plus'
const formFields: UiFormItem[] = [
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
    type: 'timepicker',
  },
]

export default formFields
```

:::

## 属性

| 属性名 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| data | `object` | `{}` | 表单数据对象 |
| inputs | `UiSimpleFormItem[]` | `[]` | 表单项配置数组 |
| direction | `horizontal \| vertical` | `horizontal` | 表单布局方向 |
| gap | `number \| string` | `16` | 表单项间距 |
| labelWidth | `number \| string` | `100` | 标签宽度 |
| labelPosition | `left \| top \| right` | `top` | 标签位置 |
| hideLabel | `boolean \| string` | `false` | 是否隐藏标签 |
| inline | `boolean \| string` | `false` | 行内模式 |
| cols | `number \| string` | `2` | 每行显示的列数 |
| rules | `FormRules` | `{}` | 表单验证规则 |
| completeCallback | `function` | - | 完成回调函数 |
| returnCallback | `function` | - | 返回回调函数 |

## 表单项类型

支持以下表单项类型：

| 类型 | 说明 |
| --- | --- |
| `input` | 输入框 |
| `textarea` | 文本域 |
| `select` | 下拉选择框 |
| `number` | 数字输入框 |
| `comboInput` | 组合输入框 |
| `checkbox` | 多选框组 |
| `radio` | 单选框组 |
| `switch` | 开关 |
| `upload` | 上传组件 |
| `cascader` | 级联选择器 |
| `date/dates/datetime/time/week` | 日期时间选择器 |
| `daterange/datetimerange/monthrange/yearrange` | 日期范围选择器 |
| `year/years/month/months` | 年月选择器 |
| `step` | 步骤分隔符 |
| `split` | 分段分隔符 |
| `rangeInput` | 范围输入框 |

## 表单项配置

```typescript
interface UiSimpleFormItem {
  field: string          // 字段名
  label: string          // 标签文本
  type: string           // 表单项类型
  placeholder?: string   // 占位提示
  options?: UiSimpleFormItemOption[]  // 选项配置
  defaultValue?: UiSimpleFormItemValue  // 默认值
  link?: UiSimpleFormLink | UiSimpleFormLink[]  // 字段关联配置
  computeFrom?: UiSimpleFormComputeFrom  // 计算字段配置
  cols?: number \| string  // 列数
  formItemAttrs?: any    // 表单项属性
  attrs?: any            // 表单控件属性
  events?: any           // 表单控件事件
}
```

## 事件

| 事件名 | 说明 | 回调参数 |
| --- | --- | --- |
| update:data | 表单数据更新事件 | `(value: Record<string, UiSimpleFormItemValue>) => void` |
| complete | 表单完成事件（分步表单最后一步点击完成时触发） | `(value: Record<string, UiSimpleFormItemValue>) => void` |
| return | 返回事件（分步表单点击返回时触发） | `(value: Record<string, UiSimpleFormItemValue>) => void` |
| change | 表单项值改变事件 | `(value: Record<string, UiSimpleFormItemValue>) => void` |
| reset | 表单重置事件 | `(value: Record<string, UiSimpleFormItemValue>) => void` |
| edited | 表单编辑事件 | `() => void` |

## 插槽

每个表单项都支持以下插槽：

| 插槽名 | 说明 |
| --- | --- |
| `${field}-before` | 表单项前插槽 |
| `${field}` | 表单项内容插槽 |
| `${field}-after` | 表单项后插槽 |
| `${field}-prefix` | 输入框前缀插槽 |
| `${field}-suffix` | 输入框后缀插槽 |
| `${field}-prepend` | 输入框前置内容插槽 |
| `${field}-append` | 输入框后置内容插槽 |
| `${field}-split` | 分段元素插槽 |

## 方法

| 方法名 | 说明 |
| --- | --- |
| resetFields | 重置表单 |
| validate | 表单验证 |
| clearValidate | 清除验证 |
| getData | 获取表单数据 |
| initFieldStates | 初始化字段状态 |
| updateLinkState | 更新关联状态 |
| toggleFieldsVisibility | 切换字段可见性 |
| toggleFieldsDisable | 切换字段禁用状态 |

## 高级功能

### 字段关联 (Link)

支持字段之间的动态关联，包括：

- 根据字段值动态显示/隐藏其他字段
- 根据字段值动态启用/禁用其他字段
- 根据字段值动态过滤选项
- 远程获取选项数据

```typescript
interface UiSimpleFormLink {
  field: string | string[]  // 关联字段
  trigger: 'input' | 'change' | 'blur' | 'focus'  // 触发时机
  filter?: (option: UiSimpleFormItemOption, value: UiSimpleFormItemValue, field: UiSimpleFormItem) => boolean
  visible?: (value: UiSimpleFormItemValue, field: UiSimpleFormItem) => boolean
  disable?: (value: UiSimpleFormItemValue, field: UiSimpleFormItem) => boolean
  fetch?: UiSimpleFormItemRemoteOptionsFetch  // 远程选项获取
}
```

::: warning

- `filter` `disable` `visible` `fetch` 互斥，即在一个关联配置中仅可选其一。
- `filter` `disable` `visible` 所配置的函数应总是返回一个布尔值。

:::

::: tip 同时配置多个关联操作

`link` 属性可传入一个数组，来为当前字段配置多个关联操作。

:::

### 计算字段 (ComputeFrom)

支持基于其他字段值动态计算字段值：

```typescript
interface UiSimpleFormComputeFrom {
  fields: string[]  // 依赖字段
  trigger: 'input' | 'change' | 'blur' | 'focus'  // 触发时机
  computer: (...args: UiSimpleFormItemValue[]) => UiSimpleFormItemValue  // 计算函数
}
```

::: tip 计算函数的参数

计算函数的参数及顺序与绑定的依赖字段列表一致。

:::
