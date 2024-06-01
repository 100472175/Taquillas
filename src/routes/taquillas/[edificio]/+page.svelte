<script lang="ts">
	import type { PageData } from './$types';
	export let data: PageData;
	import { Button, Dropdown, DropdownItem, DropdownDivider, DropdownHeader } from 'flowbite-svelte';
	import { ChevronDownOutline } from 'flowbite-svelte-icons';

	import { Hr } from 'flowbite-svelte';
	const building = data.edificio;
	const pisos = [3, 2];

	// Para hacerlo responsive, así se sacan las dimensiones de la ventana
	$: outerWidth = 0;
	$: innerWidth = 0;
	$: outerHeight = 0;
	$: innerHeight = 0;
</script>

<svelte:window bind:innerWidth bind:outerWidth bind:innerHeight bind:outerHeight />

<h1
	class="text-7xl sm:text-8xl md:text-9xl lg:text-7xl xl:text-7xl 2xl:text-7xl text-center font-montserrat"
>
	Te encuentras en el edificio {data.edificio}.
</h1>

<div class="flex flex-col items-center">
	{#each pisos as i}
		<a href="{data.edificio}/{i}" class="flex justify-center">
			<img
				src={`../edificios/${data.edificio}/${i}.jpg`}
				class="object-cover hover:opacity-60 transition duration-300 ease-in-out"
				alt={`Edificio ${data.edificio}. ${i}`}
			/>
		</a>
		{#if i !== pisos[pisos.length - 1]}
			<Hr classHr="w-48 h-1 my-4 rounded md:my-1" />
		{/if}
	{/each}
</div>

<hline></hline>

<Button color="green" size="lg" class="mt-4">
	Planta:<ChevronDownOutline class="w-6 h-6 ms-2 text-green-500 dark: text-blue-500" /></Button
>
<Dropdown>
	<div slot="header" class="px-4 py-2">
		<span class="block text-sm text-gray-900 dark:text-white">Selecciona una planta</span>
	</div>
	<DropdownItem>Dashboard</DropdownItem>
	<DropdownItem>Settings</DropdownItem>
	<DropdownItem>Earnings</DropdownItem>
	<DropdownItem slot="footer">Sign out</DropdownItem>
</Dropdown>

<div class="flex flex-col items-center h-96">
	<svg viewBox="0 0 1000 1000" xmlns="http://www.w3.org/2000/svg">
		<a href="http://google.com">
			<circle stroke="#2EAEB8" stroke-width="16" fill-opacity="0.8" cx="100" cy="100" r="45" />
		</a>
		<rect
			stroke="#2EAEB8"
			stroke-width="16"
			fill="#70D5DB"
			fill-opacity="0.8"
			stroke-dasharray="0"
			stroke-dashoffset="0"
			stroke-linecap="round"
			stroke-linejoin="round"
			x="200"
			y="200"
			width="200"
			height="200"
		></rect>
		<polyline
			fill="none"
			points="550,412 600,700 50,400 80,750"
			stroke-opacity="0.8"
			stroke="#2EAEB8"
			stroke-width="16"
			stroke-linecap="round"
			stroke-linejoin="round"
			stroke-dasharray="0"
			stroke-dashoffset="0"
		/>
	</svg>
</div>
