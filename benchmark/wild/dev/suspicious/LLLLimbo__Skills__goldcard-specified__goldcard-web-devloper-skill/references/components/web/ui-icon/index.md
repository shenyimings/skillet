# Ui Icon

简单的图标组件，支持展示自定义字体图标。

## 示例

@[demo vue](./icon-demo1.vue)

```vue
<template>
  <ui-icon name="iconfont-plus icon-plus-pushpin-line" color="#409EFF" :size="20" />
</template>

<script setup lang="ts">
import { UiIcon } from '@e-cloud/eslink-plus'
</script>
```

## 属性

| 属性名 | 类型 | 说明 |
| --- | --- | --- |
| name | `string` | 字体类名+图标类名, 参考[前端部自建图标字体平台](https://front-web.jinka.cn/base/font) 或三方字体图标平台 |
| color | `string` | 图标颜色 |
| size | `number` \| `string` | 图标大小（像素） |

## 样式类

- `.ui-icon-component` - 图标组件根元素
