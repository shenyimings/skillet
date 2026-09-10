### 6.2 NFC读取

**功能描述**

读取NFC标签数据，支持自定义超时时间，可获取标签ID和NDEF数据内容。

**方法名称**`readNfc`
::: code-tabs
@tab javascript
```javascript
esBridge.callNative("readNfc", params, callback);
```
:::

**params 字段说明**

| 字段名  | 类型     | 必填 | 默认值 | 说明               |
| ------- | -------- | ---- | ------ | ------------------ |
| timeout | `Number` | 否   | 30     | 读取超时时间（秒） |

**返回数据结构（成功）**
::: code-tabs
@tab json
```json
{
   "success": true,
   "message": "成功",
   "code": "0",
   "data": {
      "tagId": "a1b2c3d4",
      "data": ["Hello NFC World!", "Additional data"],
      "success": true
   }
}
```
:::

**返回字段说明**

| 字段名  | 类型            | 说明                                 |
| ------- | --------------- | ------------------------------------ |
| tagId   | `String`        | NFC标签唯一ID（十六进制）            |
| data    | `Array<String>` | NDEF记录数据数组(非NDEF标签无该字段) |
| success | `Boolean`       | 读取操作成功标志                     |

**返回数据结构（超时）**
::: code-tabs
@tab json
```json
{
   "success": false,
   "message": "NFC读取超时",
   "code": "060201",
   "data": {}
}
```
:::

**返回数据结构（失败）**
::: code-tabs
@tab json
```json
{
   "success": false,
   "message": "缺少NFC权限",
   "code": "060202",
   "data": {}
}
```
:::

**错误码说明**

| 错误码 | 说明            | 处理建议                     |
| ------ | --------------- | ---------------------------- |
| 060201 | NFC读取超时     | 增加超时时间或重新尝试       |
| 060202 | 缺少NFC权限     | 引导用户授予NFC权限          |
| 060203 | NFC功能未支持   | 提示用户设备不支持NFC        |
| 060204 | NFC功能未启用   | 引导用户在设置中启用NFC功能  |
| 060205 | 参数错误        | 检查必要参数                 |
| 060206 | 缺少回调参数    | 联系SDK开发者                |
| 060207 | 读取失败        | 检查NFC标签是否损坏或重试    |
| 060208 | 正在进行NFC操作 | 等待当前操作完成或中断后重试 |
| 060209 | NFC操作被中断   | 中断NFC操作执行后的返回      |

**注意事项**

1. 首次调用需要用户授予NFC权限
2. 设备需要支持NFC功能且已启用
3. 读取操作需要将设备背面靠近NFC标签
4. 支持读取NDEF格式的文本数据
5. 对于非NDEF标签，仅返回标签ID
6. 建议设置合理的超时时间，避免用户长时间等待
7. 同一时间只能执行一个NFC操作

**调用示例**
::: code-tabs
@tab javascript
```javascript
// 自定义超时读取
let params = {
  timeout: 10  // 设置60秒超时
};
esBridge.callNative("readNfc", params, (result) => {
  if (result.success) {
    console.log("NFC读取成功", result);
    console.log("标签ID:", result.data.tagId);
    console.log("数据内容:", result.data.data);

    // 处理读取到的数据
    if (result.data.data && result.data.data.length > 0) {
      result.data.data.forEach((text, index) => {
        console.log(`数据${index + 1}:`, text);
      });
    }
  } else {
    console.error("NFC读取失败", result.message);
    if (result.code === "060204") {
      alert("请在设置中启用NFC功能");
    } else if (result.code === "060201") {
      console.log("读取超时，请重新尝试");
    }
  }
});
```
:::
