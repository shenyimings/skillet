# 发送企业微信群消息

利用企业微信的[群机器人](https://developer.work.weixin.qq.com/document/path/91770)实现消息发送功能。当调用该接口时，会在群==机器人-小程序==中受到消息。

```bash
https://front-web.jinka.cn/outer/webhooks
```

## 请求说明

==请求Method==：`POST`

==请求Header==

```json
{
	"authorization": `Bearer ${token}`
}
```

==请求Body:==
| 参数名称 | 类型 | 是否必须 | 默认值 | 说明 |
| :-----: | :--: | :------:| :----: | :----: |
|operation|`AppOperationEnum `| 是 |-|操作类型|
|appName|string| 是 |-|app的中文名称|
|version|string| 是 |-|app的版本号|
|type|`AppTypeEnum`| 是 |-|app类型|
|status|`AppOperateResultEnum`| 是 |-|操作状态|
|otherInfo| `OtherInfoType`| 否 | -|其他需要在消息中发送的字段|

AppOperationEnum类型：

```typescript
enum AppOperationEnum {
	create = '新增',
	edit = '信息修改',
	delete = '删除',
	versionUpdate = '版本更新',
	versionSwitch = '版本切换',
}
```

AppTypeEnum类型：

```typescript
enum AppTypeEnum {
	AppFTP = 'AppFTP',
	MiniProgram = 'MiniProgram',
	AppPGY = 'App蒲公英',
	AppAppStore = 'AppAppStore',
	AppHuawei = 'App华为应用市场',
	AppMi = 'App小米应用市场',
	AppGoogle = 'AppGooglePlay',
	AppOppo = 'AppOPPO应用商店',
	AppVivo = 'AppVIVO应用商店',
	AppYYB = 'App应用宝',
}
```

AppOperateResultEnum类型：

```typescript
enum AppOperateResultEnum {
	success = '成功',
	pending = '发布中',
	failed = '失败',
}
```

OtherInfoType类型：

```typescript
  type OtherInfoType {
    [key: string]: string | number
  }
```

例如：

```json
{
	"operation": "新增",
	"appName": "泰能外勤",
	"version": "1.0.0",
	"type": "AppGooglePlay",
	"status": "成功",
	"operatorRealName": "第三方应用:公共CLI",
	"otherInfo": {
		"错误原因": "打包错误"
	}
}
```

## 响应说明

调用成功后可在==机器人-小程序==群中收到消息：

![消息](/public/imgs/open-api/2.png)
