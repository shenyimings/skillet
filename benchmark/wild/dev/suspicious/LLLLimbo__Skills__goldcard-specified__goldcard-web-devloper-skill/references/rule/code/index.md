# 代码编写规范

## 前言

随着前端项目的日益增多以及团队协作场景越来越频繁，我们期望拿到一个项目时能够快速熟悉和适应，也希望在遇到一个其它项目已有的功能时，能够快速复制过来进行使用。为了能够让大家专注于业务开发，针对不同的业务场景，我们从已有项目中提炼出目前常用的几套项目模板：web、大屏、h5、app、ue、小程序。项目模板它提供了一套标准化的项目结构和配置，旨在提高开发效率、保证代码质量、促进团队协作，并简化部署流程。在实际应用中，我们需要根据项目的具体需求对模板进行定制和调整，以便更好地满足项目的需求。

## 适用范围

所有==vue3==项目
新项目统一采用==vue3 + vite==
@[caniuse image](proxy)

## 命名规范

### 术语

- camelCase（`小驼峰`命名法 —— 首字母小写）
- PascalCase（`大驼峰`命名法 —— 首字母大写）
- kebab-case（连字符命名法——`短横线`连接）
- snake_case（蛇形命名法——`下划线`连接）
- SNAKE_CASE（`大蛇形`命名法——大写+下划线）
- case（`单名`）
- cases（`复数`）
- case.module（`点连接`）

### 命名参照

| 命名 | 适用对象 | 示例 | 备注 |
| - | - | - | - |
| `短横线`        | 项目、目录、v-bind、v-on、emit、id、class                                                                          | f2e-templeate-pc         | 1、第三方依赖目录除外；2、命名时优先考虑单名或复数                                |
| `小驼峰`        | 图片、html文件、js文件、ts文件、css文件、props、变量、方法名等。==路由path、路由name（影响较大，路由相关先不改）== | requestNormal.ts         | 1、api方法统一添加api前缀：apiLogin；2、操作类方法统一添加handle前缀：handleClick |
| `小驼峰+点连接` | api文件、store文件、route文件、typings文件、配置类文件                                                             | common.api.ts            | global.module.ts、index.route.ts、global.d.ts、config.pro.js、vite.config.pro.ts  |
| `大驼峰`        | vue文件、组件name、组件引入、构造函数、类、类型定义                                                                | MyComponent              | 所有.vue文件采用大驼峰，index.vue文件除外                                         |
| `大蛇形`        | 常量                                                                                                               | ETBC_SESSION_INVALID_URL | 适用于public/config、vuex的Mutation                                               |

## 项目结构规范

==实际应用时，可根据项目所需进行删除和调整。==

::: file-tree

- .vscode 
		- setting.json
- .husk 
		- commit-msg
- .build 
		- plugins.ts
- public
		- libs
				- lib.xx.js
- src 
		- apis 
				- xx.api.ts 
		- imgs 
				- fonts 
						- xx 
								- xx.ttf 
								- xx.eot 
								- xx.woff 
								- xx.woff2 
				- imgs 
						- xx 
								- xx.jpg 
								- xx.png 
		- components 
				- ui-table 
						- index.vue 
						- index.ts 
		- config 
				- options.ts 
		- core 
				- base 
						- index.ts 
		- hooks 
				- index.ts 
		- directives 
				- index.ts 
		- i18n 
				- zh-CN.json 
				- index.ts 
		- layout 
				- index.vue 
		- pages 
				- home 
						- index.route.ts 
						- index.vue 
		- store 
				- xx.module.ts 
				- index.ts 
		- styles 
				- reset.scss 
				- index.scss 
		- utils 
				- request.ts 
				- index.ts 
	- App.vue 
	- main.ts 
	- router.ts
- typings 
		- auto-import.d.ts 
		- global.d.ts 
		- env.d.ts 
		- components.d.ts
- Dockerfile
- mainpage.conf
- vite.config.ts
- package.json
  :::

### 代码示例

::: code-tabs

@tab index.vue

@[code vue](./demo1.vue)

@tab README.md
```bash
# 项目名称
xxx

## 项目运行

node版本：20.18.1（20+）

npm install
npm run dev
npm run build
```
:::

### 模板

- [h5](http://10.200.1.145/framework/web/f2e-templeate/f2e-templeate-h5)
- [大屏](http://10.200.1.145/framework/web/f2e-templeate/f2e-templeate-screen)
- [web](http://10.200.1.145/framework/web/f2e-templeate/f2e-templeate-web)
- [app](http://10.200.1.145/framework/web/f2e-templeate/f2e-templeate-app)
- [ue](http://10.200.1.145/framework/web/f2e-templeate/f2e-templeate-ue)
- [微信小程序](http://10.200.1.145/framework/web/f2e-templeate/f2e-templeate-applet)

## 参考文章

1. [Vue风格指南](https://v2.cn.vuejs.org/v2/style-guide/index.html)
2. [Web前端代码指南(vue3)](https://blog.csdn.net/qq_35940731/article/details/138134738)
