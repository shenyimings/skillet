### 5.3 获取已安装的导航APP

**功能描述**

获取当前设备已安装的导航APP列表,支持识别主流导航应用。

**方法名称**`getInstalledNavApps`
::: code-tabs
@tab javascript
```javascript
esBridge.callNative("getInstalledNavApps", callback);
```
:::

**返回数据结构(成功)**
::: code-tabs
@tab json
```json
{
  "success": true,
  "message": "成功",
  "code": "0",
  "data": {
    "navApps": ["amap", "baidu", "tencent", "google", "apple"]
  }
}
```
:::

**返回字段说明**

| 字段名  | 类型            | 说明                     |
| ------- | --------------- | ------------------------ |
| navApps | `Array<String>` | 已安装的导航APP简称列表 |

**支持的导航APP简称**

| 简称    | 导航APP名称 | 包名/Bundle ID                  |
| ------- | ----------- | ------------------------------- |
| google  | Google Maps | com.google.android.apps.maps    |
| baidu   | 百度地图    | com.baidu.BaiduMap              |
| amap    | 高德地图    | com.autonavi.minimap            |
| tencent | 腾讯地图    | com.tencent.map                 |
| apple   | 苹果地图    | com.apple.Maps                  |

**返回数据结构(失败)**
::: code-tabs
@tab json
```json
{
  "success": false,
  "message": "缺少回调参数",
  "code": "050301",
  "data": {}
}
```
:::

**错误码说明**

| 错误码 | 说明         | 处理建议      |
| ------ | ------------ | ------------- |
| 050301 | 缺少回调参数 | 联系SDK开发者 |
| 050302 | 查询失败     | 重试或联系客服 |

**注意事项**

1. 返回的列表按应用名称排序
2. 如果设备未安装任何导航APP,返回空数组
3. 仅返回已知的主流导航应用（谷歌、百度、高德、腾讯和苹果）
4. 苹果地图只有ios设备支持

**调用示例**
::: code-tabs
@tab javascript
```javascript
// 获取已安装的导航APP
esBridge.callNative("getInstalledNavApps", (result) => {
  if (result.success) {
    console.log("已安装的导航APP:", result.data.navApps);
    if (result.data.navApps.length === 0) {
      alert("未检测到已安装的导航应用");
    } else {
      // 显示导航APP选择列表
      showNavAppSelector(result.data.navApps);
    }
  } else {
    console.error("获取导航APP失败", result.message);
  }
});
```
:::
