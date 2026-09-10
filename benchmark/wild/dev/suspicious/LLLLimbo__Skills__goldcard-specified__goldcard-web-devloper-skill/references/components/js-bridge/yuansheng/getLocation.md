### 1.1 获取手机当前定位信息

**功能描述**

调用原生高德定位 SDK，获取用户当前位置信息，支持返回经纬度坐标。

**方法名称**`getLocation`
::: code-tabs
@tab javascript
```javascript
esBridge.callNative("getLocation", callback);
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
    "latitude": 39.908823,
    "longitude": 116.39747
  }
}
```
:::

**返回字段说明**

| 字段名    | 类型     | 说明 |
| --------- | -------- | ---- |
| latitude  | `Number` | 维度 |
| longitude | `Number` | 经度 |

**返回数据结构（失败）**
::: code-tabs
@tab json
```json
{
  "success": false,
  "code": "010105",
  "message": "缺少定位权限",
  "data": {}
}
```
:::

**错误码说明**

| 错误码 | 说明             | 处理建议             |
| ------ | ---------------- | -------------------- |
| 010101 | 缺少定位权限     | 检查应用权限设置     |
| 010102 | 定位服务启动失败 | 检查高德 SDK 配置    |
| 010103 | 初始化失败       | 检查高德 SDK 配置    |
| 010104 | 定位失败         | 重试定位             |
| 010105 | 缺少权限         | 引导用户授予定位权限 |
| 010106 | 缺少回调参数     | 联系SDK开发者        |

**注意事项**

1. 首次调用需要用户授予定位权限
2. 定位可能需要 3-10 秒时间，请做好加载提示
3. 返回的坐标系为 GCJ-02（火星坐标系）
4. 室内定位精度可能较低
5. 同一时间只能执行一次定位请求

**调用示例**
::: code-tabs
@tab javascript
```javascript
// 获取位置
esBridge.callNative("getLocation", (result) => {
  if (result.success) {
    console.log("定位成功", result);
    console.log("经度:", result.data.longitude);
    console.log("纬度:", result.data.latitude);
  } else {
    console.error("定位失败", result.message);
  }
});
```
:::