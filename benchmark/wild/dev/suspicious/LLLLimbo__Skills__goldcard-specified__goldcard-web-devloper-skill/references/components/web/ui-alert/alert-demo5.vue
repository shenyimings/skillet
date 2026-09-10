<template>
	<div class="mb-4">
		<UiAlert
			type="success"
			:closable="false"
			description="Success Alert Description"
		/>
	</div>
	<div class="mb-4">
		<UiAlert :closable="false" description="Info Alert Description" />
	</div>
	<div class="mb-4">
		<UiAlert
			type="error"
			:closable="false"
			description="Error Alert Description"
		/>
	</div>
	<div class="mb-4">
		<UiAlert
			type="warning"
			:closable="false"
			description="Warning Alert Description"
		/>
	</div>
</template>
