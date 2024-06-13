<script lang="ts">
	import { _handleResult } from './+page.ts';
	import { Gallery, Thumbnails, Carousel } from 'flowbite-svelte';

	let images = [
		{
			alt: 'Edificio 1. Agustín de Betancourt',
			src: 'edificios/1-betancourt.webp',
			href: '/taquillas/1'
		},
		{ alt: 'Edificio 2. Sabatini', src: 'edificios/2-sabatini.jpg', href: '/taquillas/2' },
		{
			alt: 'Edificio 4. Torres Quevedo',
			src: 'edificios/4-Torres_Quevedo.jpg',
			href: '/taquillas/4'
		},
		{ alt: 'Edificio 7. Juan Benet', src: 'edificios/7-Juan_Benet.jpg', href: '/taquillas/7' }
	];
	let index = 0;
	let forward = true;
	let titulos = {0: "Edificio 1. Agustín de Betancourt", 1: "Edificio 2. Sabatini", 2: "Edificio 4. Torres Quevedo", 3: "Edificio 7. Juan Benet"};
</script>

<h1 class="text-7xl sm:text-8xl md:text-9xl lg:text-7xl xl:text-7xl 2xl:text-6xl text-center font-montserrat mt-4 mb-8 text-[#3BC4A0]">Selección de Edificio</h1>

<div class="grid grid-cols-1 place-items-center w-screen mt-10">
	<div class="max-w-4xl space-y-4">
		<Carousel {images} let:Indicators let:Controls>
			<a class="group" slot="slide" href={images[index]?.href} let:Slide let:index>
				<Slide image={images[index]} />
				<h1
					class="hidden absolute left-1/2 top-1/2 text-2xl text-[#3BC4A0] px-6 py-2 rounded group-hover:block"
					style="transform: translate(-50%, -50%); background-color: rgba(0, 0, 0, 0.7)"
				>
					{titulos[index]}
				</h1>
			</a>
			<Controls class="items-center dark:text-red-400 text-green-400 pt-4" />
			<Indicators />
		</Carousel>
		<Thumbnails {images} {forward} bind:index />
	</div>
</div>
