<script lang="ts">
	/** @type {import('./$types').ActionData | any} */
	export let form: any;

	import { enhance } from '$app/forms';
	import { page } from '$app/stores';
	import { Tabs, TabItem, Input, Label, Button, Modal, Card } from 'flowbite-svelte';
	import {
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell,
		TableSearch
	} from 'flowbite-svelte';
	import ModalIniciaSesion from '../../ModalIniciaSesion.svelte';
	let session = $page.data.session;

	// Reactive statement to update session whenever $page.data.session changes
	$: session = $page.data.session;

	interface Taquilla {
		codigo: string;
		date: string;
		nia: number;
		nombre: string;
		status: string;
		taquilla: string;
	}

	let TablaPabloItems: [Taquilla] = $page.data.tablaPablo;

	let formModalReservation = false;
	let selectedTaquilla = '';
	let successToast = false;
	let unSuccessToast = false;
	let openModalIniciaSesion = false;
	let deleteModal = false;
	let currentTaquilla: Taquilla;
	let searchTerm = '';

	$: filteredItems = TablaPabloItems.filter(
		(item) => item.nombre.toLowerCase().indexOf(searchTerm.toLowerCase()) !== -1
	);

	async function realizar_reserva(taquilla: String) {
		// Call a function that only runs in the server side:
		let res_email = session?.user?.email || '';
		if (res_email === '') {
			formModalReservation = false;
			openModalIniciaSesion = true;
			return;
		}
		const response = await fetch('/api/realizar_reserva', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ taquilla: taquilla, email: res_email })
		});
		let result = await response.json();
		result = result['result']['message'];
		if (result.includes('confirmada')) {
			successToast = true;
			setTimeout(() => {
				successToast = false;
				location.reload();
			}, 2000);
		} else {
			unSuccessToast = true;
		}
	}

	async function eliminar_reserva(taquilla: String) {
		// Call a function that only runs in the server side:
		let res_email = session?.user?.email || '';
		if (res_email === '') {
			formModalReservation = false;
			openModalIniciaSesion = true;
			return;
		}
		const response = await fetch('/api/eliminar_reserva', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ taquilla: taquilla, email: res_email })
		});

		let result = await response.json();
		result = result['result']['message'];
		if (result.includes('eliminada')) {
			successToast = true;
			setTimeout(() => {
				successToast = false;
				location.reload();
			}, 2000);
		} else {
			unSuccessToast = true;
		}
	}

	function change_delete_modal(taquilla: Taquilla) {
		deleteModal = true;
		currentTaquilla = taquilla;
	}
</script>

<h1 class="text-4xl text-center text-[#3BC4A0] m-5 dark:bg-dark-background dark:text-dark-primary">
	Gestión de Taquillas
