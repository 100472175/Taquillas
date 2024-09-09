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
		TableSearch,
		Dropdown,
		DropdownItem, 
		DropdownDivider, 
		DropdownHeader
	} from 'flowbite-svelte';
	import { ChevronDownOutline } from "flowbite-svelte-icons";
	import ModalIniciaSesion from '../../ModalIniciaSesion.svelte';
	import { goto } from '$app/navigation';
  	import TablaTaquillas from '../../TablaTaquillas.svelte';
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

	interface Asociaciones {
		nombre: string;
		correo: string;
	}

	let TablaPabloItems: [Taquilla] = $page.data.tablaPablo.filter((item) => {
		return (item.nia);
	});
	let TablaPabloAsociacionesItems: [Taquilla] = $page.data.tablaPablo.filter((item) => {
		return (!item.nia);
	});
	console.log($page.data.tablaPablo);

	let asociaciones = $page.data.asociaciones;
	let association_selected = {"nombre": "", "correo": ""};

	let formModalReservation = false;
	let selectedTaquilla = '';
	let successToast = false;
	let unSuccessToast = false;
	let openModalIniciaSesion = false;
	let deleteModal = false;
	let deleteModal_a = false;
	let currentTaquilla: Taquilla;
	let searchTerm = '';
	let searchTermAsociaciones = '';
	let openDropdown = false;

	let show_results = true;
	
	$: filteredItems = TablaPabloItems.filter((item) =>{
		return (item.status != "rota" && item.nombre.toLowerCase().indexOf(searchTerm.toLowerCase()) !== -1);
	});

	$: filteredItems_a = TablaPabloAsociacionesItems.filter((item) =>{
		return (item.status != "rota" && item.nombre.toLowerCase().indexOf(searchTermAsociaciones.toLowerCase()) !== -1);
	});

	$: taquillasRotas = $page.data.tablaPablo.filter((item) => {
		return (item.status == "rota" && item.taquilla.toLowerCase().indexOf(searchTerm.toLowerCase()) !== -1);
	})
	
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
			}, 1000);
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
			}, 1000);
		} else {
			unSuccessToast = true;
		}
	}

	async function marcar_rota(taquilla: String) {
		// Call a function that only runs in the server side:
		let res_email = session?.user?.email || '';
		if (res_email === '') {
			formModalReservation = false;
			openModalIniciaSesion = true;
			return;
		}
		const response = await fetch('/api/marcar_rota', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ taquilla: taquilla, email: res_email })
		});

		let result = await response.json();
		result = result['result']['message'];
		if (result.includes('correctamente')) {
			successToast = true;
			setTimeout(() => {
				successToast = false;
				location.reload();
			}, 2000);
		} else {
			unSuccessToast = true;
		}
	}

	async function marcar_reparada(taquilla: String) {
		// Call a function that only runs in the server side:
		let res_email = session?.user?.email || '';
		if (res_email === '') {
			formModalReservation = false;
			openModalIniciaSesion = true;
			return;
		}
		const response = await fetch('/api/marcar_reparada', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ taquilla: taquilla, email: res_email })
		});

		let result = await response.json();
		result = result['result']['message'];
		if (result.includes('correctamente')) {
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

	function change_delete_modal_asociaciones(taquilla: Taquilla) {
		deleteModal_a = true;
		currentTaquilla = taquilla;
	}

	function closeModalAssignAssociation(association: Asociaciones) {
		openDropdown = false;
		association_selected = association;
	}

	function handleFormSubmit(event) {
        // Verificar si el nombre de la asociación está vacío
        if (!association_selected["nombre"]) {
            event.preventDefault(); // Prevenir el envío del formulario
        } else {
            // Permitir el envío del formulario
            event.target.submit();
        }
    }
</script>

<h1 class="text-4xl text-center text-dele-color m-5 dark:bg-dark-background dark:text-dark-primary">
	Gestión de Taquillas
</h1>
<Tabs tabStyle="underline" contentClass="p-4" class="px-8">
	<TabItem
		open
		title="Búsqueda por NIA"
		class=""
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		<form action="?/busquedaNia" method="post" use:enhance>
			<div class="grid grid-cols-1 w-auto">
				<div>
					<Label class="w-4/5 m-auto text-xl text-dele-color">NIA</Label>
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
					class="bg-dele-color text-white px-8 py-2 text-xl hover:bg-dele-color dark:bg-dark-primary dark:hover:bg-dark-accent"
					>Buscar</Button
				>
			</div>
		</form>
	</TabItem>
	<TabItem
		title="Búsqueda por Taquilla"
		class=""
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		<form action="?/busquedaTaquilla" method="post" use:enhance>
			<div class="grid grid-cols-1 w-auto">
				<div>
					<Label class="w-4/5 m-auto text-xl text-dele-color">Taquilla</Label>
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
					class="bg-dele-color text-white mt-8 px-8 py-2 text-xl hover:bg-dele-color dark:bg-dark-primary dark:hover:bg-dark-accent"
					>Buscar</Button
				>
			</div>
		</form>
	</TabItem>
	<TabItem
		title="Tabla Pablo"
		class=""
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		{@const reservadas = TablaPabloItems.filter((item) => item.status === 'reservada').length}
		{@const ocupadas = TablaPabloItems.filter((item) => item.status === 'ocupada').length}
		{@const no_disponibles = TablaPabloItems.filter((item) => item.status === 'rota').length}

		<div class="grid grid-cols-3 place-items-center">
			<div class="text-center">
				<p class="text-dele-color dark:text-dark-primary">Reservadas</p>
				<p class="text-2xl dark:text-dark-accent">{reservadas}</p>
			</div>
			<div class="text-center">
				<p class="text-dele-color dark:text-dark-primary">Ocupadas</p>
				<p class="text-2xl dark:text-dark-accent">{ocupadas}</p>
			</div>
			<div class="text-center">
				<p class="text-dele-color dark:text-dark-primary">No disponibles</p>
				<p class="text-2xl dark:text-dark-accent">{no_disponibles}</p>
			</div>
		</div>

		<TableSearch placeholder="Busca por Nombre" hoverable={true} bind:inputValue={searchTerm}>
			<TableHead>
				<TableHeadCell>Nombre</TableHeadCell>
				<TableHeadCell>Nia</TableHeadCell>
				<TableHeadCell>Taquilla</TableHeadCell>
				<TableHeadCell>Código</TableHeadCell>
				<TableHeadCell>Fecha</TableHeadCell>
				<TableHeadCell>Estado</TableHeadCell>
				<TableHeadCell>Acciones</TableHeadCell>
			</TableHead>
			<TableBody tableBodyClass="divide-y">
				{#if filteredItems != null && filteredItems}
					{#each filteredItems as item}
						<TableBodyRow>
							<TableBodyCell>{item.nombre}</TableBodyCell>
							<TableBodyCell>{item.nia}</TableBodyCell>
							<TableBodyCell>{item.taquilla}</TableBodyCell>
							<TableBodyCell>{item.codigo}</TableBodyCell>
							<TableBodyCell>{item.date}</TableBodyCell>
							<TableBodyCell>{item.status.charAt(0).toUpperCase() + item.status.slice(1)}</TableBodyCell>
							<TableBodyCell>
								<div class="grid grid-cols-1 xl:grid-cols-2">
									{#if item.status === "reservada"}
										<button
											class="xl:w-[95%] w-full mb-2 xl:mb-0 text-xs lg:text-md text-white bg-green-500 rounded p-1"
											on:click={() => {
												realizar_reserva(item.taquilla);
											}}>
											Confirmar
										</button>
										<button
											class="xl:w-[95%] w-full text-xs lg:text-md text-white bg-red-500 rounded p-1"
											on:click={() => {
												change_delete_modal(item);
											}}>
											Eliminar
										</button>
									{:else if item.status === "ocupada"}
										<button
											class="w-full text-xs lg:text-md text-white bg-red-500 rounded p-1 xl:col-span-2"
											on:click={() => {
												change_delete_modal(item);
											}}>
											Eliminar
										</button>
									{/if}
								</div>
							</TableBodyCell>
						</TableBodyRow>
					{/each}
				{/if}
			</TableBody>
		</TableSearch>
	</TabItem>
	<TabItem
		title="Tabla Asociaciones"
		class=""
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		{@const reservadas = TablaPabloAsociacionesItems.filter((item) => item.status === 'reservada').length}
		{@const ocupadas = TablaPabloAsociacionesItems.filter((item) => item.status === 'ocupada').length}
		{@const no_disponibles = $page.data.tablaPablo.filter((item) => item.status === 'rota').length}

		<div class="grid grid-cols-3 place-items-center">
			<div class="text-center">
				<p class="text-dele-color dark:text-dark-primary">Reservadas</p>
				<p class="text-2xl dark:text-dark-accent">{reservadas}</p>
			</div>
			<div class="text-center">
				<p class="text-dele-color dark:text-dark-primary">Ocupadas</p>
				<p class="text-2xl dark:text-dark-accent">{ocupadas}</p>
			</div>
			<div class="text-center">
				<p class="text-dele-color dark:text-dark-primary">No disponibles</p>
				<p class="text-2xl dark:text-dark-accent">{no_disponibles}</p>
			</div>
		</div>

		<TableSearch placeholder="Busca por Nombre" hoverable={true} bind:inputValue={searchTerm}>
			<TableHead>
				<TableHeadCell>Nombre</TableHeadCell>
				<TableHeadCell>Taquilla</TableHeadCell>
				<TableHeadCell>Código</TableHeadCell>
				<TableHeadCell>Fecha</TableHeadCell>
				<TableHeadCell>Estado</TableHeadCell>
				<TableHeadCell>Acciones</TableHeadCell>
			</TableHead>
			<TableBody tableBodyClass="divide-y">
				{#if filteredItems_a != null && filteredItems_a}
					{#each filteredItems_a as item}
						<TableBodyRow>
							<TableBodyCell>{item.nombre}</TableBodyCell>
							<TableBodyCell>{item.taquilla}</TableBodyCell>
							<TableBodyCell>{item.codigo}</TableBodyCell>
							<TableBodyCell>{item.date}</TableBodyCell>
							<TableBodyCell>{item.status.charAt(0).toUpperCase() + item.status.slice(1)}</TableBodyCell>
							<TableBodyCell>
								<div class="grid grid-cols-1 xl:grid-cols-2">
									{#if item.status === "reservada"}
										<button
											class="xl:w-[95%] w-full mb-2 xl:mb-0 text-xs lg:text-md text-white bg-green-500 rounded p-1"
											on:click={() => {
												realizar_reserva(item.taquilla);
											}}>
											Confirmar
										</button>
										<button
											class="xl:w-[95%] w-full text-xs lg:text-md text-white bg-red-500 rounded p-1"
											on:click={() => {
												change_delete_modal_asociaciones(item);
											}}>
											Eliminar
										</button>
									{:else if item.status === "ocupada"}
										<button
											class="w-full text-xs lg:text-md text-white bg-red-500 rounded p-1 xl:col-span-2"
											on:click={() => {
												change_delete_modal_asociaciones(item);
											}}>
											Eliminar
										</button>
									{/if}
								</div>
							</TableBodyCell>
						</TableBodyRow>
					{/each}
				{/if}
			</TableBody>
		</TableSearch>
	</TabItem>
	<TabItem
		title="Taquillas Rotas"
		class=""
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		<TableSearch placeholder="Busca por Taquilla" hoverable={true} bind:inputValue={searchTerm}>
			<TableHead>
				<TableHeadCell>Taquilla</TableHeadCell>
				<TableHeadCell>No disponible desde</TableHeadCell>
				<TableHeadCell>Reparar</TableHeadCell>
			</TableHead>
			<TableBody tableBodyClass="divide-y">
				{#if taquillasRotas != null && taquillasRotas}
					{#each taquillasRotas as item}
						<TableBodyRow>
							<TableBodyCell>{item.taquilla}</TableBodyCell>
							<TableBodyCell>{item.date}</TableBodyCell>
							<TableBodyCell>
								<button
									class="w-full text-white bg-green-500 dark:text-white rounded p-1"
									on:click={() => {
										marcar_reparada(item.taquilla);
									}}
								>
									Marcar como reparada
								</button>
							</TableBodyCell>
						</TableBodyRow>
					{/each}
				{/if}
			</TableBody>
		</TableSearch>
	</TabItem>
</Tabs>

<div class="w-screen grid xl:grid-cols-3 md:grid-cols-2 grid-cols-1 place-items-center mt-2">
	{#if form != null && form && form.reservas}
		{#each form.reservas as taquilla}
			<Card class="mt-2">
				<div class="flex place-content-between ">
					<h5 class="text-2xl font-medium underline text-dele-color dark:text-dark-primary">
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
					{:else if taquilla['status'] === 'null'}
						<p class="text-center p-1 text-white bg-black rounded">No existe</p>
					{:else}
						<p class="text-center p-1 text-white bg-black rounded">No disponible</p>
					{/if}

				</div>
				{#if taquilla['status'] === 'reservada' || taquilla['status'] === 'ocupada'}
					{#if taquilla["nia"]}
						<p class="text-black text-sm mt-4 dark:text-white">
							Reservada por {taquilla['nombre']} (<b>{taquilla['nia']}</b>) el {taquilla['date'].split(' ')[0]} a las {taquilla[
								'date'
							].split(' ')[1]}
						</p>
					{:else}
						<p class="text-black text-sm mt-4 dark:text-white">
							Reservada por {taquilla['asociacion']} el {taquilla['date'].split(' ')[0]} a las {taquilla['date'].split(' ')[1]}
						</p>
					{/if}
				{/if}
				{#if taquilla['status'] === 'reservada'}
					<div class="grid grid-cols-1 place-items-center mt-4">
						<button
							class="w-10/12 text-white bg-green-500 rounded p-1"
							on:click={() => {
								realizar_reserva(taquilla['taquilla']);
							}}>Confirmar</button
						>
					</div>
					<div class="grid grid-cols-2 place-items-center mt-4">
						<button
							class="w-2/3 text-white bg-gray-500 rounded p-1"
							on:click={() => {
								marcar_rota(taquilla['taquilla']);
							}}>Marcar rota</button
						>
						{#if taquilla["nia"]} 
							<button
								class="w-2/3 text-white bg-red-500 rounded p-1"
								on:click={() => {
									change_delete_modal(taquilla);
								}}>Eliminar</button
							>
						{:else}
							<button
								class="w-2/3 text-white bg-red-500 rounded p-1"
								on:click={() => {
									change_delete_modal_asociaciones(taquilla);
								}}>Eliminar</button
							>
						{/if}
						
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
						<button
							class="w-1/2 text-white bg-gray-500 rounded p-1 mt-4"
							on:click={() => {
								marcar_rota(taquilla['taquilla']);
							}}
						>
							Marcar como rota
						</button>
					</div>
				{:else if taquilla['status'] === 'ocupada'}
					<div class="grid grid-cols-1 mt-4 place-items-center">
						{#if taquilla["nia"]} 
							<button
								class="w-2/3 text-white bg-red-500 rounded p-1"
								on:click={() => {
									change_delete_modal(taquilla);
								}}>Eliminar</button
							>
						{:else}
							<button
								class="w-2/3 text-white bg-red-500 rounded p-1"
								on:click={() => {
									change_delete_modal_asociaciones(taquilla);
								}}>Eliminar</button
							>
						{/if}
						<button
							class="w-2/3 text-white bg-gray-500 rounded p-1 mt-4"
							on:click={() => {
								marcar_rota(taquilla['taquilla']);
							}}
						>
							Marcar como rota
						</button>
					</div>
				{:else if taquilla['status'] === 'null'}
					<div></div>
				{:else}
					<div class="grid grid-cols-1 mt-4 place-items-center">
						<button
							class="w-1/2 text-white-500 bg-green-500 dark:text-white rounded p-1"
							on:click={() => {
								marcar_reparada(taquilla['taquilla']);
							}}
						>
							Marcar como reparada
						</button>
					</div>
				{/if}
			</Card>
		{/each}
	{/if}
</div>

<Modal bind:open={formModalReservation} size="xs" autoclose={false} class="w-full">
	<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white">Reservar Taquilla</h3>
	<p>
		El precio de la taquilla es de
		{#if selectedTaquilla.includes('G')}<span class="font-bold"> 6€ </span>
		{:else}<span class="font-bold"> 4€ </span>
		{/if} el año completo y la mitad por el segundo cuatrimestre.
	</p>
	<Tabs>
		<TabItem
			open
			title="Estudiantes"
			class=""
			activeClasses="sm:text-base text-xs p-2 text-dele-accent dark:text-dark-accent"
			inactiveClasses="text-gray-500 hover:text-dele-color p-2 dark:hover:text-dark-primary sm:text-base text-xs"
			>
			<form class="flex flex-col" action="?/registerTaquilla" method="post">
				<Input type="hidden" id="correo" name="correo" value={session?.user?.email} required />
				<Label class="mb-4">
					<span>NIA:</span>
					<Input type="text" id="nia" name="nia" placeholder="100xxxxxx" required />
				</Label>
				<Label class="mb-4">
					<span>Taquilla</span>
					<Input type="text" id="taquilla" name="taquilla" value={selectedTaquilla} readonly required />
				</Label>
				<Label class="mb-4">
					<span>Nombre:</span>
					<Input type="text" id="nombre" name="nombre" required />
				</Label>
				
				<Button
					type="submit"
					class="w-full bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent"
					on:click={() => {
						show_results = false;
					}}>
					Reservar Taquilla
				</Button>
			</form>
		</TabItem>
		<TabItem
			title="Asociaciones"
			class=""
			activeClasses="sm:text-base text-xs p-2 text-dele-accent dark:text-dark-accent"
			inactiveClasses="text-gray-500 hover:text-dele-color p-2 dark:hover:text-dark-primary sm:text-base text-xs"
		>
			<form class="flex flex-col" action="?/registerTaquillaAssociation" method="post" on:submit|preventDefault={handleFormSubmit}>
				<Label class="mb-4">
					<span>Taquilla</span>
					<Input type="text" id="taquilla" name="taquilla" value={selectedTaquilla} readonly required />
				</Label>
				<Input type="hidden" id="correo" name="correo" value={association_selected["correo"]} required />
				<Input type="hidden" id="nombre" name="nombre" value={association_selected["nombre"]} required />
				<Label class="mb-4">
					<Button class="w-full bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent">
						Asociación: 
							{#if association_selected["nombre"]}
								{association_selected["nombre"]} 
							{:else}
								
							{/if}
							<ChevronDownOutline class="w-6 h-6 ms-2 text-white dark:text-white" />
					</Button>
					<Dropdown bind:open={openDropdown}>
						<div slot="header" class="px-4 py-2">
							<span class="block text-sm text-gray-900 dark:text-white">Selecciona una asociación</span>
						</div>
						{#each asociaciones as asociacion}
							<DropdownItem 
							class="rounded p-2 hover:bg-gray-100 dark:hover:bg-gray-600"
							on:click={() => closeModalAssignAssociation(asociacion)}>
								{#if asociacion["nombre"] && asociacion["nombre"] != ""}
									{asociacion["nombre"]}
								{/if}
							</DropdownItem>
						{/each}
					</Dropdown>
				</Label>
				<Button
					type="submit"
					class="w-full bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent"
					on:click={() => {
						show_results = false;
					}}>Reservar Taquilla</Button
				>
			</form>
		</TabItem>
	</Tabs>
	
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
			class="w-full1 bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent"
			on:click={(ev) => {
				ev.preventDefault();
				deleteModal = false;
				eliminar_reserva(currentTaquilla['taquilla']);
			}}>Eliminar Reserva</Button
		>
	</form>
</Modal>

<Modal bind:open={deleteModal_a} size="xs" autoclose={false} class="w-full">
	<form class="flex flex-col space-y-6">
		<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white">Eliminar Reserva</h3>
		<p>Vas a eliminar una reserva con los siguientes datos:</p>
		<Label class="space-y-2">
			<span>Nombre Asociación</span>
			<Input type="text" id="nombre" name="nombre" value={currentTaquilla['asociacion']} readonly required />
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
			class="w-full1 bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent"
			on:click={(ev) => {
				ev.preventDefault();
				deleteModal_a = false;
				eliminar_reserva(currentTaquilla['taquilla']);
			}}>Eliminar Reserva</Button
		>
	</form>
</Modal>


{#if successToast}
	<div class="fixed bottom-0 right-0 m-5">
		<Card class="bg-green-500 dark:text-white text-white dark:bg-green-500">
			<p class="p-2">Acción realizada con éxito</p>
		</Card>
	</div>
{:else if unSuccessToast}
	<div class="fixed bottom-0 right-0 m-5">
		<Card class="bg-red-500 dark:text-white text-white dark:bg-red-500">
			<p class="p-2">La acción ha fallado</p>
		</Card>
	</div>
{/if}
