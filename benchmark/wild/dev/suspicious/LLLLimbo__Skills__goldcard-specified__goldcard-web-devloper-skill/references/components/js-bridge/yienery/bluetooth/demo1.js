import * as EMeshing from '../../uni_modules/e-meshing';

EMeshing.initSDK(
	'appKeyValueString',
	(succ) => {
		console.log('init successed, msg is', succ);
	},
	(err) => {
		console.log('init failed, msg is', err);
	}
);
