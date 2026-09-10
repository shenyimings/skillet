# 插件名称 e-meshing

## 适配情况

|                           | Android | iOS  | 鸿蒙 |
| ------------------------- | ------- | ---- | ---- |
| 适配情况                  | ✅      | ✅   | ❌   |
| 最低版本                  | ≥ 21    | ≥ 13 | ❌   |
| 目标版本（targetVersion） | ≥ 33    | ——   | ❌   |



## 使用要求

1. 原生插件本地环境调试需要在自定义基座上使用，必须先打包自定义基座后再进行运行；
2. 因英臻蓝牙配网SDK强制验证了`android.permission.NEARBY_WIFI_DEVICES`权限，需要项目Android配置中targetSdkVersion>=33，否则会报定位权限错误；
3. 因英臻蓝牙配网SDK需要请求英臻服务进行鉴权，需要运行设备具备公共网络的访问能力；

## 基本使用

公开方法：==initSDK==, ==startConfig==, ==endConfig==, ==getLog==

### initSDK

初始化蓝牙配网SDK，初始化成功后，才可以调用startConfig方法进行配网。

#### 参数

| 名称 | 类型 | 必填 | 默认值 | 兼容性 | 描述 |
| - | - | - | - | - | - |
| appKey    | `string`                     | 是   | -      | -      | SDK密钥        |
| onSuccess | `(message : string) => void` | 是   | -      | -      | 初始化成功回调 |
| onFail    | `(message : string) => void` | 是   | -      | -      | 初始化失败回调 |

#### 返回值

| 类型 |
| ---- |
| void |

#### 示例

::: code-tabs
@tab index.js
@[code javascript](./demo1.js)
:::

### startConfig

启动配网，配网成功后，会返回配网结果。

#### 参数

| 名称 | 类型 | 必填 | 默认值 | 兼容性 | 描述 |
| - | - | - | - | - | - |
| sn | `string`                     | 是   | - | - | 设备SN码 |
| ssid | `string`                     | 是   | - | - | 要配置上的WIFI SSID |
| password | `string`             | 是 | - | - | WIFI密码 |
| onSuccess | `(message : string) => void` | 是 | - | - | 配网成功回调        |
| onFail | `(message : string) => void` | 是 | - | - | 配网失败回调 |

#### 返回值

| 类型 |
| ---- |
| void |

#### 示例

::: code-tabs
@tab index.js
@[code javascript](./demo2.js)
:::

### endConfig

结束或停止配网

#### 参数

无

#### 返回值

| 类型 |
| ---- |
| void |

#### 示例

::: code-tabs
@tab index.js
@[code javascript](./demo3.js)
:::

### getLog

获取上次配网日志

#### 参数

| 名称 | 类型 | 必填 | 默认值 | 兼容性 | 描述     |
| - | - | - | - | - | - |
| onSuccess | `(message : string) => void` | 是   | - | - | 成功回调 |
| onFail    | `(message : string) => void` | 是   | - | - | 失败回调 |

> 日志以JSONArray的格式化字符串形式返回, 元素为JSONObject, 包含以下字段:
>
> - `message`: 日志信息
> - `time`: 日志时间,时间戳格式

#### 返回值

| 类型 |
| ---- |
| void |

#### 示例

::: code-tabs
@tab index.js
@[code javascript](./demo4.js)
:::

## 业务码附录

| 业务码 | 业务码Key | 说明 | 插件提示 |
| - | - | - | - |
| 1000   | BLE_CODE_TYPE_OK                          | 配置成功                            | 配置成功                   |
| 1001   | BLE_CODE_TYPE_CHECK_OK                    | 鉴权成功                            | 鉴权成功                   |
| 3000   | BLE_CODE_TYPE_CONNECTING                  | 设备连接WiFi中                      | 设备连接WiFi中             |
| --     | 以下为异常码                              | --                                  | --                         |
| -1000  | BLE_CODE_TYPE_CHECK_FAILED                | 鉴权失败                            | 鉴权失败                   |
| -1001  | BLE_CODE_TYPE_NOT_POWER_ON                | 蓝⽛未授权、未开启、不⽀持          | 蓝牙未授权、未开启、不支持 |
| -1002  | BLE_CODE_TYPE_CONNECTED_WRONG_SSID        | 当前连接WiFi不是配置WiFi            | 当前连接WiFi不是配置WiFi   |
| -1003  | BLE_CODE_TYPE_SCAN_FAILED                 | 未扫描到蓝⽛设备                    | 未扫描到蓝牙设备           |
| -1004  | BLE_CODE_TYPE_CONNECT_FAILED              | 连接蓝⽛设备失败                    | 连接蓝牙设备失败           |
| -1005  | BLE_CODE_TYPE_FIND_SERVICE_FAILED         | 寻找蓝⽛服务失败                    | 寻找蓝牙服务失败           |
| -1006  | BLE_CODE_TYPE_FIND_CHARACTERISTICS_FAILED | 寻找蓝⽛Characteristics失败         | 寻找蓝牙特征值失败         |
| -1007  | BLE_CODE_TYPE_WRITE_FAILED                | 蓝⽛写⼊数据失败                    | 蓝牙写入数据失败           |
| -1008  | BLE_CODE_TYPE_DISCONNECTED                | 配置中蓝⽛断开连接                  | 配置中蓝牙断开连接         |
| -1009  | BLE_CODE_TYPE_UDP_CONNECT_FAILED          | UDP连接失败                         | UDP连接失败                |
| -1010  | BLE_CODE_TYPE_UDP_SEND_FAILED             | UDP发送数据失败                     | UDP发送数据失败            |
| -1011  | BLE_CODE_TYPE_LOCATION_ERROR              | 未授予定位权限                      | 未授予定位权限             |
| -1012  | BLE_CODE_TYPE_BLUETOOTH_ERROR             | 未授予蓝⽛权限                      | 未授予蓝牙权限             |
| -1013  | BLE_CODE_TYPE_LOCATION_DISABLE            | 未打开定位服务                      | 未打开定位服务             |
| -1020  | BLE_CODE_TYPE_TIMEOUT                     | 配置超时⽬前超时时间60s             | 配置超时                   |
| -2001  | BLE_SSID_RULE_ERROR                       | 传⼊WiFi的ssid不合规范              | WiFI的ssid不合规范         |
| -2002  | BLE_PASSWORD_ERROR                        | 传⼊WiFi的密码不合规范              | WiFi密码不合规范           |
| -2003  | BLE_SN_ERROR                              | 传⼊设备的SN号不合规范              | 设备SN号不合规范           |
| -2004  | BLE_CODE_TYPE_SSID_ERROR                  | 设备连接 WiFi异常⼀般是未找到该WiFi | 设备连接WiFi异常           |
| -2005  | BLE_CODE_TYPE_PASSWORD_ERROR              | 设备连接WiFi的密码不正确            | 设备连接WiFi的密码不正确   |
| -2006  | BLE_CODE_TYPE_OTHER_ERROR                 | 设备连接WiFi其他未知异常            | 设备连接WiFi其他未知异常   |

## 参考链接

- [安卓-SDK使用说明](https://alidocs.dingtalk.com/i/p/YRBGvEwVJxjJgmDA/docs/N7dx2rn0JbZxg5Q3TmmxReExJMGjLRb3)
- [iOS-SDK使用说明](https://alidocs.dingtalk.com/i/p/YRBGvEwVJxjJgmDA/docs/MNDoBb60VLrYwZMKsYY4N11O8lemrZQ3)
