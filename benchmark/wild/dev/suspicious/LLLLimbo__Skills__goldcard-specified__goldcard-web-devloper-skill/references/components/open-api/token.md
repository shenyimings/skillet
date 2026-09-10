# 获取调用凭证token

token是调用开放API的凭证，有效期为4小时。通过appKey和appSecret可获取token。

```bash
https://front-web.jinka.cn/outer/auth
```

## 请求说明

==请求Method==：`POST`

==请求Body:==
| 参数名称 | 类型 | 是否必须 | 默认值 | 说明 |
| :-: | :-: |:---: | :-: | :-: |
|appKey|string|是|-|平台颁发的AppKey|
|appSecret|string|是|-|平台颁发的AppSecret|

例如：

```json
{
	"appKey": "481bfa73==****==e24815",
	"appSecret": "2d256d5dd==****==2650b5b0cbe"
}
```

## 响应说明

调用成功时返回token。

例如：

```json
{
	"code": 0,
	"msg": "请求成功",
	"data": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBLZXkiOiI2ZjdlMmMwZWZlOGE0NTQxOWU3YTkxZjQzNTkwMGY3ZSIsImlhdCI6MTc0NTg4OTM2MSwiZXhwIjoxNzQ1OTAzNzYxfQ.cWmEvn0Pk-cOnEsMTMFeLIABSTnFq2GysC9TkxrF32U"
}
```