</h1>
<Tabs tabStyle="underline" contentClass="p-4" class="px-8">
	<TabItem
		open
		title="Búsqueda por NIA"
		class="hover:text-[#3BC4A0] dark:hover:text-dark-accent dark:text-dark-accent"
		activeClasses="sm:text-base text-xs p-4"
		inactiveClasses="text-gray-500 hover:text-[#3BC4A0] p-4 dark:hover:text-dark-accent sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		<form action="?/busquedaNia" method="post" use:enhance>
			<div class="grid grid-cols-1 w-auto">
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
			<div class="mt-8 grid grid-cols-1 w-auto place-items-center">
				<Button
					type="submit"
					class="bg-[#3BC4A0] text-white px-8 py-2 text-xl hover:bg-[#3BB4A0] dark:bg-dark-primary dark:hover:bg-dark-accent"
					>Buscar</Button
				>
			</div>
		</form>
	</TabItem>
	<TabItem
		title="Búsqueda por Taquilla"
		class="hover:text-[#3BC4A0] dark:hover:text-dark-accent dark:text-dark-accent"
		activeClasses="sm:text-base text-xs p-4"
		inactiveClasses="text-gray-500 hover:text-[#3BC4A0] p-4 dark:hover:text-dark-accent sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		<form action="?/busquedaTaquilla" method="post" use:enhance>
			<div class="grid grid-cols-1 w-auto">
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
			<div class="grid grid-cols-1 w-auto place-items-center">
				<Button
					type="submit"
					class="bg-[#3BC4A0] text-white mt-8 px-8 py-2 text-xl hover:bg-[#3BB4A0] dark:bg-dark-primary dark:hover:bg-dark-accent"
					>Buscar</Button
				>
			</div>
		</form>
	</TabItem>
	<TabItem
		title="Tabla Pablo"
		class="hover:text-[#3BC4A0] dark:hover:text-dark-accent dark:text-dark-accent"
		activeClasses="sm:text-base text-xs p-4"
		inactiveClasses="text-gray-500 hover:text-[#3BC4A0] p-4 dark:hover:text-dark-accent sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		<TableSearch placeholder="Busca por Nombre" hoverable={true} bind:inputValue={searchTerm}>
			<TableHead>
				<TableHeadCell>Nombre</TableHeadCell>
				<TableHeadCell>Nia</TableHeadCell>
				<TableHeadCell>Taquilla</TableHeadCell>
				<TableHeadCell>Código</TableHeadCell>
				<TableHeadCell>Fecha</TableHeadCell>
				<TableHeadCell>Status</TableHeadCell>
			</TableHead>
			<TableBody tableBodyClass="divide-y">
				{#each filteredItems as item}
					<TableBodyRow>
						<TableBodyCell>{item.nombre}</TableBodyCell>
						<TableBodyCell>{item.nia}</TableBodyCell>
						<TableBodyCell>{item.taquilla}</TableBodyCell>
						<TableBodyCell>{item.codigo}</TableBodyCell>
						<TableBodyCell>{item.date}</TableBodyCell>
						<TableBodyCell>{item.status}</TableBodyCell>
					</TableBodyRow>
				{/each}
			</TableBody>
		</TableSearch></TabItem
	>
</Tabs>

<div class="w-screen grid xl:grid-cols-3 md:grid-cols-2 grid-cols-1 place-items-center mt-2">
	{#if form != null && form}
		{#each form.reservas as taquilla}
			<Card class="mt-2">
				<div class="flex place-content-between">
					<h5 class="text-2xl font-medium underline text-[#3BC4A0] dark:text-dark-primary">
						{taquilla['taquilla']}
					</h5>
					{#if taquilla['status'] === 'reservada'}
						<p class="text-center p-1 text-white bg-yellow-400 rounded">
							Reservada: {taquilla['codigo']}
						</p>
					{:else if taquilla['status'] === 'libre'}
						<p class="text-center p-1 text-white bg-green-500 rounded">Libre</p>
					{:else if taquilla['status'] === 'ocupada'}
						<p class="text-center p-1 text-white bg-red-500 rounded">Ocupada</p>
					{:else}
						<p class="text-center p-1 text-white bg-black rounded">No disponible</p>
					{/if}
				</div>
				{#if taquilla['status'] === 'reservada' || taquilla['status'] === 'ocupada'}
					<p class="text-black text-sm mt-4 dark:text-white">
						Reservada por <b>{taquilla['nia']}</b> el {taquilla['date']} a las {taquilla[
							'date'
						].split(' ')[1]}
					</p>
				{/if}
				{#if taquilla['status'] === 'reservada'}
					<div class="grid grid-cols-2 mt-4 place-items-center">
						<button
							class="w-2/3 text-white bg-green-500 rounded p-1"
							on:click={() => {
								realizar_reserva(taquilla['taquilla']);
							}}>Confirmar</button
						>

						<button
							class="w-2/3 text-white bg-red-500 rounded p-1"
							on:click={() => {
								change_delete_modal(taquilla);
							}}>Eliminar</button
						>
					</div>
				{:else if taquilla['status'] === 'libre'}
					<div class="grid grid-cols-1 mt-4 place-items-center">
						<button
							class="w-1/2 text-white bg-green-500 rounded p-1"
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

		<Button
			type="submit"
			class="w-full1 bg-green-500 hover:bg-[#FF6D2E] dark:bg-dark-primary dark:hover:bg-dark-accent"
			>Reservar Taquilla</Button
		>
	</form>
</Modal>

<ModalIniciaSesion bind:openForm={openModalIniciaSesion}></ModalIniciaSesion>

<Modal bind:open={deleteModal} size="xs" autoclose={false} class="w-full">
	<form class="flex flex-col space-y-6">
		<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white">Eliminar Reserva</h3>
		<p>Vas a eliminar una reserva con los siguientes datos:</p>
		<Label class="space-y-2">
			<span>NIA:</span>
			<Input type="text" id="nia" name="nia" value={currentTaquilla['nia']} readonly required />
		</Label>
		<Label class="space-y-2">
			<span>Taquilla</span>
			<Input
				type="text"
				id="taquilla"
				name="taquilla"
				value={currentTaquilla['taquilla']}
				readonly
				required
			/>
		</Label>
		<Button
			type="submit"
			class="w-full1 bg-green-500 hover:bg-[#FF6D2E] dark:bg-dark-primary dark:hover:bg-dark-accent"
			on:click={(ev) => {
				ev.preventDefault();
				deleteModal = false;
				eliminar_reserva(currentTaquilla['taquilla']);
			}}>Eliminar Reserva</Button
		>
	</form>
</Modal>

{#if successToast}
	<div class="fixed bottom-0 right-0 m-5">
		<Card class="bg-green-500 text-white">
			<p class="p-2">Acción realizada con éxito</p>
		</Card>
	</div>
{:else if unSuccessToast}
	<div class="fixed bottom-0 right-0 m-5">
		<Card class="bg-red-500 text-white">
			<p class="p-2">Acción no realizada con éxito</p>
		</Card>
	</div>
{/if}
