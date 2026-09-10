<!-- markdownlint-disable MD024 -->
# Ui Table

数据表格组件，用于展示多条结构类似的数据，可对数据进行排序、筛选、对比或其他自定义操作。

## 示例

### 基础用法

@[demo vue](./table-demo1.vue)

### 纯表格

@[demo vue](./table-demo2.vue)

## 组件特点

### 预置常用功能

1. 简单+高级筛选，高级筛选支持保存和应用自定义筛选器
2. 分页及数据总数展示
3. 内置导入、导出、全选、反选、新增等常用操作，支持插入自定义操作

支持对数据列进行排序、调序、可见性切换等常见操作，支持动态首尾冻结指定列。

#### 数据格式化

组件预置了一些列格式化函数，可以实现：

1. 将数据进行格式化展示，比如将时间戳格式化为 `yyyy-MM-dd` 形式。
2. 将数据列展示为按钮、标签、链接、微图表等额外形式。

::: info

微图表是指维度指标简单、尺寸小巧适于嵌入小尺寸布局空间的图表，支持线图、柱图、条图、进度图、饼图等。

:::

![数据格式化](./images/table-style.png)

```typescript
import type { UiTableColumn } from '@e-cloud/eslink-plus'
const inputs: UiTableColumn[] = [
	{
		prop: 'birthday',
		label: '出生日期',
		display: {
			formatter: 'date',
			type: 'yyyy-MM-dd',
		},
	},
	{
		prop: 'progress',
		label: '考试进度',
		display: {
			formatter: 'microChart',
			type: 'progress',
		},
	},
	{
		prop: 'detail',
		label: '详情',
		display: {
			formatter: 'button',
			type: 'info',
			action: 'detail',
			text: '记录详情',
		},
	},
	{
		prop: 'character',
		label: '性格',
		display: {
			formatter: 'tag',
			type: 'info',
			action: 'character',
		},
	},
	// ...
]

export default inputs
```

### 更好的事件绑定方案

UiTable、UiForm 等组件实现了配置无关的、更好的事件绑定机制。

在以往项目开发中使用表格、表单等组件时，开发者需要以配置的方式注册事件侦听器，比如：

::: code-tabs
@tab formItem.js

```typescript
export const getFormItems = instance => {
	return [
		{
			prop: 'age',
			label: '年龄',
			events: {
				click: function () {
					// instance...
				}
			}
		},
		// ...
	]
}
```

:::

此类方式存在如下问题:

1. 属性配置文件可能会引入组件实例，导致配置文件函数化，且不再独立于组件实例
2. 配置文件远程化时需要额外处理
3. 增加代码复杂度、存在重复编码，不利于开发维护
4. …

通过实现更好的事件机制，解决上述问题。

目前支持 `export` `import` `selectAll` `selectReverse` `insert` `delete` 等操作类型。

内置及自定义操作类型，都可通过 `@${target}-${actionName}-${event}` 形式进行事件捕获。

- `target` 事件发起的目标:
  - `action`: 内置操作按钮及插入的自定义操作按钮类型
  - `cell`: 单元格操作类型
  - `input`: 表单域类型
  - …
- `actionName`: 定义的操作类型名称
- `event`: 要捕获的事件: click/dblclick/blur/change/input/focus…

参考如下示例：

::: code-tabs
@tab formItem.js

```typescript
export default [
	{
		prop: 'age',
		label: '年龄',
	},
	// ...
]
```

@tab form.vue

```vue
<template>
	<!-- @input-age-blur: 侦听表单中 prop 为 age 的表单域失焦事件 -->
	<UiForm
		:inputs="inputs"
		@input-age-blur="handleAgeBlur"
	></UiForm>
</template>

<script setup lang="ts">
import { UiForm } from '@e-cloud/eslink-plus'
import type { UiFormItem } from '@e-cloud/eslink-plus'
import { reactive } from 'vue'
import formItems from './formItems.js'

defineOptions({
	name: 'FormPage',
})

const inputs = reactive<UiFormItem[]>(formItems)

const handleAgeBlur = (value: string, input: HTMLInputElement): void => {
	console.log(value, input)
}
</script>
```

