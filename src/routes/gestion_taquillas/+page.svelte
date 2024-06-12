<script lang="ts">
	/** @type {import('./$types').ActionData} */
	export let form;

	import { enhance } from '$app/forms';
	import { page } from '$app/stores';
	import { Tabs, TabItem, Input, Label, Button, Modal, Card } from 'flowbite-svelte';
	let session;

	// Reactive statement to update session whenever $page.data.session changes
	$: session = $page.data.session;

	let formModalReservation = false;
	let selectedTaquilla = '';
</script>

<h1 class="text-4xl text-center text-[#3BC4A0] m-5">Gestión de Taquillas</h1>
<Tabs tabStyle="underline" contentClass="p-4 bg-white">
	<TabItem
		open
		title="Búsqueda por NIA"
		class="hover:text-[#3BC4A0]"
		inactiveClasses="text-gray-500 hover:text-[#3BC4A0] p-4"
		on:focus={() => {
			form = null;
		}}
	>
		<form action="?/busquedaNia" method="post" use:enhance>
			<div class="grid grid-cols-1">
				<div>
					<Label class="w-4/5 m-auto text-xl text-[#3BC4A0]">NIA</Label>
					<Input
						type="text"
						id="NIA_s"
						name="NIA_s"
						placeholder="NIA del usuario..."
						pattern={'100[0-9]{6}'}
						required
						class="w-4/5 m-auto"
					/>
				</div>
			</div>
			<div class="w-screen mt-8 grid grid-cols-1 place-items-center">
				<Button type="submit" class="bg-[#3BC4A0] text-white px-8 py-2 text-xl hover:bg-[#3BB4A0]"
					>Buscar</Button
				>
			</div>
		</form>
	</TabItem>
	<TabItem
		title="Búsqueda por Taquilla"
		class="hover:text-[#3BC4A0]"
		inactiveClasses="text-gray-500 hover:text-[#3BC4A0] p-4"
		on:focus={() => {
			form = null;
		}}
	>
		<form class="w-screen" action="?/busquedaTaquilla" method="post" use:enhance>
			<div class="grid grid-cols-1">
				<div>
					<Label class="w-4/5 m-auto text-xl text-[#3BC4A0]">Taquilla</Label>
					<Input
						type="text"
						id="Taquilla_s"
						name="Taquilla_s"
						placeholder="Taquilla..."
						pattern={'([0-9].){2}[A-Z].(G|P)[0-9]{3}'}
						required
						class="w-4/5 m-auto"
					/>
				</div>
			</div>
			<div class="w-screen grid grid-cols-1 place-items-center">
				<Button type="submit" class="bg-[#3BC4A0] text-white mt-8 text-xl hover:bg-[#3BB4A0]"
					>Buscar</Button
				>
			</div>
		</form>
	</TabItem>
</Tabs>

<div class="w-screen grid grid-cols-2 place-items-center mt-2">
	{#if form != null && form}
		{#each form.reservas as taquilla}
			<Card class="mt-2">
				<div class="grid grid-cols-2">
					<h5 class="text-2xl text-[#3BC4A0]">{taquilla['taquilla']}</h5>
					<p class="text-right pr-10 p-1 text-black">{taquilla['status']}</p>
				</div>
				<p class="text-black text-sm">Reservada el {taquilla['date']}</p>
				{#if taquilla['status'] === 'reservada'}
					<div class="grid grid-cols-2 mt-4 place-items-center">
						<button class="w-2/3 text-white bg-green-500 rounded">Confirmar</button>
						<button class="w-2/3 text-white bg-red-500 rounded">Eliminar</button>
					</div>
				{:else if taquilla['status'] === 'libre'}
					<div class="grid grid-cols-2 mt-4 place-items-center">
						<button
							class="w-2/3 text-white bg-green-500 rounded"
							on:click={() => {
								selectedTaquilla = taquilla['taquilla'];
								formModalReservation = true;
							}}
						>
							Reservar
						</button>
					</div>
				{/if}
			</Card>
		{/each}
	{/if}
</div>

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
			<Input type="text" id="nia" name="nia" placeholder="100xxxxxx" required />
		</Label>
		<Label class="space-y-2">
			<span>Taquilla</span>
			<Input type="text" id="taquilla" name="taquilla" value={selectedTaquilla} readonly required />
		</Label>

		<Label>
			<span>Nombre:</span>
			<Input type="text" id="nombre" name="nombre" required />
		</Label>

		<Button type="submit" class="w-full1 bg-green-500 hover:bg-blue-400">Reservar Taquilla</Button>
	</form>
</Modal>

<p>Comentarios:</p>
Estaría bien que fuera un desplegable de NIAS para borrar los roles. También tenemos que hacer una página
para consultar las reservas de los un nia.
