封装的 localStorage 存储工具函数，支持自动序列化/反序列化不同类型的数据，并可以根据组件上下文自动生成存储键名。

## 安装

```bash
npm install @eslink-plus/utils
```

## 基本用法

```typescript
import { useStorage } from '@eslink-plus/utils'

// 创建存储实例
const storage = useStorage('userInfo')

// 存储数据
storage.set({ name: 'John', age: 20 })

// 获取数据
const data = storage.get()

// 删除数据
storage.remove()
```

## API

### useStorage(key: string, options?: useStorageOptions): useStorageType

#### 参数

- `key` (string): 存储键名
- `options` (可选): 配置选项
  - `useContext` (boolean): 是否使用组件上下文路径作为 key 前缀（默认为 false）
  - `useProfileId` (boolean): 是否使用用户配置 ID 作为 key 后缀（默认为 false）

#### 返回值

返回一个包含以下方法的对象：

- `get(): unknown` - 获取存储的数据
- `set(value: unknown): void` - 设置存储的数据
- `remove(): void` - 删除存储的数据

## 功能特性

### 自动类型序列化

支持以下数据类型的自动序列化和反序列化：

- **Object**: 对象类型（自动 JSON 序列化）
- **String**: 字符串
- **Number**: 数字
- **Boolean**: 布尔值
- **Symbol**: Symbol 类型
- **BigInt**: BigInt 类型
- **Function**: 函数类型
- **undefined**: undefined 值

### 上下文感知的键名生成

当启用 `useContext` 选项时，会自动基于组件层级结构生成唯一的存储键名：

```typescript
// 在组件中使用
const storage = useStorage('formData', { useContext: true })
// 生成的键名格式: key@pagePath/ComponentName/ParentComponentName
```

### 用户隔离存储

当启用 `useProfileId` 选项时，会自动基于用户配置 ID 生成隔离的存储键名：

```typescript
// 用户隔离存储
const storage = useStorage('preferences', { useProfileId: true })
// 生成的键名格式: key:profileId
```

## 高级用法

### 组件上下文

```typescript
// 在 Vue 组件中使用上下文感知存储
const formStorage = useStorage('formData', { useContext: true })

// 这样每个组件实例都会有独立的存储空间
formStorage.set({ field1: 'value1', field2: 'value2' })
```

### 用户上下文

```typescript
// 基于用户 ID 的隔离存储
const userPrefs = useStorage('preferences', { useProfileId: true })

// 不同用户的配置不会互相干扰
userPrefs.set({ theme: 'dark', language: 'zh-CN' })
```

### 组合使用

```typescript
// 同时使用上下文和用户隔离
const advancedStorage = useStorage('data', {
  useContext: true,
  useProfileId: true
})
// 生成的键名格式: key:profileId@pagePath/ComponentPath
```

## 类型支持

### useStorageType

```typescript
type useStorageType = {
  get: () => unknown
  set: (value: unknown) => void
  remove: () => void
}
```

### useStorageOptions

```typescript
type useStorageOptions = {
  useContext?: boolean
  useProfileId?: boolean
}
```

## 注意事项

1. **SSR 兼容**: 在服务端渲染环境下会自动跳过 localStorage 操作
2. **数据类型保持**: 存储和读取时会保持原始数据类型
3. **键名冲突**: 使用上下文感知时要注意键名长度可能较长
4. **性能考虑**: 频繁的组件上下文解析可能影响性能，建议在需要时使用

## 示例

### 基本数据存储

```typescript
const storage = useStorage('appSettings')

// 存储各种类型数据
storage.set('hello')                    // 字符串
storage.set(42)                         // 数字
storage.set(true)                       // 布尔值
storage.set({ key: 'value' })           // 对象
storage.set(Symbol('test'))             // Symbol
storage.set(9007199254740991n)          // BigInt
storage.set(() => console.log('test'))  // 函数
storage.set(undefined)                  // undefined
```

### 组件状态持久化

```typescript
// 在组件中保持表单状态
const formStorage = useStorage('formState', { useContext: true })

// 组件挂载时恢复状态
onMounted(() => {
  const savedState = formStorage.get()
  if (savedState) {
    Object.assign(form, savedState)
  }
})

// 表单变化时保存状态
watch(form, (newValue) => {
  formStorage.set(newValue)
}, { deep: true })
```
