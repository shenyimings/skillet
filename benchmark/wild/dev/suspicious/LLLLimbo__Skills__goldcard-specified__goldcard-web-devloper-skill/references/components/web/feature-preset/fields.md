# 预设字段

字段预设是一个概念，表示通过某种方法，简化列表、表单字段配置和维护成本。

系统中大部分表单、列表字段在其展示、采集等方面存在一致性，因此可以通过集中配置常用字段的相关属性，在表格、表单和筛选组件中快捷使用，以便减少代码重复，保持代码整洁。

::: code-tabs
@tab user-preset.js
```javascript
const presetFields = Object.freeze({
  custName: {
    label: '客户名称',
    field: 'custName',
    column: {},
    input: {
      value: '',
      placeholder: '客户名称'
    },
    filter: {}
  }
})

const usePresetColumns = fields => {
  return fields.map(field => {
    const { label, field, column } = presetFields[field]
    return {
      label, field, ...column
    }
  })
}

const usePresetInputs = fields => {
  return fields.map(field => {
    const { label, field, input } = presetFields[field]
    return {
      label, field, ...input
    }
  })
}

const usePresetFilters = fields => {
  return fields.map(field => {
    const { label, field, input, filter } = presetFields[field]
    return {
      label, field, ...input, ...filter
    }
  })
}

export { usePresetColumns, usePresetInputs, usePresetFilters }
```

```javascript[不使用预设]
export default [
  {
    label: '客户名称',
    field: 'custName'
    // ...其他属性项
  }
]
```

```javascript[使用预设]
import { usePresetColumns } from '@e-cloud/eslink-plus'
export default [
  ...usePresetColumns([
    'custName',
    'userNo',
  ])
]
```

:::

## 预设方法

```javascript
/**
 * 一个典型的字段预设配置
 * 必要属性:
 * label: 字段描述
 * field: 字段名称
 * 可选属性:
 * column: 表示该字段可用于 ui-table 的 columns 配置
 * input: 表示该字段可用于 ui-form 的 inputs 配置
 * filter: 表示该字段可用于 ui-filter 的 params 配置
 * 其中 filter 将继承 input 的预设配置
 * 可选属性中可省略 label、field 配置，以继承父级的 label、field 字段
 */
{
  meterType: {
    label: '表具类型',
    field: 'meterType',
    // 空配置表示继承父级 label、field
    column: {},
    input: {
      type: 'select',
      value: '',
      options: [
        {
          label: '普表',
          value: 11
        },
        {
          label: '卡表',
          value: 12
        },
        {
          label: '远传表',
          value: 13
        }
      ]
    },
    // filter 预设字段，继承 input 预设配置
    filter: {
      multiple: true,
      value: []
    }
  }
}
```

待编辑…
