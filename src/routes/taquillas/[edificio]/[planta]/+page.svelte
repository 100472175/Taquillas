<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;

	const floor_size = Object.keys(data.size[data.edificio][data.planta]).length;

	const plants = [
		'1.0.E.G003',
		'cailiflower',
		'cabbage',
		'kale',
		'tomato',
		'patata',
		'cafe',
		'trastos',
		'brocoli'
	];
</script>

<h1 class="text-3xl text-center font-montserrat">
	Te encuentras en el edificio {data.edificio}, en la planta {data.planta}.
</h1>

<p>Aquí tendremos el selector de bloque dentro de cada planta.</p>

<p>
	Info <a
		class="text-blue-500 underline"
		href="https://www.w3schools.com/html/html_images_imagemap.asp"
	>
		aqui
	</a>
</p>
<br />

{#if floor_size <= 0}
	<p>No hay taquillas en esta planta.</p>
{:else}
	<p>Hay {floor_size} taquillas en esta planta.</p>
	{#each Object.keys(data.size[data.edificio][data.planta]) as bloque}
		<h3>Bloque {bloque}, que tiene un tamaño de {data.size[data.edificio][data.planta][bloque]}</h3>
		<table style="border: 1px solid black; border-collapse: 10px;">
			{#each Array(data.size[data.edificio][data.planta][bloque][1]) as _, i}
				<tr>
					{#each Array(data.size[data.edificio][data.planta][bloque][0]) as _, i}
						<td style="border: 1px solid black; border-collapse: 10px" class=" p-7 bg-red-500">
							{plants[i]}
						</td>
					{/each}
				</tr>
			{/each}
		</table>
	{/each}
{/if}
