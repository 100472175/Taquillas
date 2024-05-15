import type { LayoutServerLoad } from "./$types";
// load serverside data
export const load: LayoutServerLoad = async (event) => {
    return {
        session: await event.locals.auth()
    }

}
