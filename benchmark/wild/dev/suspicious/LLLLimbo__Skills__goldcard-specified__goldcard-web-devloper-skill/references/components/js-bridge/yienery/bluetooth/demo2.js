import * as EMeshing from '../../uni_modules/e-meshing';

EMeshing.startConfig(
	'deviceSnNo',
	'ssid',
	'password',
	(succ) => {
		console.log('start config successed, msg is', succ);
	},
	(err) => {
		console.log('start config failed, msg is', err);
	}
);
