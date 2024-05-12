// Auth client - only creates the client

import { SvelteKitAuth } from "@auth/sveltekit";
import Google from "@auth/sveltekit/providers/google";
import { AUTH_SECRET, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET } from "$env/static/private";


export const { handle } = SvelteKitAuth({
    trustHost: true,
    secret: AUTH_SECRET,
    providers: [
        Google({
            clientId: GOOGLE_CLIENT_ID,
            clientSecret: GOOGLE_CLIENT_SECRET
        })
        // Add more providers here, but for this app we only need Google
    ]
})