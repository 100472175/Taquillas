// Auth client - only creates the client

import { SvelteKitAuth } from '@auth/sveltekit';
import Google from '@auth/sveltekit/providers/google';
import 'dotenv/config';

export const { handle, signIn, signOut } = SvelteKitAuth({
	trustHost: true,
	secret: process.env.AUTH_SECRET,
	providers: [
		Google({
			clientId: process.env.GOOGLE_CLIENT_ID,
			clientSecret: process.env.GOOGLE_CLIENT_SECRET,
			
		})
		// Add more providers here, but for this app we only need Google
	],
	callbacks: {
		async signIn({ profile }) {
			let emailTest = String(profile?.email);
			if (emailTest.endsWith('uc3m.es')) {
				return true;
			}
			return false;
		  },
	  }
});
