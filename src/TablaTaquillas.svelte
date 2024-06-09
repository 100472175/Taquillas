<script lang="ts">
	import type { PageData } from './$types';
	import { Modal, Label, Input, Button } from 'flowbite-svelte';
	import { signIn, signOut } from '@auth/sveltekit/client';
	export let ocupacion_bloques, block, data: PageData;
	let formModalReservation = false;
	let formModalInformationError = false;
	let selectedTaquilla = '';
	let NIA = data.session?.user?.email?.split('@')[0] || '100XXXXXX';
	let claseTaquilla = '';

	function openModal(taquilla: string) {
		if (data.session?.user != null) {
			selectedTaquilla = taquilla;
			formModalReservation = true;
		} else {
			formModalInformationError = true;
		}
	}
</script>

<Modal bind:open={formModalReservation} size="xs" autoclose={false} class="w-full">
	<form class="flex flex-col space-y-6" action="?/registerTaquilla" method="post">
		<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white">Reservar Taquilla</h3>
		<p>
			Vas a realizar la reserva de una taquilla. El precio de las taquilla es de:
			{#if selectedTaquilla.includes('G')}<span class="font-bold"> 6€ </span>
			{:else}<span class="font-bold"> 4€ </span>
			{/if} el año completo y la mitad por el segundo cuatrimestre. Este importe se abona en delegación
			de estudiantes.
		</p>
		<Label class="space-y-2">
			<span>NIA:</span>
			<Input
				type="text"
				id="nia"
				name="nia"
				placeholder="100xxxxxx@alumnos.uc3m.es"
				value={NIA}
				required
				readonly
			/>
		</Label>
		<Label class="space-y-2">
			<span>Taquilla</span>
			<Input
				type="text"
				id="taquilla"
				name="taquilla"
				placeholder="x.y.z.ssss"
				value={selectedTaquilla}
				required
				readonly
			/>
		</Label>

		<Input type="hidden" id="correo" name="correo" value={data.session?.user?.email} />

		<Input type="hidden" id="nombre" name="nombre" value={data.session?.user?.name} />

		<Button type="submit" class="w-full1 bg-green-500 hover:bg-blue-400">Reservar Taquilla</Button>
	</form>
</Modal>

<Modal bind:open={formModalInformationError} size="xs" autoclose={false} class="w-full">
	<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white">Error</h3>
	<p>Debes iniciar sesión para reservar una taquilla</p>
	<Button
		type="button"
		class="w-full1 bg-green-500 hover:bg-blue-400"
		on:click={() => {
			signIn();
		}}
	>
		Iniciar Sesión
	</Button>
</Modal>

<div class="w-10/12 overflow-auto m-auto p-8">
	<table style="border: 1px solid black; border-collapse: 10px;" class="m-auto mb-10">
		{#each ocupacion_bloques[block - 1] as row}
			<tr>
				{#each row as taquilla}
					{#if taquilla.status == 'libre'}
						<td
							class:py-8={taquilla.taquilla.includes('G')}
							class:p-4={taquilla.taquilla.includes('P')}
							style="border: 1px solid black; border-collapse: 10px"
							class="bg-green-500 cursor-pointer hover:bg-green-400 text-center"
							on:click={() => openModal(taquilla.taquilla)}
						>
							{taquilla.taquilla}
						</td>
					{:else if taquilla.status == 'ocupada'}
						<td
							class:py-8={taquilla.taquilla.includes('G')}
							class:p-4={taquilla.taquilla.includes('P')}
							style="border: 1px solid black; border-collapse: 10px"
							class=" bg-red-500 cursor-not-allowed text-center"
						>
							{taquilla.taquilla}
						</td>
					{:else if taquilla.status == 'reservada'}
						<td
							class:py-8={taquilla.taquilla.includes('G')}
							class:p-4={taquilla.taquilla.includes('P')}
							style="border: 1px solid black; border-collapse: 10px"
							class="bg-yellow-300 cursor-not-allowed text-center"
						>
							{taquilla.taquilla}
						</td>
					{:else}
						<td
							class:py-8={taquilla.taquilla.includes('G')}
							class:p-4={taquilla.taquilla.includes('P')}
							id={taquilla.taquilla}
							style="border: 1px solid black; border-collapse: 10px"
							class="bg-gray-500 text-center"
						>
							{taquilla.taquilla}
						</td>
					{/if}
				{/each}
			</tr>
		{/each}
	</table>
</div>
