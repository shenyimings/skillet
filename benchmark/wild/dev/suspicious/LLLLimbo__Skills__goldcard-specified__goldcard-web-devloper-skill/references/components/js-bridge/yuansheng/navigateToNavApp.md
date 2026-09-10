### 5.4 跳转导航APP

**功能描述**

调用指定的导航APP进行导航,支持设置目的地坐标和导航模式。

**方法名称**`navigateToNavApp`
::: code-tabs
@tab javascript
```javascript
esBridge.callNative("navigateToNavApp", params, callback);
```
:::

**params 字段说明**

| 字段名    | 类型     | 必填 | 默认值  | 说明                                                                    |
| --------- | -------- | ---- | ------- | ----------------------------------------------------------------------- |
| navApp    | `String` | 是   | -       | 导航APP简称(见上表)                                                     |
| latitude  | `Number` | 是   | -       | 目的地纬度                                                              |
| longitude | `Number` | 是   | -       | 目的地经度                                                              |
| destName  | `String` | 否   | "目的地" | 目的地名称                                                              |
| mode      | `String` | 否   | "drive" | 导航模式<br/>`"drive"`: 驾车<br/>`"walk"`: 步行<br/>`"bus"`: 公交<br/>`"ride"`: 骑行 |

**返回数据结构(成功)**
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

**返回数据结构(失败)**
::: code-tabs
@tab json
```json
{
  "success": false,
  "message": "未安装该导航应用",
  "code": "050401",
  "data": {}
}
```
:::

**错误码说明**

| 错误码 | 说明              | 处理建议                       |
| ------ | ----------------- | ------------------------------ |
| 050401 | 未安装该导航应用  | 提示用户安装或选择其他导航APP  |
| 050402 | 参数错误          | 检查必要参数                   |
| 050403 | 缺少回调参数      | 联系SDK开发者                  |
| 050404 | 导航APP简称不支持 | 检查调用参数navApp是否在支持列表 |
| 050405 | 坐标参数无效      | 检查经纬度范围是否合法         |
| 050406 | 启动导航失败      | 检查应用权限或重试             |

**注意事项**

1. 坐标系说明: SDK不会自动转换坐标系,需要根据目标导航APP传入对应的坐标系。不同导航APP要求的坐标系如下:
   - 高德地图(amap): 需要传入 `GCJ-02`坐标系(火星坐标系)
   - 腾讯地图(tencent): 需要传入 `GCJ-02`坐标系(火星坐标系)
   - 百度地图(baidu): 需要传入 `WGS-84`坐标系(地球坐标系)
   - Google Maps(google): 需要传入 `WGS-84`坐标系(地球坐标系)
   - 苹果地图(apple): 需要传入 `WGS-84`坐标系(地球坐标系)
2. 建议先调用 `getInstalledNavApps` 获取可用的导航APP
3. 不同导航APP对导航模式的支持可能不同，当不支持某些导航模式时会自动降级，如骑行模式不支持时会降级为步行模式
4. 经度范围: -180 ~ 180,纬度范围: -90 ~ 90

**调用示例**
::: code-tabs
@tab javascript
```javascript
// 使用高德地图导航到天安门(驾车模式)
let params = {
  navApp: "amap",
  latitude: 39.908823,
  longitude: 116.39747,
  destName: "天安门",
  mode: "drive"
};
esBridge.callNative("navigateToNavApp", params, (result) => {
  if (result.success) {
    console.log("导航启动成功");
  } else {
    console.error("导航启动失败", result.message);
    if (result.code === "050301") {
      alert("您尚未安装高德地图,请先安装或选择其他导航应用");
    }
  }
});

// 完整示例:选择导航APP并启动
function startNavigation(lat, lng, name) {
  // 1. 先获取已安装的导航APP
  esBridge.callNative("getInstalledNavApps", (result) => {
    if (result.success && result.data.navApps.length > 0) {
      // 2. 如果只有一个,直接使用
      if (result.data.navApps.length === 1) {
        launchNav(result.data.navApps[0], lat, lng, name);
      } else {
        // 3. 多个时显示选择列表
        showNavSelector(result.data.navApps, lat, lng, name);
      }
    } else {
      alert("未检测到已安装的导航应用");
    }
  });
}

function launchNav(navApp, lat, lng, name) {
  let params = {
    navApp: navApp,
    latitude: lat,
    longitude: lng,
    destName: name,
    mode: "drive"
  };
  esBridge.callNative("navigateToNavApp", params, (result) => {
    if (!result.success) {
      alert("导航启动失败: " + result.message);
    }
  });
}
```
:::
