### 4.2 读取本地数据

**功能描述**

从本地存储中读取之前保存的数据。

**方法名称**`getStorage`
::: code-tabs
@tab javascript
```javascript
esBridge.callNative("getStorage", params, callback);
```
:::

**params 字段说明**

| 字段名 | 类型     | 必填 | 说明         |
| ------ | -------- | ---- | ------------ |
| key    | `String` | 是   | 要读取的键名 |

**返回数据结构（成功）**
::: code-tabs
@tab json
```json
{
  "success": true,
  "message": "成功",
  "code": "0",
  "data": {
    "value": "张三"
  }
}
```
:::

**返回字段说明**

| 字段名 | 类型     | 说明     |
| ------ | -------- | -------- |
| value  | `String` | 读取结果 |

**返回数据结构（不存在）**
::: code-tabs
@tab json
```json
{
  "success": true,
  "message": "成功",
  "code": "0",
  "data": {
    "value": null
  }
}
```
:::

**返回数据结构（失败）**
::: code-tabs
@tab json
```json
{
  "success": false,
  "code": "040204",
  "message": "获取失败",
  "data": {}
}
```
:::

**错误码说明**

| 错误码 | 说明         | 处理建议                      |
| ------ | ------------ | ----------------------------- |
| 040201 | 参数错误     | 检查必要参数                  |
| 040202 | 缺少回调参数 | 联系SDK开发者                 |
| 040203 | 缺少存储键名 | 检查调用参数key               |
| 040204 | 获取失败     | 对应值不存在,需要检查触发场景 |

**注意事项**

1. 读取结果的值为字符串格式
2. 当读取对象不存在值, 将会返回 null
3. 应该先校验读取的键值再进行调用, 否则将会返回错误

**调用示例**
::: code-tabs
@tab javascript
```javascript
// 读取信息
let params = {
  key: "userInfo"
};
esBridge.callNative("getStorage", params, (result) => {
  if (result.success) {
    console.log("读取成功", result.data.value);
  } else {
    console.error("读取失败", result.message);
  }
});
```
:::