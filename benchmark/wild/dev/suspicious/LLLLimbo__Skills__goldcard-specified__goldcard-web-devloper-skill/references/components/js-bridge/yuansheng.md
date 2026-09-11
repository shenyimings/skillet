## 快速使用

### 安装 SDK
::: code-tabs
@tab javascript
```javascript
npm i @e-cloud/outwork-bridge --save
```
:::

### 请求方法示例
::: code-tabs
@tab javascript
```javascript
// 调用JSBridge方法
esBridge.callNative(method, params, callback);
esBridge.callNative(method, params);
esBridge.callNative(method, callback);
esBridge.callNative(method);
```
:::

### 请求参数说明

| 参数名   | 类型       | 必填 | 说明                             |
| -------- | ---------- | ---- | -------------------------------- |
| method   | `String`   | 是   | 方法名称，以下会列出             |
| params   | `Object`   | 否   | 参数对象，每个方法 params 不一样 |
| callback | `Function` | 否   | 回调函数                         |

### 返回参数示例
::: code-tabs
@tab json
```json
{
  "success": true,
  "message": "获取成功",
  "code": "0",
  "data": {
    "latitude": 39.908823,
    "longitude": 116.39747
  }
}
```
:::
### 返回参数说明

| 参数名  | 类型      | 说明                                 |
| ------- | --------- | ------------------------------------ |
| success | `Boolean` | 是否成功                             |
| message | `String`  | 返回信息                             |
| data    | `Object`  | 返回数据，具体结构根据方法不同而不同 |
| code    | `String`  | 错误码 0 代表成功                    |