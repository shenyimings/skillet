### 3.1 获取用户信息

**功能描述**

获取当前登录用户信息。

**方法名称**`accessInfo`
::: code-tabs
@tab javascript
```javascript
esBridge.callNative("accessInfo");
```
:::

**返回数据结构（成功）**
::: code-tabs
@tab json
```json
{
  "success": true,
  "message": "成功",
  "code": "0",
  "data": {
    "accountNo": "",
    "channelType": "2",
    "accountType": "2",
    "userId": "15"
  }
}
```
:::

**返回字段说明**

| 字段名      | 类型     | 说明           |
| ----------- | -------- | -------------- |
| accountNo   | `String` | 账号           |
| channelType | `String` | 渠道类型 默认2 |
| accountType | `String` | 账号类型 默认2 |
| userId      | `String` | 用户ID         |

**返回数据结构（失败）**
::: code-tabs
@tab json
```json
{
  "success": false,
  "message": "缺少回调参数",
  "code": "030101",
  "data": {}
}
```
:::

**错误码说明**

| 错误码 | 说明             | 处理建议              |
| ------ | ---------------- | --------------------- |
| 030101 | 缺少回调参数     | 联系SDK开发者         |
| 030102 | 获取用户信息失败 | 开发处理,建议重新登陆 |

**注意事项**

1. 第一次进入应在调用接口前获取鉴权信息

**调用示例**
::: code-tabs
@tab javascript
```javascript
esBridge.callNative("accessInfo", (result) => {
  if (result.success) {
    console.log("账号", result.data.accountNo);
    console.log("用户ID:", result.data.userId);
  } else {
    console.error("获取鉴权信息失败", result.message);
  }
});
```
:::