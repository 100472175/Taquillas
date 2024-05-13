<script lang="ts">
    import {signIn, signOut} from '@auth/sveltekit/client';
	import { goto } from '$app/navigation';
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
	import '../app.css';

	// $page.data.session -> {user, image, etc...}
    console.log($page.data.session);
	
	let name = "";
	let image = null;
	
    if ($page.data.session) {
        name = $page.data.session?.user?.name;
        image = $page.data.session?.user?.image;
    }

	function goto_home() {
		goto("/");
	}
   
</script>

<header class="bg-[#3BC4A0] grid grid-cols-5">
	<button>Menú</button>
	<img class="" src="" alt="logo">
	<button class="font-bold-italic text-white text-center py-2 text-2xl hover:underline" on:click={goto_home}>Delegación EPS</button>
	{#if $page.data.session}
		<p class="text-white italic mt-3 text-center">{name}</p>
		<button on:click={() => signOut()} class="bg-red-500 text-white rounded-4xl h-8 mt-2 mr-2">Sign-out</button>
	{:else}
		<div></div>
		<button class="bg-white rounded-4xl h-8 mt-2 mr-2" on:click={() => signIn("google")}>Log-in</button>
	{/if}
</header>

<slot />
