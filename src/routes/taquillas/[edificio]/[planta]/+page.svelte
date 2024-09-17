<script lang="ts">
	import type { PageData } from './$types';
	import {
		Button,
		Dropdown,
		Radio,
		ButtonGroup,
		Toast,
		Popover,
		Indicator,
		Card
	} from 'flowbite-svelte';
	import {
		ChevronDownOutline,
		ArrowLeftOutline,
		ArrowRightOutline,
		CloseCircleSolid,
		CheckCircleSolid,
		QuestionCircleSolid
	} from 'flowbite-svelte-icons';
	import TablaTaquillas from '../../../../TablaTaquillas.svelte';
	import { Confetti } from 'svelte-confetti';

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

	function clearForm(time: number) {
		setTimeout(() => {
			form = null;
		}, time);
	}

	export let form;
</script>

<h1
	class="text-3xl sm:text-4xl lg:text-5xl xl:text-7xl text-center font-montserrat mt-4 mb-4 text-dele-color dark:text-dark-primary"
>
	Selección de Taquilla
</h1>

<div class="w-screen grid grid-cols-1 place-items-center mb-4">
	<Button
		id="pop_edificio"
		class="dark:text-dark-primary dark:hover:text-dark-accent text-dele-color hover:text-dele-accent"
	>
		<QuestionCircleSolid class="md:h-8 md:w-8 h-10 w-10" />
	</Button>
</div>

<Popover
	class="text-black dark:text-white dark:bg-dark-secondary md:w-1/3 sm:w-1/2 w-10/12 sm:text-md text-sm"
	title="Tutorial Taquillas - Selección de Taquilla"
	triggeredBy="#pop_edificio"
>
	Por último, tienes que buscar la taquilla seleccionando el bloque donde se encuentra la misma.
	Para cambiar entre bloques, puedes usar el menú desplegable o los botones inferiores. Además,
	tienes un mapa al final de la página para ayudarte a seleccionar el bloque.
	<br /><br />
	<b>Recuerda hacer login en una cuenta de la UC3M para reservar la taquilla.<b> </b></b></Popover
>

<div class="w-screen h-full grid grid-rows-1 place-items-center">
	<Button
		size="lg"
		class="w-1/10 bg-dele-color hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent"
	>
		Bloque {block}
		<ChevronDownOutline class="w-6 h-6 ms-2 text-black dark:text-red-500" />
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
	<div class="grid grid-cols-1 place-self-center mt-6">
		<div class="w-auto m-auto dark:text-white grid sm:grid-cols-4 grid-cols-2">
			<span class="flex items-center"
				><Indicator size="lg" color="green" class="me-1.5" />Libre</span
			>
			<span class="flex items-center"
				><Indicator size="lg" color="yellow" class="me-1.5" />Reservada</span
			>
			<span class="flex items-center"
				><Indicator size="lg" color="red" class="me-1.5" />Ocupada</span
			>
			<span class="flex items-center"
				><Indicator size="lg" color="dark" class="me-1.5" />No Disponible</span
			>
		</div>
	</div>
	<TablaTaquillas bind:ocupacion_bloques={ocupacionBloques} bind:block bind:data></TablaTaquillas>
	<div class="w-screen h-auto grid grid-rows-1 place-items-center mt-6">
		<ButtonGroup class="space-x-px">
			<Button
				pill
				class="dark:bg-dark-primary dark:hover:bg-dark-accent bg-[#3BC4A0] hover:bg-[#FF6D2E]"
				on:click={() => substractBlock()}
			>
				<ArrowLeftOutline />
			</Button>
			<Button
				pill
				class="dark:bg-dark-primary dark:hover:bg-dark-accent bg-[#3BC4A0] hover:bg-[#FF6D2E]"
				on:click={() => addBlock()}
			>
				<ArrowRightOutline />
			</Button>
		</ButtonGroup>
	</div>
	<div class="w-screen grid grid-rows-1 place-items-center px-4 mt-6 mb-6">
		<img src={urlMapa} alt="Mapa" class="max-w-[800px] md:w-7/12 w-10/12 dark:invert" />
	</div>
{:else}
	<p class="text-center p-6 dark:text-dark-primary">Loading...</p>
{/if}

{#if form}
	{#if form.message.includes('Error')}
		<div
			class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 border-dashed border-4 border-red-500 dark:border-red-500 p-4 mx-auto text-center"
		>
			<Card class="text-white bg-red-500 dark:text-white dark:bg-red-500">
				<p class="p-2">{form.message}</p>
			</Card>
		</div>
		<div class="text-white dark:text-dark-background">
			{clearForm(2000)}
		</div>
	{:else}
		<div
			class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 border-dashed border-4 border-green-500 dark:border-green-500 p-4 mx-auto text-center"
		>
			<Card class="text-white bg-green-500 dark:text-white dark:bg-green-500">
				<p class="p-2">{form.message}</p>
			</Card>
			<Confetti amount={500} x={[-0.5, 3.5]} delay={[0, 2000]} duration={2000} infinite />
		</div>
		<div class="text-white dark:text-dark-background">
			{handleReload()}
		</div>
	{/if}
{/if}
