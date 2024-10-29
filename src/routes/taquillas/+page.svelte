<script lang="ts">
  import { goto } from '$app/navigation';
	import { _handleResult } from './+page.ts';
	import { Gallery, Thumbnails, Carousel, Popover, Button  } from 'flowbite-svelte';
	import {QuestionCircleSolid} from 'flowbite-svelte-icons';
	let images = [
		{
			alt: 'Edificio 1. Agustín de Betancourt',
			src: 'edificios/1-betancourt.webp',
			href: '/taquillas/1'
		},
		{ 
			alt: 'Edificio 2. Sabatini', 
			src: 'edificios/2-sabatini.webp', 
			href: '/taquillas/2' },
		{
			alt: 'Edificio 4. Torres Quevedo',
			src: 'edificios/4-Torres_Quevedo.webp',
			href: '/taquillas/4'
		},
		{ 
			alt: 'Edificio 7. Juan Benet', 
			src: 'edificios/7-Juan_Benet.webp',
			href: '/taquillas/7' }
	];
	let index = 0;
	let forward = true;
	const titulos = {
		0: 'Edificio 1. Agustín de Betancourt',
		1: 'Edificio 2. Sabatini',
		2: 'Edificio 4. Torres Quevedo',
		3: 'Edificio 7. Juan Benet'
	};
</script>

<h1
	class="text-3xl sm:text-4xl lg:text-5xl xl:text-7xl text-center font-montserrat mt-4 mb-8 text-dele-color dark:text-dark-primary recompensa:text-recompensa-primary"
>
	Selección de Edificio
</h1>

<div class="w-screen grid grid-cols-1 place-items-center mb-4">
	<Button id="pop_edificio" class="dark:text-dark-primary dark:hover:text-dark-accent recompensa:text-recompensa-primary hover:recompensa:text-recompensa-accent text-dele-color hover:text-dele-accent">
		<QuestionCircleSolid class="md:h-8 md:w-8 h-10 w-10"/>
	</Button>
</div>

<Popover class="text-black dark:text-white dark:bg-dark-secondary recompensa:text-white recompensa:bg-recompensa-secondary md:w-1/3 sm:w-1/2 w-10/12 sm:text-md text-sm" title="Tutorial Taquillas - Selección de Edificio" triggeredBy="#pop_edificio">
	Primero, selecciona el edificio usando la galeria haciendo click en la imagen con el edificio donde 
	quieres reservar la taquilla. Usa las flechas de la galería o las imágenes inferiores para rotar entre los edificios.
</Popover >

<div class="grid grid-cols-1 place-items-center w-screen mt-6 mb-6">
	<div class="max-w-4xl space-y-4">
		<Carousel {images} {forward} let:Indicators let:Controls bind:index>
			<a class="group" slot="slide" on:click={goto(images[index]?.href)} let:Slide let:index>
				<Slide image={images[index]} on:click={goto(images[index]?.href)}/>
				<h1
					class="absolute left-1/2 top-1/2 md:text-2xl sm:text-lg text-sm text-dele-color px-6 py-2 rounded block dark:text-dark-primary recompensa:text-recompensa-primary"
					style="transform: translate(-50%, -50%); background-color: rgba(0, 0, 0, 0.8)"
					on:click={goto(images[index]?.href)}
				>
					{titulos[index]}
				</h1>
			</a>
			<Controls class="items-center dark:text-red-400 text-green-400 recompensa:text-blue-400 pt-4"/>
			<Indicators />
		</Carousel>
		<Thumbnails {images} {forward} bind:index />
	</div>
</div>
