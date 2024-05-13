<script lang="ts">
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import {signIn, signOut} from '@auth/sveltekit/client';
    import { page } from '$app/stores';
    // $page.data.session -> {user, image, etc...}
    console.log($page.data.session);

    if ($page.data.session) {
        let name = $page.data.session?.user?.name;
        let image = $page.data.session?.user?.image;
    }
    

</script>

<div class="p-24">
    {#if $page.data.session}
        <button on:click={() => signOut()} class="btn-xl bg-pink-400 text-blue-700 rounded-2xl shadow-2xl">
            You are logged in. Click here to sign out.
        </button>
        <br />
        <p>{$page.data.session.user?.name} ha iniciado sesión, y tiene esta foto de perfil:</p>
        <img src="{$page.data.session.user?.image}" alt="{$page.data.session.user?.name} profile image" class="rounded-full w-24 h-24" />

    {:else}
        <button on:click={() => signIn("google")} class="btn-xl bg-black text-white rounded-2xl shadow-2xl px-2 py-1">
            Sign In
        </button>
    {/if}
</div>