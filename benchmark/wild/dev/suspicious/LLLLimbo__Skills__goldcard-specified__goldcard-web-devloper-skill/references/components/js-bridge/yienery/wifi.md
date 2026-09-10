# e-wifi

Wi-Fi 功能模块,从 uni-wifi 插件二次开发而来。

## 安装说明

将插件文件夹放入项目的 `uni_modules` 目录下即可使用。

## 使用方式

::: code-tabs
@tab javascript
```javascript
import * as EWifi from '@/uni_modules/e-wifi'

// 初始化 WiFi 模块
EWifi.startWifi({
  success: (res) => {
    console.log('WiFi模块初始化成功')
  },
  fail: (err) => {
    console.log('WiFi模块初始化失败', err)
  }
})
```
:::

## 平台兼容性

| API | App-Android | App-iOS | 说明 |
|:-:|:-:|:-:|:--|
| startWifi | √ | √ | 初始化WiFi模块 |
| stopWifi | √ | √ | 关闭WiFi模块 |
| getConnectedWifi | √ | √ | 获取已连接的WiFi信息 |
| getWifiList | √ | × | 获取WiFi列表(仅Android) |
| onGetWifiList | √ | × | 监听WiFi列表(仅Android) |
| offGetWifiList | √ | × | 移除WiFi列表监听(仅Android) |
| connectWifi | √ | × | 连接WiFi(仅Android) |
| onWifiConnected | √ | × | 监听WiFi连接(仅Android) |
| offWifiConnected | √ | × | 移除WiFi连接监听(仅Android) |
| onWifiConnectedWithPartialInfo | √ | × | 监听WiFi连接-部分信息(仅Android) |
| offWifiConnectedWithPartialInfo | √ | × | 移除WiFi连接监听-部分信息(仅Android) |
| connectIotDevice | √ | × | 连接IoT设备热点(仅Android) |
| disconnectIotDevice | √ | × | 断开IoT设备连接(仅Android) |

## 平台注意事项

### App-iOS平台

#### 功能限制

- **getWifiList/onGetWifiList/offGetWifiList**: iOS 系统限制,不支持获取周边 WiFi 列表
- **connectWifi**: iOS 系统限制,不支持直接连接 WiFi(需用户手动操作)
- **onWifiConnected/offWifiConnected**: iOS 系统限制,无法监听 WiFi 连接事件

#### 权限配置

