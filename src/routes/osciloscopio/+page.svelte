<script lang="ts">
	import { Gallery, Thumbnails, Carousel, Popover, Button  } from 'flowbite-svelte';
	import { QuestionCircleSolid } from 'flowbite-svelte-icons';
	import { goto } from '$app/navigation';
	import type { PageData } from './$types';
	export let data: PageData;

	let disponibilidad_osciloscopio: any[] = [];
	data.osciloscopio.then((value) => {
		disponibilidad_osciloscopio = Object.entries(value);
	});
</script>

<h1
	class="text-3xl sm:text-4xl lg:text-5xl xl:text-7xl text-center font-montserrat mt-4 mb-8 text-dele-color dark:text-dark-primary recompensa:text-recompensa-primary"
>
	Selección de Puesto
</h1>

<div class="w-screen grid grid-cols-1 place-items-center mb-4">
	<Button id="pop_edificio" class="dark:text-dark-primary dark:hover:text-dark-accent recompensa:text-recompensa-primary hover:recompensa:text-recompensa-accent text-dele-color hover:text-dele-accent">
		<QuestionCircleSolid class="md:h-8 md:w-8 h-10 w-10"/>
	</Button>
</div>

<Popover class="text-black dark:text-white dark:bg-dark-secondary recompensa:text-white recompensa:bg-recompensa-secondary md:w-1/3 sm:w-1/2 w-10/12 sm:text-md text-sm" title="Tutorial Puestos de Electrónica - Selección de Puesto" triggeredBy="#pop_edificio">
	Primero, selecciona el puesto sobre el que quieres realizar la reserva. 
	En delegación, contamos con tres puestos de electrónica, los tres igualmente equipados.
</Popover >

<div class="grid grid-cols-1 place-items-center w-screen mt-6 mb-6">
	{#if disponibilidad_osciloscopio.length > 0} 
		{#each disponibilidad_osciloscopio as puesto}
			{#if puesto[1]}
				<Button class="text-white sm:text-3xl text-2xl px-8 py-3 bg-dele-color mb-2 rounded-2xl hover:bg-dele-accent dark:hover:bg-dark-accent hover:recompensa:bg-recompensa-accent dark:text-white recompensa:text-white dark:border-black recompensa:border-black dark:bg-dark-primary recompensa:bg-recompensa-primary" href={"/osciloscopio/" + puesto[0]}>{"Puesto " + puesto[0]}</Button>
			{:else}
				<p class="text-white sm:text-3xl text-2xl px-8 py-3 bg-dele-color mb-2 rounded-2xl hover:bg-dele-accent dark:hover:bg-dark-accent hover:recompensa:bg-recompensa-accent dark:text-white recompensa:text-white dark:border-black recompensa:border-black dark:bg-dark-primary recompensa:bg-recompensa-primary">{"Puesto " + puesto[0]} no disponible</p>
			{/if}
		{/each}
	{/if}
</div>