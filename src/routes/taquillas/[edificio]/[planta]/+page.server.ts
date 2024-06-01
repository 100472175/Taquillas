import type { PageServerLoad } from './$types';
import size from '$lib/size';

export const load: PageServerLoad = async () => {
	return {
		serverMessage: 'hello from server load function',
        size: size,
	};
};