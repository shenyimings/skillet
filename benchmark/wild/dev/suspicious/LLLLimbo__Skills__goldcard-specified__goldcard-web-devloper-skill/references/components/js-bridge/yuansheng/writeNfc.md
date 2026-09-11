### 6.3 NFC写入

**功能描述**

向NFC标签写入文本数据，支持自定义超时时间和指定目标标签ID，数据以NDEF格式存储。

**方法名称**`writeNfc`
::: code-tabs
@tab javascript
```javascript
esBridge.callNative("writeNfc", params, callback);
```
:::

**params 字段说明**

| 字段名      | 类型     | 必填 | 默认值 | 说明                              |
| ----------- | -------- | ---- | ------ | --------------------------------- |
| data        | `String` | 是   | -      | 要写入的文本数据                  |
| timeout     | `Number` | 否   | 30     | 写入超时时间（秒）                |
| targetTagId | `String` | 否   | -      | 目标标签ID，为空时写入任意NFC标签 |

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

**返回数据结构（超时）**
::: code-tabs
@tab json
```json
{
   "success": false,
   "message": "NFC写入超时",
   "code": "060301",
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
   "code": "060302",
   "data": {}
}
```
:::

**错误码说明**

| 错误码 | 说明                          | 处理建议                     |
| ------ | ----------------------------- | ---------------------------- |
| 060301 | 缺少NFC权限                   | 引导用户授予NFC权限          |
| 060302 | 设备不支持NFC                 | 提示用户设备不支持NFC        |
| 060303 | NFC功能未启用                 | 引导用户在设置中启用NFC功能  |
| 060304 | 缺少回调参数                  | 联系SDK开发者                |
| 060305 | 参数错误                      | 检查必要参数                 |
| 060306 | NFC写入失败                   | 检查NFC标签是否可写入或重试  |
| 060307 | 缺少写入数据                  | 检查data参数是否为空         |
| 060308 | 不支持的标签类型              | 更换支持NDEF格式的NFC标签    |
| 060309 | NFC写入操作超时               | 增加超时时间或重新尝试       |
| 060310 | NFC操作正在进行中，请稍后重试 | 等待当前操作完成或中断后重试 |
| 060311 | NFC不可写入                   | 更换可写入的NFC标签          |
| 060312 | NFC容量不足                   | 减少写入数据长度             |
| 060313 | NFC操作被中断                 | 中断NFC操作执行后的返回      |

**注意事项**

1. 首次调用需要用户授予NFC权限
2. 设备需要支持NFC功能且已启用
3. 写入操作需要将设备背面靠近可写入的NFC标签
4. 只能写入支持NDEF格式的NFC标签
5. 标签必须是可写入状态（非只读）
6. 写入数据长度受NFC标签容量限制
7. 指定targetTagId时，只有匹配的标签才会被写入
8. 写入成功后原有数据会被覆盖
9. 同一时间只能执行一个NFC操作

**调用示例**
::: code-tabs
@tab javascript
```javascript
// 完整参数写入（指定标签ID和超时时间）
let fullParams = {
  data: "重要数据内容",
  timeout: 60,           // 60秒超时
  targetTagId: "a1b2c3d4" // 只写入指定ID的标签
};
esBridge.callNative("writeNfc", fullParams, (result) => {
  if (result.success) {
    console.log("指定标签写入成功");
  } else {
    console.error("写入失败", result.message);
    if (result.code === "060301") {
      console.log("写入超时");
    }
  }
});
```
:::