```typescript [columns.js]
import type { UiTableColumn } from '@e-cloud/eslink-plus'
const columns: UiTableColumn[] = [
	{
		label: '姓名',
		prop: 'name',
		width: 180,
		display: {
			formatter: 'button',
			type: 'primary',
			// 定义了一个名为 edit-name 的 action
			action: 'edit-name',
		}
	},
	...
]

export default columns
```

```vue [table.vue]
<template>
	<!-- @cell-edit-name-click: 侦听 column 中 action 为 edit-name 的按钮点击事件 -->
	<UiTable
		:columns="columnsConfig"
		:data="data"
		@cell-edit-name-click="handleEditName"
	></UiTable>
</template>

<script setup lang="ts">
import { UiTable } from '@e-cloud/eslink-plus'
import type { UiTableColumn, UiTableRecord } from '@e-cloud/eslink-plus'
import { reactive } from 'vue'
import columns from './columns.js'

defineOptions({
	name: 'TablePage',
})

const columnsConfig = reactive<UiTableColumn[]>(columns)

const data = ref<UiTableRecord[]>([
	{
		name: '王小明',
		age: 18,
		address: '北京市海淀区',
	},
	{
		name: '张小红',
		age: 20,
		address: '上海市浦东新区',
	},
])

const handleEditName = (row: UiTableRecord, column: UiTableColumn): void => {
	console.log('编辑姓名', row, column)
}
</script>
```

:::

#### One More Thing…

开发者可能习惯通过插槽放入操作按钮，并维护一个选中记录 `selections`, 比如：

::: code-tabs

@tab table.vue

```vue
<template>
	<UiTable
		:columns="columnsConfig"
		:data="data"
		@selection-change="handleSelectionChange"
	>
		<template #action-left>
			<ui-button @click="handleExport">导出</UiButton>
		</template>
	</UiTable>
</template>
<script setup lang="ts">
import { UiTable } from '@e-cloud/eslink-plus'
import type { UiTableColumn, UiTableRecord } from '@e-cloud/eslink-plus'
import { reactive } from 'vue'
import columns from './columns.js'

defineOptions({
	name: 'TablePage',
})

const columnsConfig = reactive<UiTableColumn[]>(columns)
const data = ref<UiTableRecord[]>([
	{
		name: '王小明',
		age: 18,
		address: '北京市海淀区',
	},
	{
		name: '张小红',
		age: 20,
		address: '上海市浦东新区',
	},
])

const selections = ref<UiTableRecord[]>([])

const handleSelectionChange = (rows: UiTableRecord[]): void => {
	selections.value = rows
}

const handleExport = (): void => {
	console.log('导出', selections)
}
</script>
```

:::

针对这种情况，开发者可以通过一下方式简化操作和代码。

::: code-tabs

@tab table.vue

```vue
<template>
	<UiTable
		:columns="columnsConfig"
		:data="data"
		@action-export-click="handleExport"
	>
		<template #action-left>
			<ui-button action:click="export" action:bind="selection">导出</UiButton>
		</template>
	</UiTable>
</template>
<script setup lang="ts">
import { UiTable } from '@e-cloud/eslink-plus'
import type { UiTableColumn, UiTableRecord } from '@e-cloud/eslink-plus'
import { reactive } from 'vue'
import columns from './columns.js'

defineOptions({
	name: 'TablePage',
})

const columnsConfig = reactive<UiTableColumn[]>(columns)
const data = ref<UiTableRecord[]>([
	{
		name: '王小明',
		age: 18,
		address: '北京市海淀区',
	},
	{
		name: '张小红',
		age: 20,
		address: '上海市浦东新区',
	},
])

const handleExport = (selections, e): void => {
	console.log('导出', selections)
}
</script>
```

:::

::: info

