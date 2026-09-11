### 5.1 跳转外部浏览器

**功能描述**

跳转到手机默认浏览器打开指定链接。

**方法名称**`navigateToBrowser`
::: code-tabs
@tab javascript
```javascript
esBridge.callNative("navigateToBrowser", params);
```
:::

**params 字段说明**

| 字段名 | 类型     | 必填 | 说明     |
| ------ | -------- | ---- | -------- |
| url    | `String` | 是   | 链接地址 |

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
  "message": "参数错误",
  "code": "050101"
}
```
:::

**错误码说明**

| 错误码 | 说明         | 处理建议                           |
| ------ | ------------ | ---------------------------------- |
| 050101 | 参数错误     | 检查必要参数                       |
| 050102 | 缺少回调参数 | 联系SDK开发者                      |
| 050103 | 缺少链接地址 | 检查调用参数url                    |
| 050104 | 跳转失败     | 引导用户检查手机默认浏览器是否正常 |

**注意事项**

1. 浏览器使用系统默认浏览器, 如果配置异常需要引导用户检查系统配置
2. 地图、导航、下载等功能均可以通过外部浏览器跳转实现

**调用示例**
::: code-tabs
@tab javascript
```javascript
// 高德导航页
let params = {
  url: "https://uri.amap.com/navigation?to=116.39747,39.908823,%E5%8C%97%E4%BA%AC&mode=car&policy=0&src=NewOutworkCloud"
};
esBridge.callNative("navigateToBrowser", params, (result) => {
  if (!result.success) {
    console.error("跳转失败", result.message);
  }
});
```
:::