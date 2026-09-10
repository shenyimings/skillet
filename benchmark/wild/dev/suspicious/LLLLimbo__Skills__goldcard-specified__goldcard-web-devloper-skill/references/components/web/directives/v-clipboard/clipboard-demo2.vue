<template>
  <div class="demo-section">
    <div class="demo-item">
      <p>文本输入框：</p>
      <input v-clipboard.text type="text" value="输入框内容" class="form-element">
    </div>

    <div class="demo-item">
      <p>复选框：</p>
      <label>
        <input v-clipboard.text type="checkbox" checked>
        选项一
      </label>
      <p class="tip">复制结果: "选项一: 已选中"</p>
    </div>

    <div class="demo-item">
      <p>单选按钮：</p>
      <label>
        <input v-clipboard.text type="radio" name="group" checked>
        选项A
      </label>
      <p class="tip">复制结果: "选项A"</p>
    </div>

    <div class="demo-item">
      <p>下拉选择框：</p>
      <select v-clipboard.text v-model="selectValue" class="form-element">
        <option value="1">选项一</option>
        <option value="2">选项二</option>
        <option value="3">选项三</option>
      </select>
      <p class="tip">复制结果: 选中选项的文本内容</p>
    </div>

    <div class="demo-item">
      <p>多选下拉框：</p>
      <select v-clipboard.text.contextmenu.prevent.stop multiple v-model="multiSelectValue" class="form-element">
        <option value="1">选项一</option>
        <option value="2">选项二</option>
        <option value="3">选项三</option>
      </select>
      <p class="tip">复制结果: "选项一, 选项二"</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const selectValue = ref('2')
const multiSelectValue = ref(['1', '2'])
</script>

<style scoped>
.form-element {
  margin: 5px 0;
  padding: 5px 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.tip {
  font-size: 12px;
  color: #666;
  margin: 5px 0 0 0;
}
</style>