`action:click="export"` 表示点击按钮时，触发 `action-export-click` 事件。

`action:bind="selection"` 表示 `action-export-click` 事件回调将传入选中记录参数。

`action:bind` 所有可选值:

- `selection`: 选中记录
- `filters`: 筛选器参数
- `page`: 分页信息

:::

## 属性

| 属性名称               | 描述           | 类型            |
| --------------------- | ------------------ | -------------- |
| columns               | 表格字段配置         | `UiTableColumn[]`                      |
| [config]              | 表格配置             | `UiTableConfig`                        |
| [data]                | 表格数据             | `UiTableRecord[]`                      |
| [request]             | 数据查询配置         | `UiTableRequest`                       |
| [pagination]          | 分页配置             | `Partial<PaginationProps> & { size?: number, page?: number }`<br>el-pagination [分页设置](https://element-plus.org/zh-CN/component/pagination.html#api) |
| [filters]             | 筛选器配置           | `UiFilterWrapperFilterConfig`                  |
| [params]              | 筛选器参数           | `UiFilterWrapperParams<UiFilterWrapperFilterConfig>`   |
| [usePresetActions]    | 使用预置操作按钮      | `UiTablePresetActions`                |
| [actionButtons]       | 自定义操作按钮        | `UiTableActionButton[]`                |
| [disableLocalFilter]  | 是否禁用本地筛选      | `boolean`                             |
| [dataFilter]          | 自定义静态数据筛选函数 | `(data, params?, page?) => { data, total: number }` |
| [filterMode] | 筛选器模式 | `'simple' \| 'advanced' \| 'complex'` |
| [showColumnConfig] | 是否显示列配置 | `boolean` |
| [emptyCellText] | 空单元格文本 | `string` |
| [hideFilterBar] | 是否隐藏筛选工具条 | `boolean` |
| [hideTopBar] | 是否隐藏顶栏 | `boolean` |
| [usePureTable] | 是否启用纯表格模式 | `boolean` |

### columns

#### 私有属性

| 属性名称 | 描述 | 类型 |
|--------|--------|--------|
| [visible] | 该列是否可见 | `boolean` |
| [display] | 单元格显示配置，预置的格式化函数 | `UiTableCellDisplay` |

##### display

单元格显示配置，预置的格式化函数。基于此，开发者可以方便的将该列[数据格式化](#数据格式化)为不同的展示形式。

###### 属性

| 属性名称 | 描述 | 类型 |
|--------|--------|--------|
| formatter | 格式化器名称 | `UiTableCellFormatter` |
| [type] | 格式化器参数 | `UiTableCellFormatterTypeMap[UiTableCellFormatter]` |
| [action] | 自定义操作名称 | `string` |
| [text] | 按钮或链接文本 | `string` |
| [disabled] | 是否禁用 | `UiTableCellFormatterStateFunction` |
| [hidden] | 是否隐藏 | `UiTableCellFormatterStateFunction` |
| [attrs] | 额外属性，例如 size/style 等，直接传入对应的 element-plus 组件 | `Record<string, recordPropValueType>` |

<!-- markdownlint-disable-next-line MD036 -->
==formatter==

UiTable 预置的格式化器名称，可选值：`date` `button` `tag` `link` `progress` `microChart` `icon` `text` `image` `html`

<!-- markdownlint-disable-next-line MD036 -->
==type==

格式化器参数。根据应用的格式化器，参数类型不同，参考一下对照表。

| formatter | 参数类型 |
|-----------|-----------|
| date | `UiTableCellDateFormatterType` |
| button | `primary \| success \| warning \| danger \| info \| text` |
| tag | `success \| warning \| danger \| info` |
| link | `primary \| success \| warning \| danger \| info` |
| progress | `success \| warning \| exception` |
| microChart | `line \| bar \| pie` |
| icon | `string` |
| text | `success \| warning \| danger \| info` |
| image | `fit \| fill \| contain \| cover \| scale-down` |
| html | `never` |

<!-- markdownlint-disable-next-line MD036 -->
==disabled==

是否禁用，当格式化器设置为 `button` `link` 等类型且需要控制交互时非常有用。

设定值为函数，函数签名类型：

<!-- markdownlint-disable-next-line MD036 -->
==hidden==

是否隐藏，当需要控制格式化结果内容可见性时非常有用。设定值为函数，函数签名类型：

#### 继承属性

其他属性参考 element-plus 组件文档: [Table-column API](https://element-plus.org/zh-CN/component/table.html#table-column-api)。

### config

UiTable 功能配置。

#### 私有属性

| 属性名称 | 描述 | 类型 |
|--------|--------|--------|
| [showPagination] | 是否展示分页 | `boolean` |
| [attrs] | el-table [支持的属性](https://element-plus.org/zh-CN/component/table.html#table-api) | `TableProps` |

##### showPagination

是否展示分页。如需关闭分页请==显式的==将其设置为 `false`。

::: info

`showPagination: false` 时，pagination 配置将被忽略。

:::

### data

开发者可以监听 UiTable `filter-change` 事件获取参数，或使用外部参数，自行控制数据查询逻辑，并通过 `data` 属性向 UiTable 传入获取的数据。

<!-- Todo: 需要实现分页总数的更新 -->

::: tip

表格的数据可以通过 `data` 属性静态传入，也可以通过提供 `request` 查询方法来动态载入。

当使用 `data` 静态传入数据时，筛选工具将默认启用本地筛选，可以通过 `disableLocalFilter` 禁用该功能。

:::

### request

开发者可以定义符合 `UiTableRequestApi` 类型签名的函数，通过 `request` 属性配置到 UiTable，组件内部将自动组织筛选器、分页器等参数，并通过该函数进行数据查询。

支持 `beforeRequest` `afterRequest` 两个钩子函数，用于处理请求前参数及请求后数据处理。

```typescript
import type { UiTableRequest, UiTableProps } from '@e-cloud/eslink-plus'
import { getList } from '@/apis/customer'
import { reactive } from 'vue'

const typeMap = {
	1: '非居',
	2: '居民',
}
const request: UiTableRequest = {
	api: (params) => {
		return getList(params)
	},
	beforeRequest: (params, page) => {
		return Object.assign(params, page, { businessType: 1 })
	},
	afterRequest: (res) => {
		return res.data.map(item => {
			item.custTypeDes = typeMap[item.type]
			return item
		})
	}
}

const config = reactive<UiTableProps>({
	...
	request,
})
```

::: tip

如果需要根据条件取消请求，可在 `beforeRequest` 钩子函数中返回 `false`。

:::

### filters

[筛选器构造配置](../ui-filter-wrapper/)，支持简单+高级筛选控件配置。

| 属性名称 | 描述 | 类型 |
|--------|--------|--------|
| [simple] | 简单筛选器 | `[SimpleFilterItem, SimpleFilterItem?]` |
| [advanced] | 高级筛选器 | `UiFilterItem[]` |
| [rules] | 筛选器表单校验规则 | `FormRules` |

![筛选器](./images/filters.png)

如上图所示，红色框部分为简单筛选器。

简单筛选器右侧蓝色框内的漏斗按钮为高级筛选器切换按钮。展开的高级筛选器如上图所示。

::: tip

简单及高级筛选器配置都是一组表单元素配置，参考 [Ui Simple Form](../ui-simple-form/index.md#属性) 相关章节。

:::

#### simple

简单筛选条件，配置后将展示于表格顶栏左侧，可以包含若干常用筛选条件，用于快速查找数据。

#### advanced

简单筛选条件，配置后将展示于表格顶栏左侧，可以包含若干常用筛选条件，用于快速查找数据。

### params

初始化或动态更新筛选器默认参数。

::: tip

`params` 属性是单向的，请通过监听 `filter-change` 事件来获取筛选器最新参数状态。

:::

### usePresetActions

<!-- Todo: 权限方案待定 -->

UiTable 目前已预置多个操作按钮。

| 操作名称 | 功能描述 |
| ------ | ------ |
| `add` | 新增 |
| `edit` | 编辑 |
| `delete` | 删除 |
| `export` | 导出 |
| `import` | 导入 |
| `selectAll` | 全选 |
| `selectReverse` | 反选 |
| `refresh` | 刷新 |

::: tip

预置按钮功能需要开发者自行实现。

例如，开发者可监听 `action-add-click` 来实现新增相关功能，参考[更好的事件绑定方案](#更好的事件绑定方案)。

:::

配置示例

```typescript
import { ref } from 'vue'
import type { UiTablePresetActions } from '@e-cloud/eslink-plus'
const usePresetActions: UiTablePresetActions = ref([
	'selectAll',
	'export',
	'import',
	{
		type: 'danger',
		action: 'delete',
		label: '删除',
		icon: 'Delete'
	}
])
```

### actionButtons

自定义操作按钮配置。

| 属性名称 | 描述 | 类型 | 可选 |
| --------- | --------- | --------- | ---- |
| action | 操作名称 | `string` | × |
| label | 按钮文本 | `string` | × |
| permission | 权限标识 | `string` | √ |
| hidden | 是否隐藏 | `boolean` | √ |
| position | 按钮位置 | `right \| before-filter \| after-filter` | √ |
| attrs | 额外属性，查看[Button API](https://element-plus.org/zh-CN/component/button.html#button-api) | `Record<string, recordPropValueType>` | √ |

### disableLocalFilter

是否禁用本地数据筛选功能。当表格数据是通过 `data` 属性静态传入时。可通过该属性控制表格筛选器是否用于本地数据筛选。

如需禁用，请显式的将其设置为 `false`。

## 事件

| 事件名称               | 说明                                     | 类型                             |
| --------------------- | --------------------------------------- | ------------------------------- |
| load | 通过 `request` 函数数据载入事件 | `(data: UiTableResponse) => void` |
| row-click | 表格数据行点击事件 | `(row: T, event: Event) => void` |
| row-dbl-click | 表格数据行双击事件 | `(row: T, event: Event) => void` |
| selection-change | 表格数据选择变更事件 | `(selection: T[]) => void` |
| single-select | 表格数据单选事件 | `(selection: T, oldSelection: T) => void` |
| page-change | 表格页码变更事件 | `(page: number) => void` |
| size-change | 表格每页显示数据条数变更事件 | `(size: number) => void` |
| sort-change | 表格数据排序变更事件 | `onSortChange: (order: UiTableOrder) => void` |
| filter-change | 表格筛选器状态变更事件 | `(filters: Record<string, recordPropValueType>) => void` |
| filter-toggle-change | 高级筛选器显示/隐藏切换事件 | (boolean: boolean) |
| action-${action}-click | 内置及自定义操作按钮点击事件 | `(selection: T[], button: UiTableActionButton) => void` |
| cell-${action}-click | 单元格自定义操作点击事件 | `(row: T, column: UiTableColumn, event: Event) => void` |
| error | 表格异常事件 | `(error: Error) => void` |
| ready | 组件就绪事件 | () |
| refresh | 刷新事件 | (params, page, order) |

## 方法

通过 ref 可以获取到组件实例并调用实例方法

| 方法名 | 说明 | 参数 |
| --- | --- | --- |
| refresh | 保持查询条件、分页、排序等刷新列表 | `() => void` |
| reload | 保持查询条件、重置分页、排序等刷新列表 | `() => void` |
| validate | 验证表单 | `() => Promise<boolean>` |
| clearValidate | 清除校验 | `() => void` |
| clearData | 清空数据 | `() => void` |
| table | 获取底层 Element Plus Table 实例 | `() => ComponentPublicInstance` |

## 插槽

| 插槽名称               | 说明           |
| --------------------- | ------------- |
| filter-left | 筛选器左侧 |
| filter-right | 筛选器右侧 |
| action-left | 操作区左侧 |
| action-right | 操作区右侧 |
| under-top-bar | 表格顶栏下方 |
| under-table | 表格下方 |
| pagination-inner | 分页栏插槽<br>需要在 `config.pagination.layout` 中通过 `default` 关键字指定[位置](https://element-plus.org/zh-CN/component/pagination.html#%E6%8F%92%E6%A7%BD) |
| empty | 空数据时占位内容 |
| append | 表格数据最后一行之后 |
| `${column.prop}-header` | 自定义 prop 列列头内容 |
| `${column.prop}` | 自定义 prop 列单元格内容 |
| `${column.prop}-filter-icon` | 自定义 prop 列筛选图标 |
| `${column.prop}-filter-icon` | 自定义 prop 列筛选图标 |
| `${column.prop}-before` | 自定义 prop 列单元格前置额外内容 |
| `${column.prop}-after` | 自定义 prop 列单元格后置额外内容 |
| `${column.prop}-${index}-before` | 自定义 prop 列索引为 index 的单元格额外内容 |
| `${column.prop}-${index}-after` | 自定义 prop 列索引为 index 的单元格额外内容 |

## 类型签名

::: code-tabs

@tab UiTableProps

```typescript
/** 表格属性接口 */
export interface UiTableProps<T = UiTableRecord[]> {
	/** 表格列配置 */
	columns: UiTableColumn[]
	/** 表格静态数据 */
	data?: T
	/** 静态数据自定义过滤函数 */
	dataFilter?: <T>(
		/** 传入的静态数据 */
		data: T[],
		dataFilterParams,
	) => {
		/** 过滤后的数据 */
		data: T[]
		/** 过滤后的总记录数 */
		total: number
	}
	/** 表格配置 */
	config?: UiTableConfig
	/** 分页设置 */
	pagination?: UiTablePagination
	/** 筛选器配置 */
	filters?: UiFilterWrapperFilterConfig
	/** 筛选器初始数据 */
	params?: UiFilterWrapperParams<UiFilterWrapperFilterConfig>
	/** 远程请求函数 */
	request?: UiTableRequest<T>
	/** 通过 data 属性传入数据时，是否禁用本地数据筛选 */
	disableLocalFilter?: boolean | `${boolean}`
	/** 启用预置操作按钮 */
	usePresetActions?: UiTablePresetActions
	/** 操作按钮列表 */
	actionButtons?: UiTableActionButton[]
	/**
	 * 筛选器模式
	 * simple: 简单模式，仅显示 simple 配置的筛选器
	 * advanced: 高级筛选，仅显示 advanced 配置的筛选器，并自动展开
	 * complex: 复杂模式，显示 simple 和 advanced 配置的筛选器，且 simple 作为 advanced 子集
	 * */
	filterMode?: 'simple' | 'advanced' | 'complex'
	/** 是否显示列配置 */
	showColumnConfig?: boolean | undefined
	emptyCellText?: string
	/** 是否隐藏筛选工具条 */
	hideFilterBar?: boolean
	/** 是否隐藏顶栏 */
	hideTopBar?: boolean
	/** 是否启用纯表格，无筛选、无分页、无列配置 */
	usePureTable?: boolean
}
```

@tab UiTableColumn

```typescript [UiTableColumn]
import type { TableColumnCtx } from 'element-plus'
/** 表格列配置接口 */
export interface UiTableColumn extends Partial<TableColumnCtx<UiTableRecord>> {
	/** 是否可见 */
	visible?: boolean
	/** 单元格显示配置 */
	display?: UiTableCellDisplay
	type?: UiTableColumnType
	isSelectionStateTag?: boolean
	selectionStateRender?: (value: recordPropValueType, row: UiTableRecord, column: UiTableColumn) => string | undefined
}
```

@tab UiTableRecord

```typescript [UiTableRecord]
/** 表格数据记录类型 */
export type UiTableRecord = Record<string, recordPropValueType>
```

@tab UiTableConfig

```typescript [UiTableConfig]
import type { TableProps } from 'element-plus'
/** 表格配置接口 */
export interface UiTableConfig {
	/** 是否显示分页 */
	showPagination?: boolean
	/** 额外属性，直接传递到 ui-table */
	attrs?: Partial<TableProps<UiTableRecord>>
}
```

@tab UiFilterWrapperFilterConfig

```typescript [UiFilterWrapperFilterConfig]
import type { UiFormItem } from '../ui-form'
/** 表格筛选器配置接口 */
export interface UiFilterWrapperFilterConfig {
	/** 简单筛选项 */
	simple?: [UiSimpleFormItem, UiSimpleFormItem?]
	/** 高级筛选项 */
	advanced?: UiSimpleFormItem[]
	/** 是否显示高级筛选器 */
	showAdvanced?: boolean
}
```

@tab UiTableActionButton

```typescript [UiTableActionButton]
/** 表格操作按钮配置接口 */
export interface UiTableActionButton {
	/** 操作名称 */
	action: string
	/** 按钮文本 */
	label: string
	/** 权限标识 */
	permission?: string
	/** 是否隐藏 */
	hidden?: boolean
	/** 按钮位置 */
	position?: 'right' | 'filter-left' | 'filter-right'
	/** 额外属性, 直接传递到 ui-button */
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	attrs?: Record<string, any>
}
```

@tab UiTablePresetActionButton

```typescript [UiTablePresetActionButton]
export type UiTablePresetActionButton = Omit<UiTableActionButton, 'action'> & {
	action: presetAction
}
```

@tab UiTablePresetActions

```typescript [UiTablePresetActions]
/** 实现使用预置操作按钮类型 */
export type UiTablePresetActions = (presetAction | UiTablePresetActionButton)[]
```

@tab UiTableEvents

```typescript [UiTableEvents]
/** 表格事件接口 */
export interface UiTableEvents<T = UiTableRecord> {
	/** 错误事件 */
	onError: (error: Error) => void
	/** 组件就绪事件 */
	onReady: () => void
	/** 刷新事件 */
	onRefresh: (
		params: UiFilterWrapperParams<UiFilterWrapperFilterConfig>,
		page: UiTablePageState,
		order: UiTableOrder,
	) => void
	/** 数据加载事件 */
	onLoad: (data: UiTableResponse<T>) => void
	/** 行点击事件 */
	onRowClick: (row: T, event: Event) => void
	/** 行双击事件 */
	onRowDblclick: (row: T, event: Event) => void
	/** 选择变更事件 */
	onSelectionChange: (selection: T[]) => void
	/** 单选事件 */
	onSingleSelect: (selection: T, oldSelection: T) => void
	/** 页码变更事件 */
	onPageChange: (page: number) => void
	/** 每页数量变更事件 */
	onSizeChange: (size: number) => void
	/** 排序变更事件 */
	onSortChange: (order: UiTableOrder) => void
	/** 筛选器选项变更事件 */
	onFilterChange: (
		params: UiFilterWrapperParams<UiFilterWrapperFilterConfig>,
		page: UiTablePageState,
		order: UiTableOrder,
	) => void

	/** 高级筛选器显示/隐藏切换事件 */
	onFilterToggleChange: (boolean: boolean) => void
	/** 操作按钮点击事件 */
	[key: `onAction${string}Click`]: (selection: T[], button: UiTableActionButton) => void
	/** 单元格点击事件 */
	[key: `onCell${string}Click`]: (row: T, column: UiTableColumn, event: Event) => void
}
```

@tab ActionEventName

```typescript [ActionEventName]
/** 获取操作按钮事件名称类型 */
export type ActionEventName<T> = Extract<keyof UiTableEvents<T>, `onAction${string}Click`>
```

@tab CellEventName

```typescript [CellEventName]
/** 获取单元格点击事件名称类型 */
export type CellEventName<T> = Extract<keyof UiTableEvents<T>, `onCell${string}Click`>
```

@tab UiTableState

```typescript [UiTableState]
/** 表格状态接口 */
export interface UiTableState<T = Record<string, recordPropValueType>> {
	/** 分页状态 */
	page: UiTablePageState
	/** 加载状态 */
	loading: boolean
	/** 选中行数据 */
	selection: T[] | T
	/** 排序字段 */
	sortProp?: string
	/** 排序方向 */
	sortOrder?: 'ascending' | 'descending'
	filters: Record<string, recordPropValueType>
	orderState: UiTableOrder
}
```

@tab UiTableCellDisplay

```typescript [UiTableCellDisplay]
/** 格式化状态函数类型 */
export type UiTableCellFormatterStateFunction = (
	row: UiTableRecord,
	column: UiTableColumn,
	cellValue: recordPropValueType,
	index: number,
) => boolean

/** 格式化器类型映射 */
export type UiTableCellFormatterTypeMap = {
	date: UiTableCellDateFormatterType
	button: UiTableCellButtonFormatterType
	tag: UiTableCellTagFormatterType
	link: UiTableCellLinkFormatterType
	progress: UiTableCellProgressFormatterType
	microChart: UiTableCellMicroChartFormatterType
	icon: UiTableCellIconFormatterType
	text: UiTableCellTextFormatterType
	image: UiTableCellImageFormatterType
	amountLToU: string
	formatToThousandSeparator: string
	html: never
	custom: never
}
/** 单元格显示配置接口 */
export interface UiTableCellDisplayBase {
	/** 格式化器名称 */
	formatter: UiTableCellFormatter
	/** 格式化器参数 */
	type?: UiTableCellFormatterTypeMap[UiTableCellFormatter]
	/** 自定义操作名称 */
	action?: string
	/** 按钮或链接文本 */
	text?: string
	/** 是否禁用 */
	disabled?: UiTableCellFormatterStateFunction
	/** 是否隐藏 */
	hidden?: UiTableCellFormatterStateFunction
	/** 额外属性，例如 size/style 等 */
	attrs?: Record<string, recordPropValueType>
	/** 自定义渲染函数 */
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	render?: (value: any, row: UiTableRecord) => any
}

/** 单元格显示配置接口 */
export type UiTableCellDisplay = UiTableCellDisplayBase
```

@tab UiTableResponse

```typescript [UiTableResponse]
/** 表格响应数据接口 */
export interface UiTableResponse<T = UiTableRecord[]> {
	/** 总记录数 */
	total?: number
	/** 状态码 */
	code?: number
	/** 消息 */
	message?: string
	/** 数据列表，属性名根据 responseListKey 配置 */
	[key: string]: T | number | string | undefined
}
```

@tab UiTableRequest

```typescript [UiTableRequest]
/** 数据请求函数 */
export type UiTableRequestApi<T = UiTableRecord[]> = (
	params: UiFilterWrapperParams<UiFilterWrapperFilterConfig> & UiTablePageState & { order?: string | undefined },
) => Promise<UiTableResponse<T>>

export type UiTablePageState = {
	/** 当前页码 */
	page: number
	/** 每页数量 */
	size: number
	/** 总记录数 */
	total?: number
}

/** 数据请求前钩子 */
export type UiTableBeforeRequest = (
	params?: UiFilterWrapperParams<UiFilterWrapperFilterConfig>,
	page?: UiTablePageState,
	order?: string | undefined,
) => Promise<Record<string, recordPropValueType> | undefined | false>

/** 数据请求后钩子 */
export type UiTableAfterRequest<T = UiTableRecord[]> = (response?: UiTableResponse<T>) => Promise<UiTableResponse<T> | undefined>

/** 数据请求配置对象 */
export type UiTableRequest<T = UiTableRecord[]> = {
	api: UiTableRequestApi<T>
	beforeRequest?: UiTableBeforeRequest
	afterRequest?: UiTableAfterRequest<T>
	responseListKey?: string
}
```

:::
