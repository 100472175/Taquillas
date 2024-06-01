<script lang="ts">
	import type { PageData } from './$types';
	export let data: PageData;

	import { Hr } from 'flowbite-svelte';
	const building = data.edificio;
	const pisos = [3, 2];
</script>

<h1
	class="text-7xl sm:text-8xl md:text-9xl lg:text-7xl xl:text-8xl 2xl:text-9xl text-center font-montserrat"
>
	Te encuentras en el edificio {data.edificio}.
</h1>

<div class="flex flex-col items-center">
	{#each pisos as i}
		<a href="{data.edificio}/{i}" class="flex justify-center w-full">
			<img
				src={`../edificios/${data.edificio}/${i}.jpg`}
				class="w-1/2 object-cover"
				alt={`Edificio ${data.edificio}. ${i}`}
			/>
		</a>
		{#if i !== pisos[pisos.length - 1]}
			<Hr classHr="w-48 h-1 my-4 rounded md:my-1" />
		{/if}
	{/each}
</div>
