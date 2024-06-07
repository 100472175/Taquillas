<script lang="ts">
	import type { PageData } from './$types';
	import { Button, Dropdown, Radio, ButtonGroup } from 'flowbite-svelte';
	import { ChevronDownOutline, ArrowLeftOutline, ArrowRightOutline } from 'flowbite-svelte-icons';
	import TablaTaquillas from '../../../../TablaTaquillas.svelte';

	export let data: PageData;

	const floor_size = Object.keys(data.size[data.edificio][data.planta]);

	let block = 1;
	let openDropdown = false;

	let ocupacionBloques: any[];
	let drawBlocks = false;

	data.bloques.then((value) => {
		ocupacionBloques = value;
		drawBlocks = true;
	});

	function closeModalAssignBlock(block_selected: string) {
		openDropdown = false;
		block = parseInt(block_selected);
	}

	function substractBlock() {
		block -= 1;
		if (block < 1) {
			block = floor_size.length;
		}
	}

	function addBlock() {
		block += 1;
		if (block > floor_size.length) {
			block = 1;
		}
	}
</script>

<h1
	class="text-6xl sm:text-7xl md:text-8xl lg:text-6xl xl:text-6xl 2xl:text-6xl text-center font-montserrat mt-4 mb-8 text-[#3BC4A0]"
>
	Edificio {data.edificio} - Planta {data.planta}
</h1>

<div class="w-screen h-full grid grid-rows-2 place-items-center">
	<h1 class="text-3xl text-[#3BC4A0] text-center">Selecciona el bloque:</h1>
	<Button color="green" size="lg" class="mt-4 w-1/10">
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

{#if drawBlocks}
	<TablaTaquillas bind:ocupacion_bloques={ocupacionBloques} bind:block bind:data></TablaTaquillas>

	<div class="w-screen h-full grid grid-rows-2 place-items-center">
		<ButtonGroup class="space-x-px">
			<Button pill color="green" on:click={() => substractBlock()}>
				<ArrowLeftOutline />
				Previo
			</Button>
			<Button pill color="green" on:click={() => addBlock()}>
				Siguiente
				<ArrowRightOutline />
			</Button>
		</ButtonGroup>
	</div>
{:else}
	<p class="text-center p-6">Loading...</p>
{/if}
