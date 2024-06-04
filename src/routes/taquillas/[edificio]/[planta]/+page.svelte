<script lang="ts">
	import type { PageData } from './$types';
	import { Button, Dropdown, DropdownItem, DropdownDivider, DropdownHeader, Radio } from 'flowbite-svelte';
	import { ChevronDownOutline } from 'flowbite-svelte-icons';
	
	export let data: PageData;

	const floor_size = Object.keys(data.size[data.edificio][data.planta]).length;

	const plants = [
		'1.0.E.G003',
		'cailiflower',
		'cabbage',
		'kale',
		'tomato',
		'patata',
		'cafe',
		'trastos',
		'brocoli'
	];
	
	let block = 1;
</script>

<h1 class="text-6xl sm:text-7xl md:text-8xl lg:text-6xl xl:text-6xl 2xl:text-6xl text-center font-montserrat mt-4 mb-8 text-[#3BC4A0]">
	Edificio {data.edificio} - Planta {data.planta}
</h1>

<p>Aquí tendremos el selector de bloque dentro de cada planta.</p>

<p>
	Info <a
		class="text-blue-500 underline"
		href="https://www.w3schools.com/html/html_images_imagemap.asp"
	>
		aqui
	</a>
</p>
<br />

<div class="w-screen h-full grid grid-rows-2 place-items-center">
	<h1 class="text-3xl text-[#3BC4A0] text-center">Ocupación por bloque</h1>
	<Button color="green" size="lg" class="mt-4 w-1/12">
		Bloque: <ChevronDownOutline class="w-6 h-6 ms-2 text-green-500 dark: text-blue-500"/>
	</Button>
	<Dropdown>
		<div slot="header" class="px-4 py-2">
			<span class="block text-sm text-gray-900 dark:text-white">Selecciona un bloque</span>
		</div>
		{#each Object.keys(data.size[data.edificio][data.planta]) as bloque}
			<li class="rounded p-2 hover:bg-gray-100 dark:hover:bg-gray-600">
				<Radio name="block" bind:group={block} value={bloque}>Bloque {bloque}</Radio>
			</li>
		{/each}
	</Dropdown>
</div>

{#if block != 0}
	<h3 class="text-center m-4">Bloque {block}, que tiene un tamaño de {data.size[data.edificio][data.planta][block]}</h3>
	<table style="border: 1px solid black; border-collapse: 10px;" class="m-auto mb-10">
		{#each Array(data.size[data.edificio][data.planta][block][1]) as _, i}
			<tr>
				{#each Array(data.size[data.edificio][data.planta][block][0]) as _, i}
					<td style="border: 1px solid black; border-collapse: 10px" class=" p-7 bg-red-500">
						{plants[i]}
					</td>
				{/each}
			</tr>
		{/each}
	</table>
{/if}
