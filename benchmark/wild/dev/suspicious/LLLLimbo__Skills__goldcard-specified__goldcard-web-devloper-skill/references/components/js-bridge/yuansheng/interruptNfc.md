### 6.4 中断NFC操作

**功能描述**

中断当前正在进行的NFC读取或写入操作，停止等待NFC标签响应。

**方法名称**`interruptNfc`
::: code-tabs
@tab javascript
```javascript
esBridge.callNative("interruptNfc", callback);
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
   "message": "缺少回调参数",
   "code": "060401",
   "data": {}
}
```
:::

**错误码说明**

| 错误码 | 说明         | 处理建议      |
| ------ | ------------ | ------------- |
| 060401 | 缺少回调参数 | 联系SDK开发者 |

**注意事项**

1. 可以随时调用此方法中断NFC操作
2. 中断操作会立即停止NFC前台分发
3. 中断后之前的读取或写入操作会提示被中断
4. 中断操作总是成功，即使没有正在进行的NFC操作
5. 建议在页面退出或用户主动取消时调用

**调用示例**
::: code-tabs
@tab javascript
```javascript
// 中断NFC操作
esBridge.callNative("interruptNfc", (result) => {
  if (result.success) {
    console.log("NFC操作已中断");
  } else {
    console.error("中断失败", result.message);
  }
});
```
:::
