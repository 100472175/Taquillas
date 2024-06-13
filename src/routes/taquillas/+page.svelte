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
</script>

<div class="">
	<div class="max-w-4xl space-y-4">
		<Carousel {images} let:Indicators let:Controls>
			<a slot="slide" href={images[index]?.href} let:Slide let:index>
				<Slide image={images[index]} />
			</a>
			<Controls class="items-center dark:text-red-400 text-green-400 pt-4" />
			<Indicators />
		</Carousel>
		<Thumbnails {images} {forward} bind:index />
	</div>
</div>
