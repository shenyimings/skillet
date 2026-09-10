## postMessageGetInitConfig

## 说明

> 子系统初始化加载前向门户获取 功能权限码/css主题变量/国际化配置/用户信息

## 引用

```javascript
import { postMessageGetInitConfig } from '@e-cloud/eslink-plus'
```

## 使用

```javascript
// main.ts

const app = createApp(App)

const initApp = async () => {
	const data = await postMessageGetInitConfig()
	console.log(data)
	app.mount('#app')
}

initApp()
```

## 参数说明

|参数名称|参数说明|默认值|类型|是否必传|
|------|---------|---------|-----|-------|
|timeout|配置信息获取超时时间|5000|number|false|
|menus  |子系统上报菜单数据  | -  |[ApplicationMenu\[\]](/scheme/identityCenter#applicationmenu)|false|

## menus 格式

```javascript
[
	{
		appId: '1',
		componentId: '1',
		name: '组织管理',
		uri: 'http://localhost:2000/system/organize',
	},
	{
		appId: '1',
		componentId: '2',
		name: '员工管理',
		uri: 'http://localhost:2000/system/member',
	},
	{
		appId: '1',
		componentId: '3',
		name: '角色管理',
		uri: 'http://localhost:2000/system/role',
	}
]
```
