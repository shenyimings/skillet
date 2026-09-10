# Ui Marker Show

地图上纯展示点位

1. 支持国内使用高德地图、国际使用mapbox（默认国内高德地图）
2. 支持国际地图底图多语言展示
3. 支持国内、国际地图点位展示
4. 坐标传入需为WGS-84

## 示例

### 高德地图点位展示

@[demo vue](./marker-show-demo1.vue)

### 国外地图点位展示

@[demo vue](./marker-show-demo2.vue)

## API

### Ui Marker Show 配置项

| 属性      | 说明                                                                    | 类型    | 默认值                                       |
| --------- | ----------------------------------------------------------------------- | ------- | -------------------------------------------- |
| inChina   | 国内还是国际，默认国内（true: 国内使用高德地图, false：国外使用mapbox） | Boolean | true                                         |
| language  | 国外地图语言，默认英语（inChina必须为false）                            | String  | 浏览器语言                                   |
| id        | 地图容器id                                                              | String  | map-box                                      |
| mapConfig | 地图配置                                                                | Object  | `{center: [116.397428, 39.90923], zoom: 15}` |

<a href="https://lbs.amap.com/api/javascript-api-v2/documentation#map">高德地图配置</a> <a href="https://maptalks.org/maptalks.js/api/1.x/Map.html#options">mapbox配置</a>

### 事件

| 事件名       | 说明                         | 参数                                         |
| ------------ | ---------------------------- | -------------------------------------------- |
| ready        | 地图初始化完成会触发该事件   | `{ mapInstance 地图实例, map 引入地图对象 }` |
| marker-click | 点击地图上某点位会触发该事件 | `{lng, lat }` WGS-84                         |

### 地图抛出方法

| 方法名    | 说明               | 参数                                                                                        |
| --------- | ------------------ | ------------------------------------------------------------------------------------------- |
| addMarker | 地图上渲染图标标记 | 两个参数： map, options = {} <br> map：地图实例 <br> options: 见下方marker options配置 <br> |

### mapbox抛出方法

| 方法名        | 说明                         | 参数                                                                                                                                |
| ------------- | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| fitMapboxView | 调整地图视图以适配所有标记点 | 三个参数map,markerList,options <br> map：地图实例 <br> markerList 地图点位<br> options 默认padding：20，maxZoom：15，duration：1000 |

### marker options 具体项

| 属性         | 必填 | 说明               | 类型   | 默认值                      |
| ------------ | ---- | ------------------ | ------ | --------------------------- |
| iconOptions  | 否   | 图标配置           | Object | `{ width: 24, height: 29 }` |
| position     | 是   | 经纬度信息         | Array  | []                          |
| text         | 否   | 文本信息           | String |                             |
| otherOptions | 否   | marker其它配置信息 | Object | {}                          |

<a href="https://lbs.amap.com/api/javascript-api-v2/documentation#marker">高德 otherOptions点位属性配置</a>
<br>
<a href="https://maptalks.org/maptalks.js/api/1.x/ui.UIMarker.html#options">mapbox otherOptions点位属性配置</a>
