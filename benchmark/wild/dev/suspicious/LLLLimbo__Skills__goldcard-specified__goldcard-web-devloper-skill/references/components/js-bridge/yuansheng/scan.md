### 6.1 扫码

**功能描述**

调用原生扫码功能，支持二维码、条形码等多种码制识别，返回扫描结果。

**方法名称**`scan`
::: code-tabs
@tab javascript
```javascript
esBridge.callNative("scan", callback);
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
    "qrResult": "https://www.example.com"
  }
}
```
:::

**返回字段说明**

| 字段名   | 类型     | 说明     |
| -------- | -------- | -------- |
| qrResult | `String` | 扫码结果 |

**返回数据结构（取消）**
::: code-tabs
@tab json
```json
{
  "success": false,
  "message": "扫码已取消",
  "code": "060103",
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
  "message": "缺少相机权限",
  "code": "060101",
  "data": {}
}
```
:::

**错误码说明**

| 错误码 | 说明         | 处理建议             |
| ------ | ------------ | -------------------- |
| 060101 | 缺少相机权限 | 引导用户授予相机权限 |
| 060102 | 缺少回调参数 | 联系SDK开发者        |
| 060103 | 扫码已取消   | -                    |

**注意事项**

1. 首次调用需要用户授予相机权限
2. 支持二维码、条形码等多种码制
3. 扫码界面有手电筒功能，方便在暗光环境下使用
4. 用户可以通过返回按钮取消扫码操作
5. 建议在调用前检查相机权限状态

**调用示例**
::: code-tabs
@tab javascript
```javascript
// 启动扫码
esBridge.callNative("scan", (result) => {
  if (result.success) {
    console.log("扫码成功", result);
    console.log("扫码结果:", result.data.qrResult);
    // 处理扫码结果，如跳转链接、解析数据等
    if (result.data.qrResult.startsWith('http')) {
      // 如果是链接，可以跳转浏览器
      esBridge.callNative("navigateToBrowser", {
        url: result.data.qrResult
      });
    }
  } else {
    console.error("扫码失败", result.message);
    if (result.code === "060101") {
      alert("请授予相机权限后重试");
    } else if (result.code === "060103") {
      console.log("用户取消扫码");
    }
  }
});
```
:::
