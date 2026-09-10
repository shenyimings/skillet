<template>
	<div class="demo-container">
		<h4 style="margin-top: 0">不同标记类型示例</h4>
		<div class="flag-demo">
			<ui-flag type="default" text="默认标记" />
			<ui-flag type="primary" text="主要标记" />
			<ui-flag type="error" text="错误标记" />
			<ui-flag type="success" text="成功标记" />
			<ui-flag type="warning" text="警告标记" />
		</div>

		<h4>不同边框宽度</h4>
		<div class="flag-demo">
			<ui-flag type="primary" text="细边框" :weight="1" />
			<ui-flag type="primary" text="中等边框" :weight="2" />
			<ui-flag type="primary" text="粗边框" :weight="3" />
		</div>

		<h4>不同间距</h4>
		<div class="flag-demo">
			<ui-flag type="success" text="小间距" :gap="4" />
			<ui-flag type="success" text="默认间距" :gap="8" />
			<ui-flag type="success" text="大间距" :gap="16" />
		</div>

		<h4>自定义插槽内容</h4>
		<div class="flag-demo">
			<ui-flag type="primary">
				<span style="color: #fff; font-weight: bold">自定义内容</span>
			</ui-flag>

			<ui-flag type="success">
				<div style="display: flex; align-items: center; gap: 4px">
					<svg
						width="16"
						height="16"
						viewBox="0 0 24 24"
						fill="currentColor"
					>
						<path
							d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"
						/>
					</svg>
					<span>带图标的标记</span>
				</div>
			</ui-flag>

			<ui-flag type="warning">
				<div style="display: flex; align-items: center; gap: 6px">
					<span style="font-size: 14px">🔥</span>
					<span>热门</span>
				</div>
			</ui-flag>

			<ui-flag type="error">
				<div style="display: flex; align-items: center; gap: 4px">
					<span style="font-size: 12px">❗</span>
					<span>紧急</span>
				</div>
			</ui-flag>
		</div>

		<h4>复杂自定义内容</h4>
		<div class="flag-demo">
			<ui-flag type="default">
				<div style="text-align: center; padding: 2px 8px">
					<div style="font-size: 12px; font-weight: bold">NEW</div>
					<div style="font-size: 10px; opacity: 0.8">最新</div>
				</div>
			</ui-flag>

			<ui-flag type="primary">
				<div
					style="
						display: flex;
						align-items: center;
						gap: 6px;
						padding: 0 8px;
					"
				>
					<div
						style="
							width: 8px;
							height: 8px;
							border-radius: 50%;
							background: #fff;
						"
					></div>
					<span>在线</span>
				</div>
			</ui-flag>
		</div>
	</div>
</template>

<script setup>
import { UiFlag } from '@e-cloud/eslink-plus';
</script>

<style scoped>
.demo-container {
	height: auto;
}

.flag-demo {
	display: flex;
	gap: 25px;
	flex-wrap: wrap;
	align-items: center;
}
</style>
