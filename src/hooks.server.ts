import { SvelteKitAuth } from '@auth/sveltekit';
import Google from '@auth/sveltekit/providers/google';
import 'dotenv/config';

const { handle: authHandle } = SvelteKitAuth({
	providers: [
		Google({
			clientId: process.env.GOOGLE_CLIENT_ID,
			clientSecret: process.env.GOOGLE_CLIENT_SECRET
		})
	],
	useSecureCookies: true,
	trustHost: true,
	debug: false,
	secret: process.env.AUTH_SECRET,
});

export const handle = async ({ event, resolve }: any) => {
	// Ensure URL is HTTPS
	if (event.url.protocol !== 'https:') {
		event.url.protocol = 'https:';
	}

	// Access internal request symbol for URL list manipulation
	const requestSymbols = Object.getOwnPropertySymbols(event.request);
	const internalRequest =
		event.request[requestSymbols.find((symbol) => symbol.description === 'internal')];

	if (internalRequest) {
		internalRequest.url.protocol = 'https:';
		internalRequest.urlList.forEach((url: URL) => {
			url.protocol = 'https:';
		});
	}

	// Use the handle function provided by SvelteKitAuth
	return await authHandle({ event, resolve });
};
