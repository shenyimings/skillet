## navigatorLink

## 说明

> 子系统页面跳转

## 引用

```javascript
import { navigatorLink } from '@e-cloud/eslink-plus'
```

## 使用

```javascript
navigatorLink({
	name: 'xxx详情',
	url: 'https://xxxx..xx',
	openType: 'inner',
})
```

## 参数说明

|参数名称|参数说明|默认值|类型|是否必传|
|------|---------|---------|-----|----|
|name|页面跳转后的名称|-|string|true|
|url|页面跳转目标地址|-|string|true|
|openType|跳转类型|-|'inner' \| 'new-tab' \| 'blank'|true|


