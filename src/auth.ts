// Auth client - only creates the client

import { SvelteKitAuth } from '@auth/sveltekit';
import Google from '@auth/sveltekit/providers/google';
import { AUTH_SECRET, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET } from '$env/static/private';
import 'dotenv/config';

export const { handle, signIn, signOut } = SvelteKitAuth({
	trustHost: true,
	secret: process.env.AUTH_SECRET,
	providers: [
		Google({
			clientId: process.env.GOOGLE_CLIENT_ID,
			clientSecret: process.env.GOOGLE_CLIENT_SECRET
		})
		// Add more providers here, but for this app we only need Google
	]
});
