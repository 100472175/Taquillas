<script lang="ts">
    import {signIn, signOut} from '@auth/sveltekit/client';
	import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { page } from '$app/stores';

	import '../app.css';
	
	function goto_home() {
		goto("/");
	}

    // $page.data.session -> {user, image, etc...}
    console.log($page.data.session);

    if ($page.data.session) {
        let name = $page.data.session?.user?.name;
        let image = $page.data.session?.user?.image;
    }
   
</script>

<header class="bg-[#3BC4A0] grid grid-cols-5">
	<button>Menú</button>
	<img class="" src="" alt="logo">
	<button class="font-bold-italic text-white text-center py-2 text-2xl" on:click={goto_home}>Delegación EPS</button>
	<div></div>
	{#if $page.data.session}
		<button on:click={() => signOut()} class="bg-red-500 text-white rounded-4xl h-8 mt-2 mr-2">Sign-out</button>
	{:else}
		<button class="bg-white rounded-4xl h-8 mt-2 mr-2" on:click={() => signIn("google")}>Log-in</button>
    {/if}
</header>

<slot />
