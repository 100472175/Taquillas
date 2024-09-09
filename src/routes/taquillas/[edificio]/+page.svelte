<script lang="ts">
	import type { PageData } from './$types';
	import { Popover, Button  } from 'flowbite-svelte';
	import {QuestionCircleSolid} from 'flowbite-svelte-icons';
	export let data: PageData;

	const building  = data.edificio;
	const pisos = data.pisos.reverse();

	// Para hacerlo responsive, así se sacan las dimensiones de la ventana
	$: outerWidth = 0;
	$: innerWidth = 0;
	$: outerHeight = 0;
	$: innerHeight = 0;
</script>

<svelte:window bind:innerWidth bind:outerWidth bind:innerHeight bind:outerHeight />

<h1
	class="text-3xl sm:text-4xl lg:text-5xl xl:text-7xl text-center font-montserrat mt-4 mb-8 text-dele-color dark:text-dark-primary"
>
	Selección de Piso
</h1>

<div class="w-screen grid grid-cols-1 place-items-center mb-4">
	<Button id="pop_edificio" class="dark:text-dark-primary dark:hover:text-dark-accent text-dele-color hover:text-dele-accent">
		<QuestionCircleSolid class="md:h-8 md:w-8 h-10 w-10"/>
	</Button>
</div>

<Popover class="text-black dark:text-white dark:bg-dark-secondary md:w-1/3 sm:w-1/2 w-10/12 sm:text-md text-sm" title="Tutorial Taquillas - Selección de Piso" triggeredBy="#pop_edificio">
	Ahora, selecciona la piso donde se encuentra la taquilla que quieres reservar.
</Popover >

<div class="flex flex-col items-center mb-6">
	{#each pisos as i}
		<a href="{building}/{i}" class="flex justify-center group relative">
			<img
				src={`../edificios/${data.edificio}/${i}.webp`}
				class="object-cover w-auto group-hover:opacity-60 transition duration-500 ease-in-out"
				alt={`Edificio ${data.edificio}. ${i}`}
			/>
			<h1
				class="absolute left-1/2 top-1/2 md:text-3xl sm:text-lg text-sm text-dele-color px-6 py-2 rounded block dark:text-dark-primary"
				style="transform: translate(-50%, -50%); background-color: rgba(0, 0, 0, 0.8)"
			>
				Piso {i}
			</h1>
		</a>
	{/each}
</div>

<hline></hline>
