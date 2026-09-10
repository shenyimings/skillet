# 预设样式

属于原子样式的范畴，可自定义或引用成熟方案。

## 内外边距

### 字母指代

字母 | 样式属性 | 说明
---|---|---
m | margin | 外边距，样式简写
p | padding | 内边距，样式简写
h | - | 水平 left + right，方向简写
v | - | 垂直 top + bottom，方向简写
l | left | 左侧，方向简写
r | right | 右侧，方向简写
t | top | 顶部，方向简写
b | bottom | 底部，方向简写
a | auto | 自动边距

可取边距值列表 `0` `5` `10` `15` `20` `25` `30` `40` `50`，单位为 `px`

### 样式名规则

`样式简写 + [方向简写] + 边距值 | -a`

### 示例

```html
<!-- 无外边距  -->
<div class="m0"></div>

<!-- 顶部外边距 5px  -->
<div class="mt5"></div>

<!-- 左侧内边距 10px -->
<div class="pl10"></div>

<!-- 水平内边距 10px -->
<div class="ph10"></div>

<!-- 水平内边距 10px，垂直外边距自动 -->
<div class="ph10 mv-a"></div>

<!-- 除了右侧内边距 10px，其他方向无内边距 -->
<div class="p0 pr10"></div>

<!-- 顶部内边距 5px，同时底部外边距 5px -->
<div class="pt5 mb5"></div>
```

## 宽高

样式名列表

样式名 | 说明
---|---
h100 | 高度为父元素的 100%
w100 | 宽度为父元素的 100%
hw100 | 宽度和高度均为父元素的 100%

示例

```html
<!-- 高度为父元素的 100% -->
<div class="h100"></div>
```

## 定位类型

样式名列表

样式名 | 说明
---|---
relative | 相对定位
absolute | 绝对定位
fixed | 固定定位

示例

```html
<!-- 元素绝对定位 -->
<div class="absolute"></div>
```

## 文本对齐

样式名列表

样式名 | 说明
---|---
text-left | 左对齐
text-center | 居中对齐
text-right | 右对齐

示例

```html
<!-- 元素内容居中对齐 -->
<div class="text-center"></div>
```

::: warning
该样式会被其后代元素继承
:::

## 忽略鼠标事件

样式名列表

样式名 | 说明
---|---
no-pointer | 添加该样式，将使元素不在响应鼠标事件

示例

```html
<!-- 元素将不能被点击、拖拽。 -->
<div class="no-pointer"></div>
```

::: warning
其后代元素也将不能响应鼠标事件
:::

## 浮动

样式名列表

样式名 | 说明
---|---
pull-left | 左浮动
pull-right | 右浮动
clear-both | 清除两侧浮动，即不允许两侧出现浮动元素
clear-left | 清除左侧浮动，即不允许左侧出现浮动元素
clear-right | 清除右侧浮动，即不允许右侧出现浮动元素

示例

```html
<!-- 元素右浮动 -->
<div class="pull-right"></div>
```

## flex 布局系统

::: code-tabs
@tab helper.scss
```css
.flex {
  display: flex;

  // 主轴方向 (嵌套在 .flex 下)
  &.row {
    flex-direction: row;

    &-reverse {
      flex-direction: row-reverse;
    }
  }

  &.col {
    flex-direction: column;

    &-reverse {
      flex-direction: column-reverse;
    }
  }

  // 主轴对齐 (嵌套在 .flex 下)
  &.justify {
    &-start {
      justify-content: flex-start;
    }

    &-end {
      justify-content: flex-end;
    }

    &-center {
      justify-content: center;
    }

    &-between {
      justify-content: space-between;
    }

    &-around {
      justify-content: space-around;
    }

    &-evenly {
      justify-content: space-evenly;
    }
  }

  // 交叉轴对齐 (嵌套在 .flex 下)
  &.items {
    &-start {
      align-items: flex-start;
    }

    &-end {
      align-items: flex-end;
    }

    &-center {
      align-items: center;
    }

    &-baseline {
      align-items: baseline;
    }

    &-stretch {
      align-items: stretch;
    }
  }

  // 多行对齐 (嵌套在 .flex 下)
  &.content {
    &-start {
      align-content: flex-start;
    }

    &-end {
      align-content: flex-end;
    }

    &-center {
      align-content: center;
    }

    &-between {
      align-content: space-between;
    }

    &-around {
      align-content: space-around;
    }

    &-stretch {
      align-content: stretch;
    }
  }

  // 换行 (嵌套在 .flex 下)
  &.wrap {
    flex-wrap: wrap;

    &-none {
      flex-wrap: nowrap;
    }

    &-reverse {
      flex-wrap: wrap-reverse;
    }
  }

  // 子项扩展 (嵌套在 .flex 下)
  > .grow {
    flex-grow: 1;

    &-0 {
      flex-grow: 0;
    }
  }

  > .shrink {
    flex-shrink: 1;

    &-0 {
      flex-shrink: 0;
    }
  }

  > .flex {
    &-1 {
      flex: 1 1 0%;
    }

    &-auto {
      flex: 1 1 auto;
    }

    &-initial {
      flex: 0 1 auto;
    }

    &-none {
      flex: none;
    }
  }

  // 子项对齐 (嵌套在 .flex 下)
  > .self {
    &-auto {
      align-self: auto;
    }

    &-start {
      align-self: flex-start;
    }

    &-end {
      align-self: flex-end;
    }

    &-center {
      align-self: center;
    }

    &-stretch {
      align-self: stretch;
    }

    &-baseline {
      align-self: baseline;
    }
  }

  // 子项顺序 (嵌套在 .flex 下)
  > .order {
    &-first {
      order: -9999;
    }

    &-last {
      order: 9999;
    }

    &-none {
      order: 0;
    }
  }
}

// 间隙样式 (独立类)
$gap-sizes: (
  0: 0,
  1: 0.25rem,
  2: 0.5rem,
  3: 0.75rem,
  4: 1rem,
  5: 1.25rem,
  6: 1.5rem,
  8: 2rem,
  10: 2.5rem,
  12: 3rem,
  16: 4rem,
  20: 5rem,
  24: 6rem,
  32: 8rem,
  40: 10rem,
  48: 12rem,
  56: 14rem,
  64: 16rem
);

@each $size, $value in $gap-sizes {
  .gap-#{$size} {
    gap: $value;
  }

  .row-gap-#{$size} {
    row-gap: $value;
  }

  .col-gap-#{$size} {
    column-gap: $value;
  }
}

// 内联 Flex 容器
.inline-flex {
  display: inline-flex;

  // 继承 .flex 的所有嵌套样式
  @extend .flex;
}
```

```html[index.html]
<div class="flex row justify-between items-center">
  <div class="flex-1">左侧内容</div>
  <div class="flex-none self-end">固定宽度内容</div>
  <div class="flex-1 text-right">右侧内容</div>
</div>
```

:::

待编辑…
