<template>
	<div class="mb-4">
		<UiAlert
			title="透明背景警告"
			type="info"
			description="这是一个透明背景的警告提示"
			:transparent="true"
		/>
	</div>
	<div class="mb-4">
		<UiAlert
			title="透明成功提示"
			type="success"
			description="操作成功完成"
			:transparent="true"
			:show-icon="true"
			:closable="true"
		/>
	</div>
	<div class="mb-4">
		<UiAlert
			title="透明错误警告"
			type="error"
			description="发生了一个错误，请检查"
			:transparent="true"
			:show-icon="true"
		/>
	</div>
</template>