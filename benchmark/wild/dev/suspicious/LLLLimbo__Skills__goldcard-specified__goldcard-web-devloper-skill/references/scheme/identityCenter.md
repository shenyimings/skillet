# 门户设计方案

## 简介

门户是软件中心在经历 ETBC 无法轻量化、无法实现功能级权限设置、无法统一身份认证等背景下应运而生的系统。

对于前端而言，门户即门户与子应用的沟通桥梁，较多通用化的配置皆有门户完成，例如:多主题、多语言、消息通知等。

## 框架介绍

门户整体框架主要三种：

1. 自定义的页面。主要由门户主应用负责。例如：登录页、无权限访问页等。
2. 门户无 aside 页面。主要由门户主应用负责。例如：工作台、应用中心等。
3. 门户有 aside 页面。主要由门户+子应用负责。例如：各个业务板块的页面。

## 开发模式

各个业务板块进行开发时，只需开发灰色区域板块即可。将业务页面嵌入到门户中才能正常显示，只打开子应用页面时由于css变量未定义，就会出现错误的页面样式。

### 1、子应用初始化

线上运行的门户中的菜单是通过后台配置的。开发阶段为了方便开发调试，需要子应用将自己的菜单上报给门户，具体上报菜单的说明见[microAppInit](/components/web/utils/microAppInit)。


### 2、页面访问方式

门户公共开发环境地址为：[http://portal-dev.eslink.net.cn](http://portal-dev.eslink.net.cn)。开发子应用时将子应用地址通过url传给门户即可。例如子应用启动后的地址是`http://localhost:2000`，则完整的访问的完整路径为：

```bash
http://portal-dev.eslink.net.cn/portal/home-dev?url=http://localhost:2000
```

如果子应用中对接了后端接口，应该修改host然后用域名的方式访问子应用，这样能保证门户中的cookie可以在子应用中也有效。如：

```bash
http://portal-dev.eslink.net.cn/portal/home-dev?url=http://center.eslink.net.cn:2000
```

## 运行过程

主应用和子应用之间的交互过程大体上如下：

![](references/imgs/scheme/identityCenter/运行过程.svg)


### 1、配置数据
子应用初始化时从门户中能获取到的数据有：

- lang：当前语言
- profile： 当前用户信息
- margin： 子页面布局，结构类型为`{top: number, left: number }`
- theme：当前主题
- variablesRaw：全局css变量
- permissions：权限数据

### 2、菜单导航

在主应用中，左侧的为菜单[menu](http://10.200.1.145/web/platform/portal-front/blob/dev/src/core/navigate/menu.ts)，点击菜单后打开的页面为标签[tab](http://10.200.1.145/web/platform/portal-front/blob/dev/src/core/navigate/tab.ts)，通过[navigate](http://10.200.1.145/web/platform/portal-front/blob/dev/src/core/navigate/index.ts)统一管理。

`Navigate`实现了单例模式，可以通过以下方式使用：

```typescript
import Navigate from '@/core/navigate'

Navigate.Instance<Navigate>().init()
```

### 3、事件消息

主应用中定义了一些postMessage事件，用于实现不同场景下的需求。

|  事件名称   |    说明         |     参数        |
| ---------- | --------------- | -------------- |
| getInitConfig | 子应用从主应用中获取配置数据 | - |
| sessionInvalid | 子应用中session过期就调用该方法，可以跳转登录页 | - |
| showMessage | 让主应用弹出一个消息 | 同[ui-message](/components/web/ui-message/) |
| setTopLevel | 设置iframe的层级 | true: 设置为高层级；false：设置为低层级 | 
