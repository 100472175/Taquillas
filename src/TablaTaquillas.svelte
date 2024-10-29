<script lang="ts">
	import type { PageData } from './$types';
	import { Modal, Label, Input, Button } from 'flowbite-svelte';
	import { signIn, signOut } from '@auth/sveltekit/client';
	import { goto } from '$app/navigation';
	import { enhance } from '$app/forms';
	import ModalIniciaSesion from './ModalIniciaSesion.svelte';
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

<Modal bind:open={formModalReservation} size="xs" autoclose={false} class="w-full recompensa:bg-recompensa-secondary">
	{#if data.session?.user?.email?.endsWith('@alumnos.uc3m.es')}
		<form
			class="flex flex-col space-y-6"
			action="?/registerTaquilla"
			method="post"
			use:enhance
			on:submit={() => {
				formModalReservation = false;
			}}
		>
			<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white recompensa:text-white">Reservar Taquilla</h3>
			<p class="dark:text-white recompensa:text-white">
				La reserva de la taquilla {selectedTaquilla}. El precio de las taquilla
				{#if selectedTaquilla.includes('G')}al ser <span class="italic">grande</span> es de
					<span class="font-bold">6€</span> para
				{:else}
					al ser <span class="italic">pequeña</span> es de <span class="font-bold"> 4€ </span>para
				{/if} el año completo y la mitad para el segundo cuatrimestre. Este importe se abona en delegación
				de estudiantes
				<a
					href="https://maps.app.goo.gl/QaxfXbWVz5AvqsCW6"
					class="underline hover:dark:text-dark-accent hover:recompensa:text-recompensa-accent hover:text-accent">(1.0.H01)</a
				>.
			</p>
			<Label class="space-y-2 recompensa:text-white">
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
			<Label class="space-y-2 recompensa:text-white">
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

			<Button
				type="submit"
				class="w-full1 bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent recompensa:bg-recompensa-primary hover:recompensa:bg-recompensa-accent"
				>Reservar Taquilla</Button
			>
		</form>
	{:else if data.session?.user?.email?.endsWith("uc3m.es")}
		<form
		class="flex flex-col space-y-6"
		action="?/registerTaquillaAssociation"
		method="post"
		use:enhance
		on:submit={() => {
			formModalReservation = false;
		}}
		>
			<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white recompensa:text-white">Reservar Taquilla</h3>
			<p class="dark:text-white recompensa:text-white">
				La reserva de la taquilla {selectedTaquilla}. El precio de las taquilla
				{#if selectedTaquilla.includes('G')}al ser <span class="italic">grande</span> es de
					<span class="font-bold">6€</span> para
				{:else}
					al ser <span class="italic">pequeña</span> es de <span class="font-bold"> 4€ </span>para
				{/if} el año completo y la mitad para el segundo cuatrimestre. Este importe se abona en delegación
				de estudiantes
				<a
					href="https://maps.app.goo.gl/QaxfXbWVz5AvqsCW6"
					class="underline hover:dark:text-dark-accent hover:recompensa:text-recompensa-accent hover:text-accent">(1.0.H01)</a
				>.
			</p>
			
			<Label class="space-y-2">
				<span>Nombre Asociación</span>
				<Input
					type="text"
					id="nombre"
					name="nombre"
					value={data.session?.user?.name}
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

			<Button
				type="submit"
				class="w-full1 bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent recompensa:bg-recompensa-primary hover:recompensa:bg-recompensa-accent"
				>Reservar Taquilla
			</Button>
		</form>
	{/if}
</Modal>

<ModalIniciaSesion bind:openForm={formModalInformationError}></ModalIniciaSesion>

<Modal bind:open={formModalInformationError} size="xs" autoclose={false} class="w-full recompensa:bg-recompensa-secondary">
	<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white recompensa:text-white">Error</h3>
	<p class="dark:text-white recompensa:text-white">Debes iniciar sesión para reservar una taquilla</p>
	<Button
		type="button"
		class="w-full bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent recompensa:bg-recompensa-primary hover:recompensa:bg-recompensa-accent"
		on:click={() => {
			signIn();
		}}
	>
		Iniciar Sesión
	</Button>
</Modal>

<div class="w-10/12 overflow-auto m-auto mt-6">
	<table
		style="border: 2px solid black; border-collapse: 10px; border-radius: 13px; border-spacing: 0; "
		class="m-auto"
	>
		{#each ocupacion_bloques[block - 1] as row}
			<tr>
				{#each row as taquilla}
					{#if taquilla.status == 'libre'}
						<td
							class:py-8={taquilla.taquilla.includes('G')}
							class:p-4={taquilla.taquilla.includes('P')}
							style="border: 1px solid black; border-collapse: 10px"
							class="bg-green-500 cursor-pointer hover:bg-green-400 text-center px-3"
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
