<script lang="ts">
	import type { PageData } from './$types';
	import { Button, Dropdown, Radio, ButtonGroup, Toast } from 'flowbite-svelte';
	import {
		ChevronDownOutline,
		ArrowLeftOutline,
		ArrowRightOutline,
		CloseCircleSolid,
		CheckCircleSolid
	} from 'flowbite-svelte-icons';
	import TablaTaquillas from '../../../../TablaTaquillas.svelte';

	export let data: PageData;

	const floor_size = Object.keys(data.size[data.edificio][data.planta]);

	let block = 1;
	let openDropdown = false;

	let ocupacionBloques: any[];
	let drawBlocks = false;

	let urlMapa = `/mapas/${data.edificio}.${data.planta}.webp`;

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

	function handleReload() {
		setTimeout(() => {
			location.reload();
		}, 2000);
	}

	export let form;
</script>

<h1
	class="text-3xl sm:text-4xl lg:text-5xl xl:text-7xl text-center font-montserrat mt-4 mb-8 text-[#3BC4A0] dark:text-dark-primary"
>
	Edificio {data.edificio} - Planta {data.planta}
</h1>

<div class="w-screen h-full grid grid-rows-2 place-items-center">
	<h1
		class="text-2xl sm:text-3xl lg:text-4xl xl:text-6xl text-[#3BC4A0] dark:text-dark-primary text-center"
	>
		Selecciona el bloque:
	</h1>
	<Button size="lg" class="mt-4 w-1/10 bg-[#3BC4A0] hover:bg-[#FF6D2E] dark:bg-dark-primary dark:hover:bg-dark-accent">
		Bloque {block} <ChevronDownOutline class="w-6 h-6 ms-2 text-black dark:text-red-500" />
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

	<div class="w-screen h-auto grid grid-rows-3 place-items-center -mt-8">
		<ButtonGroup class="space-x-px">
			<Button pill class="dark:bg-dark-primary dark:hover:bg-dark-accent bg-[#3BC4A0] hover:bg-[#FF6D2E]" on:click={() => substractBlock()}>
				<ArrowLeftOutline />
			</Button>
			<Button pill class="dark:bg-dark-primary dark:hover:bg-dark-accent bg-[#3BC4A0] hover:bg-[#FF6D2E]" on:click={() => addBlock()}>
				<ArrowRightOutline />
			</Button>
		</ButtonGroup>
	</div>
	<div class="w-screen grid grid-rows-1 place-items-center mt-4 px-4">
		<img src={urlMapa} alt="Mapa" class="max-w-[800px] md:w-7/12 w-10/12 dark:invert" />
	</div>
{:else}
	<p class="text-center p-6 dark:text-dark-primary">Loading...</p>
{/if}

{#if form}
	{#if form.message.includes('Error')}
		<Toast color="red" position="bottom-right">
			<svelte:fragment slot="icon">
				<CloseCircleSolid class="w-5 h-5" />
				<span class="sr-only">Error icon</span>
			</svelte:fragment>
			{form.message}
		</Toast>
	{:else}
		<Toast color="green" position="bottom-right">
			<svelte:fragment slot="icon">
				<CheckCircleSolid class="w-5 h-5" />
				<span class="sr-only">Error icon</span>
			</svelte:fragment>
			{form.message}
		</Toast>
		{handleReload()}
	{/if}
{/if}
