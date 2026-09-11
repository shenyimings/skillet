# microAppInit

## 说明

用于初始化子应用。每个子应用在初始化时(即main.ts文件中)，都要先调用该方法。该方法中封装了业务无关的和门户的postmessage消息。
具体的实现参考[microAppInit](http://10.200.1.145/framework/web/es-lab/es-eslink-plus/blob/main/packages/framework/micro-app.ts#L20)。


## 引入

```javascript
import { microAppInit } from '@e-cloud/eslink-plus'
```

## 使用

在main.ts文件中:

```javascript
microAppInit(app, { menus }).then(data => {
        const { lang, profile } = data
}).finally(() => {
        app.mount('#app')
}),

```
具体的使用可参考[main.ts](http://10.200.1.145/web/cis/aicis/aicis-pc/blob/dev/src/main.ts#L27)

## 参数说明

|参数名称|参数说明|默认值    |类型 |是否必传|
|------|---------|---------|-----|-------|
| app  | vue实例 |  -      | App | 是    |
| options | 其他参数| -   | Options | 否 |


**Options**

|参数名称|参数说明|默认值    |类型 |是否必传|
|------|---------|---------|-----|-------|
| appId | 应用id，用于调试权限，后端生成 | - | string | 否 |
| menus | 应用的菜单，给门户上报菜单 | -   | Menu[]  | 开发阶段必须，生产环境不传 |


## 参数类型

```ts
interface Menu {
        componentId: number | string // 菜单id
        uri: string // 菜单对应子应用页面的完整url，
        name: string // 菜单名称
}

```
