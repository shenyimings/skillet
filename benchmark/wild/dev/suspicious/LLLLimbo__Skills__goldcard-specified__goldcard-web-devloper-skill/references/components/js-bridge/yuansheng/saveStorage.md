### 4.1 保存数据到本地

**功能描述**

将数据持久化保存到本地存储，类似 localStorage，但由原生管理，数据更安全可靠。

**方法名称**`saveStorage`
::: code-tabs
@tab javascript
```javascript
esBridge.callNative("saveStorage", params, callback);
```
:::

**params 字段说明**

| 字段名 | 类型     | 必填 | 说明                        |
| ------ | -------- | ---- | --------------------------- |
| key    | `String` | 是   | 存储键名                    |
| value  | `String` | 否   | 存储值 不存在时进行键名清除 |

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
  "code": "040101",
  "data": {}
}
```
:::

**错误码说明**

| 错误码 | 说明         | 处理建议              |
| ------ | ------------ | --------------------- |
| 040101 | 参数错误     | 检查必要参数          |
| 040102 | 缺少回调参数 | 联系SDK开发者         |
| 040103 | 缺少存储键名 | 检查调用参数key       |
| 040104 | 存储失败     | 检查存储空间/文件损坏 |

**注意事项**

1. 存储键名不能为空或空字符串, 禁止出现 \0 \n \r 等控制字符
2. 高频写入的存储键名应尽量短
3. 如果保存的值为空，则删除该键值对
4. 如果保存的值为空字符串, 则更新该键值为空字符串
5. 存储空间有限，建议只保存必要数据
6. 不建议存储敏感信息（如密码），建议加密后存储
7. 保存的值只能是字符串, 复杂对象请通过 JSON 进行转换
8. Key 命名建议使用命名空间，如 `app_userInfo`、`app_settings`

**调用示例**
::: code-tabs
@tab javascript
```javascript
// 保存数据
let userData = {
  id: 10001,
  name: "张三"
};
let params = {
  key: "userInfo",
  value: JSON.stringify(userData),
};
esBridge.callNative("saveStorage", params, (result) => {
  if (result.success) {
    console.log("保存成功");
  } else {
    console.error("保存失败", result.message);
  }
});
```
:::