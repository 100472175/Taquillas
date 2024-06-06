<script lang="ts">
	import type { PageData } from './$types';
	export let data: PageData;

	const building = data.edificio;
	const pisos = data.pisos.reverse();

	// Para hacerlo responsive, así se sacan las dimensiones de la ventana
	$: outerWidth = 0;
	$: innerWidth = 0;
	$: outerHeight = 0;
	$: innerHeight = 0;
</script>

<svelte:window bind:innerWidth bind:outerWidth bind:innerHeight bind:outerHeight />

<h1
	class="text-7xl sm:text-8xl md:text-9xl lg:text-7xl xl:text-7xl 2xl:text-6xl text-center font-montserrat mt-4 mb-8 text-[#3BC4A0]"
>
	Edificio {building}
</h1>

<div class="flex flex-col items-center">
	{#each pisos as i}
		<a href="{building}/{i}" class="flex justify-center group relative">
			<img
				src={`../edificios/${data.edificio}/${i}.jpeg`}
				class="object-cover w-auto group-hover:opacity-60 transition duration-500 ease-in-out"
				alt={`Edificio ${data.edificio}. ${i}`}
			/>
			<h1
				class="hidden absolute left-1/2 top-1/2 text-5xl text-[#3BC4A0] px-6 py-2 rounded group-hover:block"
				style="transform: translate(-50%, -50%); background-color: rgba(0, 0, 0, 0.7)"
			>
				Piso {i}
			</h1>
		</a>
	{/each}
</div>

<hline></hline>
