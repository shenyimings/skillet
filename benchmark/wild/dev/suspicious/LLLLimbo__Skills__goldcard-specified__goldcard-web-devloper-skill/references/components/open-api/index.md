# 开放API

开放API用于解决==外部工具或应用调用前端部门平台(以下称平台)能力的问题==。例如公共CLI调用平台webhooks接口发送企业微信群消息等场景。以该场景为例，调用流程如下：

## 调用流程

![调用流程](/public/imgs/open-api/1.png)

- 登录平台，在 ==系统管理** - **应用== 中可创建应用，创建完成后会生成应用的AppKey和AppSecret；
- 应用一旦删除或者禁用，token会==立即失效==；
- token的有效期为==4小时==；
- 携带token的方式为请求头增加`authorization`字段，值为 `Bearer ${token}`
- 所有开放api均以/outer开头；

## 接口说明

接口返回统一响应结构体：

```typescript
interface Response<T> {
	code: number // 状态码，0表示调用成功
	msg: string // 调用结果说明
	data: T // 业务数据
}
```