1. **Access WiFi Information 能力**
   - 登录[苹果开发者网站](https://developer.apple.com)
   - 进入 "Certificates, Identifiers & Profiles" 页面
   - 选择对应的 App ID,确保开启 "Access WiFi information"
   - 保存后重新生成 profile 文件

2. **定位权限** (iOS 13+)
   - iOS 13 及以上系统获取 WiFi 信息需要定位权限
   - 使用 `getConnectedWifi` 时会自动触发定位权限申请弹窗
   - 需在 `manifest.json` 的 `ios > privacyDescription` 中配置:

     ::: code-tabs
     @tab json

     ```json
     "NSLocationWhenInUseUsageDescription": "需要定位权限以获取WiFi信息"
     ```

     :::

3. **Info.plist 配置**
   - 插件已包含必要的配置文件 `uni_modules/e-wifi/utssdk/app-ios/Info.plist`

### App-Android平台

#### 权限要求

插件的 `AndroidManifest.xml` 已包含以下权限,无需手动配置:

::: code-tabs
@tab xml

```xml
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE"/>
<uses-permission android:name="android.permission.CHANGE_WIFI_STATE"/>
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>
```

:::

#### 运行时权限

- 首次调用 `startWifi` 时会自动请求定位权限(Android 6.0+)
- 需要定位权限才能获取 WiFi 列表和连接信息

#### 版本限制

- **connectWifi**: Android 10 (API 29) 及以上系统不支持直接连接 WiFi
  - 可使用 `maunal: true` 参数引导用户手动连接
- **minSdkVersion**: 19 (Android 4.4)

## API 文档

### startWifi(options)

初始化 Wi-Fi 模块。

**参数说明**

| 参数 | 类型 | 必填 | 说明 |
|:--|:--|:--|:--|
| success | Function | 否 | 接口调用成功的回调函数 |
| fail | Function | 否 | 接口调用失败的回调函数 |
| complete | Function | 否 | 接口调用结束的回调函数(成功、失败都会执行) |

**示例代码**

::: code-tabs
@tab javascript

```javascript
import * as EWifi from '@/uni_modules/e-wifi'

EWifi.startWifi({
  success: (res) => {
    console.log('WiFi模块已启动', res)
  },
  fail: (err) => {
    console.error('启动失败', err)
  }
})
```

:::

### stopWifi(options)

关闭 Wi-Fi 模块。

**参数说明**

| 参数 | 类型 | 必填 | 说明 |
|:--|:--|:--|:--|
| success | Function | 否 | 接口调用成功的回调函数 |
| fail | Function | 否 | 接口调用失败的回调函数 |
| complete | Function | 否 | 接口调用结束的回调函数 |

### getConnectedWifi(options)

获取已连接的 Wi-Fi 信息。

**平台支持**: Android、iOS

**参数说明**

| 参数 | 类型 | 必填 | 说明 |
|:--|:--|:--|:--|
| partialInfo | Boolean | 否 | 是否只返回部分信息(仅SSID) |
| success | Function | 否 | 接口调用成功的回调函数 |
| fail | Function | 否 | 接口调用失败的回调函数 |
| complete | Function | 否 | 接口调用结束的回调函数 |

**success 返回参数**

::: code-tabs
@tab typescript

```typescript
{
  wifi: {
    SSID: string,        // WiFi 的 SSID
    BSSID?: string,      // WiFi 的 BSSID
    secure?: boolean,    // WiFi 是否安全
    signalStrength?: number,  // WiFi 信号强度(Android: 0-100)
    frequency?: number   // WiFi 频率(单位MHz)
  }
}
```

:::

**示例代码**

::: code-tabs
@tab javascript

```javascript
EWifi.getConnectedWifi({
  partialInfo: false,
  success: (res) => {
    console.log('当前连接的WiFi:', res.wifi.SSID)
    console.log('信号强度:', res.wifi.signalStrength)
  },
  fail: (err) => {
    console.error('获取失败:', err.errMsg)
  }
})
```

:::

### getWifiList(options)

请求获取 Wi-Fi 列表。

**平台支持**: 仅 Android

**注意**: wifiList 数据会在 `onGetWifiList` 注册的回调中返回。

**参数说明**

| 参数 | 类型 | 必填 | 说明 |
|:--|:--|:--|:--|
| success | Function | 否 | 接口调用成功的回调函数 |
| fail | Function | 否 | 接口调用失败的回调函数 |
| complete | Function | 否 | 接口调用结束的回调函数 |

**示例代码**

::: code-tabs
@tab javascript

```javascript
// 先注册监听
EWifi.onGetWifiList((res) => {
  console.log('WiFi列表:', res.wifiList)
  res.wifiList.forEach(wifi => {
    console.log(`SSID: ${wifi.SSID}, 信号: ${wifi.signalStrength}`)
  })
})

// 再请求获取
EWifi.getWifiList({
  success: (res) => {
    console.log('开始扫描WiFi')
  }
})
```

:::

### onGetWifiList(callback)

监听获取到 Wi-Fi 列表数据事件。

**平台支持**: 仅 Android

**注意**: `onGetWifiList` 注册的回调会在接收一次数据后被回收。

**参数说明**

| 参数 | 类型 | 必填 | 说明 |
|:--|:--|:--|:--|
| callback | Function | 是 | WiFi列表数据回调函数 |

**callback 参数**

::: code-tabs
@tab typescript

```typescript
{
  wifiList: Array<{
    SSID: string,
    BSSID?: string,
    secure?: boolean,
    signalStrength?: number,
    frequency?: number
  }>
}
```

:::

### offGetWifiList(callback)

移除获取 Wi-Fi 列表数据事件的监听函数。

**平台支持**: 仅 Android

**参数说明**

| 参数 | 类型 | 必填 | 说明 |
|:--|:--|:--|:--|
| callback | Function | 否 | 要移除的监听函数,不传则移除所有监听 |

### connectWifi(options)

连接 Wi-Fi。

**平台支持**: 仅 Android (Android 10+ 仅支持手动模式)

**参数说明**

| 参数 | 类型 | 必填 | 说明 |
|:--|:--|:--|:--|
| SSID | String | 是 | WiFi 的 SSID |
| BSSID | String | 否 | WiFi 的 BSSID |
| password | String | 否 | WiFi 密码 |
| maunal | Boolean | 否 | 是否手动连接(Android 10+必须为true) |
| partialInfo | Boolean | 否 | 是否只返回部分信息 |
| success | Function | 否 | 接口调用成功的回调函数 |
| fail | Function | 否 | 接口调用失败的回调函数 |
| complete | Function | 否 | 接口调用结束的回调函数 |

**示例代码**

::: code-tabs
@tab javascript

```javascript
EWifi.connectWifi({
  SSID: 'MyWiFi',
  password: '12345678',
  success: (res) => {
    console.log('连接成功', res)
  },
  fail: (err) => {
    if (err.errCode === 12001) {
      // Android 10+ 系统不支持,使用手动模式
      EWifi.connectWifi({
        maunal: true,
        success: () => {
          console.log('已打开WiFi设置页面')
        }
      })
    }
  }
})
```

:::

### onWifiConnected(callback)

监听连接上 Wi-Fi 的事件。

**平台支持**: 仅 Android

**参数说明**

| 参数 | 类型 | 必填 | 说明 |
|:--|:--|:--|:--|
| callback | Function | 是 | WiFi连接成功的回调函数 |

### offWifiConnected(callback)

移除连接上 Wi-Fi 的事件的监听函数。

**平台支持**: 仅 Android

**参数说明**

| 参数 | 类型 | 必填 | 说明 |
|:--|:--|:--|:--|
| callback | Function | 否 | 要移除的监听函数,不传则移除所有监听 |

### onWifiConnectedWithPartialInfo(callback)

监听连接上 Wi-Fi 的事件(仅返回 SSID)。

**平台支持**: 仅 Android

**参数说明**

| 参数 | 类型 | 必填 | 说明 |
|:--|:--|:--|:--|
| callback | Function | 是 | WiFi连接成功的回调函数 |

### offWifiConnectedWithPartialInfo(callback)

移除连接上 Wi-Fi 的事件的监听函数(部分信息版本)。

**平台支持**: 仅 Android

**参数说明**

| 参数 | 类型 | 必填 | 说明 |
|:--|:--|:--|:--|
| callback | Function | 否 | 要移除的监听函数,不传则移除所有监听 |

### connectIotDevice(options)

连接 IoT 设备热点(SoftAP 直连)。专门用于配网场景,手机作为客户端连接设备开启的热点。

**平台支持**: 仅 Android

**技术实现**:
- Android 10+ (API 29+): 使用 `WifiNetworkSpecifier` API,需用户在系统弹窗中确认连接
- Android 9 及以下: 使用传统 `WifiManager` API,自动切换网络

**特性**:
- 自动根据 Android 版本选择合适的连接方式
- 移除 `NET_CAPABILITY_INTERNET` 能力,支持无网热点
- 自动绑定进程流量到 WiFi 接口,防止回退到移动数据

**参数说明**

| 参数 | 类型 | 必填 | 说明 |
|:--|:--|:--|:--|
| SSID | String | 是 | IoT 设备的 WiFi SSID |
| password | String | 是 | IoT 设备的 WiFi 密码 |
| BSSID | String | 否 | IoT 设备的 BSSID(可选) |
| timeout | Number | 否 | 连接超时时间(毫秒),默认 30000 |
| success | Function | 否 | 接口调用成功的回调函数 |
| fail | Function | 否 | 接口调用失败的回调函数 |
| complete | Function | 否 | 接口调用结束的回调函数 |

**示例代码**

::: code-tabs
@tab javascript

```javascript
import * as EWifi from '@/uni_modules/e-wifi'

// 连接 IoT 设备热点
EWifi.connectIotDevice({
  SSID: 'ESP32-Device-AP',
  password: '12345678',
  timeout: 30000,
  success: (res) => {
    console.log('成功连接到 IoT 设备热点')

    // 现在可以与设备通信,发送配网信息
    // 例如: 发送路由器 SSID 和密码给设备
    sendConfigToDevice({
      routerSSID: 'Home-WiFi',
      routerPassword: 'password123'
    })
  },
  fail: (err) => {
    console.error('连接失败:', err.errMsg)
    if (err.errCode === 12007) {
      uni.showToast({
        title: '用户拒绝连接或超时',
        icon: 'none'
      })
    }
  },
  complete: () => {
    console.log('连接请求已完成')
  }
})
```

:::

**注意事项**:
- Android 10+ 会弹出系统弹窗,需用户手动确认连接(或打开设置-WiFi, 需要点击下已指定的SSID)
- 连接成功后,App 的所有网络流量会被绑定到该 WiFi,无法访问互联网
- 配网完成后,应调用 `disconnectIotDevice` 解除绑定

### disconnectIotDevice(options)

断开 IoT 设备连接,解除进程的网络流量绑定。

**平台支持**: 仅 Android

**参数说明**

| 参数 | 类型 | 必填 | 说明 |
|:--|:--|:--|:--|
| success | Function | 否 | 接口调用成功的回调函数 |
| fail | Function | 否 | 接口调用失败的回调函数 |
| complete | Function | 否 | 接口调用结束的回调函数 |

**示例代码**

::: code-tabs
@tab javascript

```javascript
// 配网完成后,断开 IoT 设备连接
EWifi.disconnectIotDevice({
  success: (res) => {
    console.log('已断开 IoT 设备连接')
    // 流量绑定已解除,App 可以正常访问互联网
  },
  fail: (err) => {
    console.error('断开失败:', err.errMsg)
  }
})
```

:::

## IoT 设备配网完整流程示例

::: code-tabs
@tab javascript

```javascript
import * as EWifi from '@/uni_modules/e-wifi'

export default {
  methods: {
    // 完整的 IoT 设备配网流程
    async configIotDevice() {
      try {
        // 1. 连接到 IoT 设备的热点
        await this.connectToDevice()

        // 2. 向设备发送路由器信息
        await this.sendWifiConfig()

        // 3. 断开设备热点连接
        await this.disconnectFromDevice()

        uni.showToast({
          title: '配网成功',
          icon: 'success'
        })
      } catch (error) {
        uni.showToast({
          title: '配网失败: ' + error,
          icon: 'none'
        })
      }
    },

    // 连接到设备热点
    connectToDevice() {
      return new Promise((resolve, reject) => {
        EWifi.connectIotDevice({
          SSID: 'IoT-Device-AP',
          password: '12345678',
          timeout: 30000,
          success: () => {
            console.log('已连接到设备热点')
            resolve()
          },
          fail: (err) => {
            reject(err.errMsg)
          }
        })
      })
    },

    // 向设备发送路由器配置
    sendWifiConfig() {
      return new Promise((resolve, reject) => {
        // 通过 HTTP/Socket 等方式向设备发送配置
        uni.request({
          url: 'http://192.168.4.1/config', // 设备的 IP
          method: 'POST',
          data: {
            ssid: 'Home-Router',
            password: 'router-password'
          },
          success: (res) => {
            if (res.statusCode === 200) {
              console.log('配置已发送到设备')
              resolve()
            } else {
              reject('设备返回错误')
            }
          },
          fail: (err) => {
            reject('发送配置失败: ' + err.errMsg)
          }
        })
      })
    },

    // 断开设备连接
    disconnectFromDevice() {
      return new Promise((resolve, reject) => {
        EWifi.disconnectIotDevice({
          success: () => {
            console.log('已断开设备连接')
            resolve()
          },
          fail: (err) => {
            reject(err.errMsg)
          }
        })
      })
    }
  }
}
```

:::

## 错误码

| 错误码 | 说明 | 备注 |
|:--|:--|:--|
| 12000 | 未初始化 | 需先调用 startWifi |
| 12001 | 系统不支持 | 当前系统不支持该功能 |
| 12002 | 密码错误 | WiFi 密码错误 |
| 12005 | WiFi 未开启 | Android 特有,未打开 WiFi 开关 |
| 12007 | 用户拒绝授权 | 用户拒绝授权连接 WiFi 或定位权限 |
| 12010 | 系统错误 | 其他系统错误 |
| 12013 | WiFi 配置过期 | Android 特有,建议忘记 WiFi 后重试 |

## 完整示例

::: code-tabs
@tab javascript

```javascript
import * as EWifi from '@/uni_modules/e-wifi'

export default {
  data() {
    return {
      wifiList: [],
      currentWifi: null
    }
  },
  methods: {
    // 初始化并获取WiFi信息
    async initWifi() {
      // 1. 启动WiFi模块
      EWifi.startWifi({
        success: () => {
          console.log('WiFi模块已启动')

          // 2. 获取当前连接的WiFi
          this.getCurrentWifi()

          // 3. 注册WiFi列表监听 (仅Android)
          // #ifdef APP-ANDROID
          EWifi.onGetWifiList((res) => {
            this.wifiList = res.wifiList
          })

          // 4. 获取WiFi列表
          EWifi.getWifiList({
            success: () => {
              console.log('开始扫描WiFi列表')
            }
          })
          // #endif
        }
      })
    },

    // 获取当前连接的WiFi
    getCurrentWifi() {
      EWifi.getConnectedWifi({
        success: (res) => {
          this.currentWifi = res.wifi
          console.log('当前WiFi:', res.wifi.SSID)
        },
        fail: (err) => {
          console.error('获取WiFi失败:', err.errMsg)
        }
      })
    },

    // 连接指定WiFi (仅Android)
    connectToWifi(ssid, password) {
      // #ifdef APP-ANDROID
      EWifi.connectWifi({
        SSID: ssid,
        password: password,
        success: (res) => {
          uni.showToast({
            title: '连接成功',
            icon: 'success'
          })
        },
        fail: (err) => {
          if (err.errCode === 12001) {
            // Android 10+ 使用手动模式
            EWifi.connectWifi({
              maunal: true
            })
          } else {
            uni.showToast({
              title: '连接失败: ' + err.errMsg,
              icon: 'none'
            })
          }
        }
      })
      // #endif
    },

    // 停止WiFi模块
    stopWifi() {
      // #ifdef APP-ANDROID
      EWifi.offGetWifiList()
      // #endif

      EWifi.stopWifi({
        success: () => {
          console.log('WiFi模块已停止')
        }
      })
    }
  },

  onUnload() {
    this.stopWifi()
  }
}
```

:::

## 参考文档

- [uni-app WiFi API 官方文档](https://uniapp.dcloud.net.cn/api/system/wifi.html)

