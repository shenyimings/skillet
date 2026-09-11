<template>
	<!-- 属性顺序推荐：固定属性 > v-bind(:) > v-on(@) -->
	<el-dialog
		ref="dialogRef"
		v-model="dialogVisible"
		class="gc-dialog"
		draggable
		:width="width"
		:append-to-body="appendToBody"
		@open="handleOpen"
		@close="handleClose"
	>
		<div class="gc-dialog-header">
			<div class="gc-dialog-header-left">
				<!-- class命名不宜过长，最多3个短横线 -->
				<div class="icon">
					<!-- 无slot采用自闭合 -->
					<GcIcon />
				</div>
				<div class="title">
					<TitleComponent>
						<div></div>
					</TitleComponent>
				</div>
			</div>
			<div class="gc-dialog-header-right"></div>
		</div>
		<div class="gc-dialog-body">
			<slot></slot>
		</div>
		<slot v-if="$slots.footer" name="footer"></slot>
		<div v-else class="gc-dialog-footer">
			<div class="gc-dialog-footer-left"></div>
			<div class="gc-dialog-footer-right"></div>
		</div>
	</el-dialog>
</template>

<script lang="ts" setup>
/**
 * 多行注释
 * 1、import引入顺序
 * 1-1、官方/生态 方法、类型
 * 1-2、全局方法、类型、组件
 * 1-3、依赖方法、类型、组件
 * 1-4、局部方法、类型、组件
 */
// 单行注释
import { reactive } from 'vue';
import { ElMessage } from 'element-plus';
import globalModule from '@/store/global.module';
import TitleComponent from './TitleComponent.vue';

// 2、组件name，Vue3.3版本之前需安装 unplugin-vue-define-options 插件，Vue3.3版本之后内置支持
defineOptions({
	name: 'GcDialog',
});

// 3、定义类型接口
interface RuleForm {
	name: string;
	age?: number;
}

// 4、props、emits
const props = defineProps({
	modelValue: {
		required: true,
		type: Boolean,
		default: false,
	},
	width: {
		type: [String, Number],
		default: '500px',
	},
	appendToBody: {
		type: Boolean,
		default: false,
	},
});
const emits = defineEmits(['update:modelValue', 'open', 'close']);

// 5、定义数据（多功能不分开写，尽量拆组件）
const count = ref(0);
const dialogRef = ref();
const ruleForm = reactive<RuleForm>({
	name: '',
	age: 0,
});

// 6、定义计算属性
const dialogVisible = computed({
	get: () => props.modelValue,
	set: (val) => emits('update:modelValue', val),
});
const plusOne = computed(() => count.value + 1);

// 7、定义数据监视
watch(dialogVisible, () => {});
watch(
	() => ruleForm.name,
	(newValue, oldvalue) => {},
	{ deep: true }
);

/**
 * 8、定义方法
 * 函数参数不超过 3 个
 */
const handleOpen = (args) => {
	const { a, b, c, d } = args;
};
const handleClose = () => {
	emits('close');
};

// 9、组件挂载
onMounted(() => {
	// init()
});

// 10、导出
defineExpose({
	handleOpen,
});
</script>

<style scoped lang="scss">
/* 一般情况css无需注释 */
.gc-dialog {
	/* 统一不使用 & 符嵌套，便于搜索查找 */
	.gc-dialog-header {
	}

	.gc-dialog-body {
	}

	.gc-dialog-footer {
	}
}
/* 避免嵌套过深，控制在3级以内 */
.gc-dialog-header {
	.gc-dialog-heade-left {
		.icon {
		}
		.title {
		}
	}
	.gc-dialog-heade-right {
	}
}

:deep(.el-button) {
}
</style>
