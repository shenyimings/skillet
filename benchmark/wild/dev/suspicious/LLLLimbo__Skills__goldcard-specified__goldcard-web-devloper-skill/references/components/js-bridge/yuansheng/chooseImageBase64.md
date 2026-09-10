### 2.1 选择照片或拍照

**功能描述**

打开相册选择图片或调用相机拍照，支持多选，返回图片的 Base64 编码数据。

**方法名称**`chooseImageBase64`
::: code-tabs
@tab javascript
```javascript
esBridge.callNative("chooseImageBase64", params, callback);
```
:::

**params 字段说明**

| 字段名       | 类型                   | 必填 | 默认值 | 说明                                 |
| ------------ | ---------------------- | ---- | ------ | ------------------------------------ |
| sourceType   | `Array<camera\|album>` | 是   | -      | `"album"`: 相册<br/>`"camera"`: 拍照 |
| maxSelection | `Number`               | 否   | 1      | 最多可选择的图片数量（1-9）          |

**返回数据结构（成功）**
::: code-tabs
@tab json
```json
{
  "success": true,
  "message": "成功",
  "code": "0",
  "data": {
    "fileList": [
    "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0a...",
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9aw..."
    ],
    "origin": "camera"
  }
}
```
:::

**返回字段说明**

| 字段名   | 类型            | 说明                                              |
| -------- | --------------- | ------------------------------------------------- |
| fileList | `Array<String>` | 图片 Base64 编码数组                              |
| origin   | `String`        | 图片来源<br/>`"album"`: 相册<br/>`"camera"`: 拍照 |

**返回数据结构（取消）**
::: code-tabs
@tab json
```json
{
  "success": false,
  "message": "拍照已取消",
  "code": "020105",
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
  "message": "缺少拍照权限",
  "code": "020101",
  "data": {}
}
```
:::

**错误码说明**

| 错误码 | 说明           | 处理建议               |
| ------ | -------------- | ---------------------- |
| 020101 | 缺少拍照权限   | 引导用户授予定位权限   |
| 020102 | 参数错误       | 检查必要参数           |
| 020103 | 缺少回调参数   | 联系SDK开发者          |
| 020104 | 图片源参数错误 | 检查调用参数sourceType |
| 020105 | 拍照已取消     | -                      |
| 020106 | 拍照失败       | 检查权限配置           |
| 020107 | 图片转换失败   | 检查权限配置           |

**注意事项**

1. Base64 数据较大，建议压缩后再上传服务器
2. 多选图片时注意内存占用
3. 拍照模式下 `maxSelection` 固定为 1
4. 用户取消选择也会触发回调，`success` 为 `false`, `code` 为 `020105`

**调用示例**
::: code-tabs
@tab javascript
```javascript
// 相册或拍照（推荐）
let params = {
  sourceType: ["album", "camera"],
  maxSelection: 9,
};
esBridge.callNative("chooseImageBase64", params, (result) => {
  if (result.success) {
    console.log("获取图片成功", result);
    console.log("图片来源:", result.data.photoOrigin === "camera" ? "拍照" : "相册");
    console.log("图片数量:", result.data.fileList.length);
  } else {
    console.error("获取图片失败", result.message);
  }
});
```
:::