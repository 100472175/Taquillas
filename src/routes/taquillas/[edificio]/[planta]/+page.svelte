<script lang="ts">
	import type { PageData } from './$types';
	import { Button, Dropdown, Radio, Modal, Label, Input } from 'flowbite-svelte';
	import { ChevronDownOutline } from 'flowbite-svelte-icons';

	export let data: PageData;

	const floor_size = Object.keys(data.size[data.edificio][data.planta]);

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
	let openDropdown = false;
	let formModal = false;
	let selectedTaquilla = '';
	let NIA = data.session?.user?.email?.split('@')[0].split('.')[0] || '100XXXXXX';

	function closeModalAssignBlock(block_selected: string) {
		openDropdown = false;
		block = parseInt(block_selected);
	}

	function openModal(taquilla: string) {
		selectedTaquilla = taquilla;
		formModal = true;
	}
</script>

<h1
	class="text-6xl sm:text-7xl md:text-8xl lg:text-6xl xl:text-6xl 2xl:text-6xl text-center font-montserrat mt-4 mb-8 text-[#3BC4A0]"
>
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
		Bloque {block}: <ChevronDownOutline class="w-6 h-6 ms-2 text-green-500 dark: text-blue-500" />
	</Button>
	<Dropdown bind:open={openDropdown}>
		<div slot="header" class="px-4 py-2">
			<span class="block text-sm text-gray-900 dark:text-white">Selecciona un bloque</span>
		</div>
		{#each floor_size as bloque}
			<!-- svelte-ignore a11y-click-events-have-key-events -->
			<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
			<li
				class="rounded p-2 hover:bg-gray-100 dark:hover:bg-gray-600"
				on:click={() => closeModalAssignBlock(bloque)}
			>
				<Radio name="block" bind:group={block} value={bloque}>Bloque {bloque}</Radio>
			</li>
		{/each}
	</Dropdown>
</div>

{#if block != 0}
	<h3 class="text-center m-4">
		Bloque {block}, que tiene un tamaño de {data.size[data.edificio][data.planta][block]}
	</h3>
	<div class="w-10/12 overflow-auto m-auto">
		<table style="border: 1px solid black; border-collapse: 10px;" class="m-auto mb-10">
			{#each Array(data.size[data.edificio][data.planta][block][1]) as _, i}
				<tr>
					{#each Array(data.size[data.edificio][data.planta][block][0]) as _, i}
						<td
							style="border: 1px solid black; border-collapse: 10px"
							class=" p-7 bg-red-500"
							on:click={() => openModal(plants[i])}
						>
							{plants[i]}
						</td>
					{/each}
				</tr>
			{/each}
		</table>
	</div>
{/if}

<Modal bind:open={formModal} size="xs" autoclose={false} class="w-full">
	<form class="flex flex-col space-y-6" action="?/registerTaquilla" method="post">
		<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white">Reservar Taquilla</h3>
		<p>
			Vas a realizar la reserva de una taquilla. El precio de las taquilla es de:
			{#if selectedTaquilla.includes('G')}<span class="font-bold"> 6€ </span>
			{:else}<span class="font-bold"> 4€ </span>
			{/if} el año completo y la mitad por el segundo cuatrimestre.
		</p>
		<Label class="space-y-2">
			<span>NIA:</span>
			<Input
				type="text"
				id="nia"
				name="nia"
				placeholder="100xxxxxx@alumnos.uc3m.es"
				value={NIA}
				required
			/>
		</Label>
		<Label class="space-y-2">
			<span>Taquilla</span>
			<Input type="text" id="taquilla" name="taquilla" value={selectedTaquilla} required />
		</Label>

		<Button type="submit" class="w-full1 bg-green-500 hover:bg-blue-400">Reservar Taquilla</Button>
	</form>
</Modal>
