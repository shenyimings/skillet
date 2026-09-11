import * as EMeshing from '../../uni_modules/e-meshing';

EMeshing.getLog(
	(succ) => {
		console.log('get log successed, msg is', succ);
	},
	(err) => {
		console.log('get log failed, msg is', err);
	}
);
