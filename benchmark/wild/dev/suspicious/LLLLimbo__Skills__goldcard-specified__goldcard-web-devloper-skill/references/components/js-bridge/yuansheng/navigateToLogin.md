### 5.2 跳转登录页

**功能描述**

当鉴权失效时，跳转到登录页获取新的鉴权信息。

**方法名称**`navigateToLogin`
::: code-tabs
@tab javascript
```javascript
esBridge.callNative("navigateToLogin");
```
:::

**注意事项**

1. 跳转到登录页会回退并关闭当前页面, 需要做好页面临时数据的维护

**调用示例**
::: code-tabs
@tab javascript
```javascript
// 跳转登录页
esBridge.callNative("navigateToLogin");
```
:::
