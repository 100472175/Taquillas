<script context="module">
	export function goto_page(page) {
		goto(page);
		let menu = false;
	}
</script>

<script lang="ts">
	import { signIn, signOut } from '@auth/sveltekit/client';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import '../app.css';

	// $page.data.session -> {user, image, etc...}

	let name = '';
	let image = null;

	if ($page.data.session) {
		name = $page.data.session?.user?.name;
		image = $page.data.session?.user?.image;
	}

	let menu;
	let menu_display = false;
	let changing = false;

	function toggle_menu() {
		if (!changing) {
			changing = true;
			menu_display = !menu_display;
			if (menu_display) {
				menu.style.display = 'block';
				menu.classList.add('animate-appear');
			} else {
				menu.classList.add('animate-disappear');
				setTimeout(() => {
					menu.style.display = 'none';
				}, 750);
			}
			setTimeout(() => {
				changing = false;
				menu.classList.remove('animate-appear', 'animate-disappear');
			}, 800);
		}
	}
</script>

<link
	href="https://fonts.googleapis.com/css2?family=Montserrat:wght@100;200;300;400;500;600;700;800;900&family=Roboto&display=swap"
	rel="stylesheet"
/>

<header class="bg-[#3BC4A0] grid grid-cols-5">
	<button class="bg-white w-1/3 h-8 mt-2 ml-2 rounded-2xl" on:click={toggle_menu}>Menú</button>
	<img class="" src="" alt="logo" />
	<button
		class="font-bold-italic text-white text-center py-2 text-2xl hover:underline"
		on:click={() => {
			goto_page('./');
		}}>Delegación EPS</button
	>
	{#if $page.data.session}
		<p class="text-white italic mt-3 text-center">{name}</p>
		<button on:click={() => signOut()} class="bg-red-500 text-white rounded-2xl h-8 mt-2 ml-8 w-4/5"
			>Sign-out</button
		>
	{:else}
		<div></div>
		<button class="bg-white rounded-2xl h-8 mt-2 ml-8 w-4/5" on:click={() => signIn('google')}
			>Log-in</button
		>
	{/if}
</header>

<div bind:this={menu} class="bg-[#FFFFFF] w-1/4 h-screen border-2 absolute hidden">
	<button
		class="bg-[#3BC4A0] text-center w-full h-20"
		on:click={() => {
			goto_page('./');
		}}><h1 class="text-2xl text-white hover:underline">Delegación EPS - Home</h1></button
	>
	<button
		class="bg-[#3BC4A0] text-center w-full mt-1 h-20"
		on:click={() => {
			goto_page('./taquillas');
		}}><h1 class="text-2xl text-white hover:underline">Taquillas</h1></button
	>
	<button
		class="bg-[#3BC4A0] text-center w-full mt-1 h-20"
		on:click={() => {
			goto_page('./');
		}}><h1 class="text-2xl text-white hover:underline">Osciloscopios</h1></button
	>
	<button
		class="bg-[#3BC4A0] text-center w-full mt-1 h-20"
		on:click={() => {
			goto_page('./encuestas');
		}}><h1 class="text-2xl text-white hover:underline">Encuestas</h1></button
	>
</div>
<slot />
