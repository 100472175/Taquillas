import type { PageServerLoad } from './$types';

export const load = (async () => {
    const fetchAuthorizedEmails = async () => {
		const res = await fetch('http://localhost:18080/api/authorizedEmails');
		const data = await res.json();
		return data;
	};

    return {
        authorizedEmails: await fetchAuthorizedEmails(),
    };
}) satisfies PageServerLoad;