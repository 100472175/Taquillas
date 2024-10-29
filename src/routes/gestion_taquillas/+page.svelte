<script lang="ts">
	/** @type {import('./$types').ActionData | any} */
	export let form: any;

	import { enhance } from '$app/forms';
	import { page } from '$app/stores';
	import { Tabs, TabItem, Input, Label, Button, Modal, Card, Popover } from 'flowbite-svelte';
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
	import { ChevronDownOutline,  CaretDownSolid, CaretUpSolid } from "flowbite-svelte-icons";
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

	function count_reservas(size, list) {
		let count = 0;
		for (let taquilla of list) {
			if (taquilla.taquilla[6] == size) {
				count += 1;
			}
		}
		return count;
	}

	$: sortedItems = filteredItems;
	let sorting = false;
	let sorting_dir = true;

	function change_sorting() {
		sorting = !sorting;
		if (!sorting) {
			sortedItems = filteredItems;
		}
		else {
			if (!sorting_dir) {
			sortedItems = [...filteredItems].sort((a, b) => {
				let trimmed_a = a.taquilla.substring(0, 4) + a.taquilla.substring(7);
				let trimmed_b = b.taquilla.substring(0, 4) + b.taquilla.substring(7);
				return trimmed_a.localeCompare(trimmed_b);
			});
			}
			else {
				sortedItems = [...filteredItems].sort((a, b) => {
					let trimmed_a = a.taquilla.substring(0, 4) + a.taquilla.substring(7);
					let trimmed_b = b.taquilla.substring(0, 4) + b.taquilla.substring(7);
					return trimmed_b.localeCompare(trimmed_a);
				});
			}
		}
	}
	
	function change_sorting_dir() {
		if (sorting_dir) {
			sortedItems = [...filteredItems].sort((a, b) => {
				let trimmed_a = a.taquilla.substring(0, 4) + a.taquilla.substring(7);
				let trimmed_b = b.taquilla.substring(0, 4) + b.taquilla.substring(7);
				return trimmed_a.localeCompare(trimmed_b);
			});
		}
		else {
			sortedItems = [...filteredItems].sort((a, b) => {
				let trimmed_a = a.taquilla.substring(0, 4) + a.taquilla.substring(7);
				let trimmed_b = b.taquilla.substring(0, 4) + b.taquilla.substring(7);
				return trimmed_b.localeCompare(trimmed_a);
			});
		}
		sorting_dir = !sorting_dir;
	}

	$: sortedItems_a = filteredItems_a;
	let sorting_a = false;
	let sorting_dir_a = true;

	function change_sorting_a() {
		sorting_a = !sorting_a;
		if (!sorting_a) {
			sortedItems_a = filteredItems_a;
		}
		else {
			if (!sorting_dir_a) {
			sortedItems_a = [...filteredItems_a].sort((a, b) => {
				let trimmed_a = a.taquilla.substring(0, 4) + a.taquilla.substring(7);
				let trimmed_b = b.taquilla.substring(0, 4) + b.taquilla.substring(7);
				return trimmed_a.localeCompare(trimmed_b);
			});
			}
			else {
				sortedItems_a = [...filteredItems_a].sort((a, b) => {
					let trimmed_a = a.taquilla.substring(0, 4) + a.taquilla.substring(7);
					let trimmed_b = b.taquilla.substring(0, 4) + b.taquilla.substring(7);
					return trimmed_b.localeCompare(trimmed_a);
				});
			}
		}
	}

	function change_sorting_dir_a() {
		if (sorting_dir_a) {
			sortedItems_a = [...filteredItems_a].sort((a, b) => {
				let trimmed_a = a.taquilla.substring(0, 4) + a.taquilla.substring(7);
				let trimmed_b = b.taquilla.substring(0, 4) + b.taquilla.substring(7);
				return trimmed_a.localeCompare(trimmed_b);
			});
		}
		else {
			sortedItems_a = [...filteredItems_a].sort((a, b) => {
				let trimmed_a = a.taquilla.substring(0, 4) + a.taquilla.substring(7);
				let trimmed_b = b.taquilla.substring(0, 4) + b.taquilla.substring(7);
				return trimmed_b.localeCompare(trimmed_a);
			});
		}
		sorting_dir_a = !sorting_dir_a;
	}

</script>

<h1 class="text-4xl text-center text-dele-color m-5 dark:bg-dark-background dark:text-dark-primary recompensa:bg-recompensa-secondarybackground recompensa:text-recompensa-primary">
	Gestión de Taquillas
</h1>
<Tabs defaultClass="flex flex-coll space-x-2 rtl:space-x-reverse overflow-x-auto" class="px-8" tabStyle="underline" contentClass="p-4">
	<TabItem
		open
		title="Búsqueda por NIA"
		class=""
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent recompensa:text-recompensa-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary recompensa:text-recompensa-primary hover:recompensa:text-white sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		<form action="?/busquedaNia" method="post" use:enhance>
			<div class="grid grid-cols-1 w-auto">
				<div>
					<Label class="w-4/5 m-auto text-xl text-dele-color recompensa:text-recompensa-primary">NIA</Label>
					<Input
						type="text"
						id="NIA_s"
						name="NIA_s"
						placeholder="NIA del usuario..."
						pattern={'100[0-9]{6}'}
						required
						class="w-4/5 m-auto recompensa:bg-[#e0e0e0]"
					/>
				</div>
			</div>
			<div class="mt-8 grid grid-cols-1 w-auto place-items-center">
				<Button
					type="submit"
					class="bg-dele-color text-white px-8 py-2 text-xl hover:bg-dele-color dark:bg-dark-primary dark:hover:bg-dark-accent recompensa:bg-recompensa-primary hover:recompensa:bg-recompensa-accent"
					>Buscar</Button
				>
			</div>
		</form>
	</TabItem>
	<TabItem
		title="Búsqueda por Taquilla"
		class=""
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent recompensa:text-recompensa-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary recompensa:text-recompensa-primary hover:recompensa:text-white sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		<form action="?/busquedaTaquilla" method="post" use:enhance>
			<div class="grid grid-cols-1 w-auto">
				<div>
					<Label class="w-4/5 m-auto text-xl text-dele-color recompensa:text-recompensa-primary">Taquilla</Label>
					<Input
						type="text"
						id="Taquilla_s"
						name="Taquilla_s"
						placeholder="Taquilla..."
						pattern={'([0-9].){2}[A-Z].(G|P)[0-9]{3}'}
						required
						class="w-4/5 m-auto recompensa:bg-[#e0e0e0]"
					/>
				</div>
			</div>
			<div class="grid grid-cols-1 w-auto place-items-center">
				<Button
					type="submit"
					class="bg-dele-color text-white mt-8 px-8 py-2 text-xl hover:bg-dele-color dark:bg-dark-primary dark:hover:bg-dark-accent recompensa:bg-recompensa-primary hover:recompensa:bg-recompensa-accent"
					>Buscar</Button
				>
			</div>
		</form>
	</TabItem>
	<TabItem
		title="Tabla Pablo"
		class=""
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent recompensa:text-recompensa-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary recompensa:text-recompensa-primary hover:recompensa:text-white sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		{@const reservadas = TablaPabloItems.filter((item) => item.status === 'reservada').length}
		{@const ocupadas = TablaPabloItems.filter((item) => item.status === 'ocupada').length}
		{@const no_disponibles = TablaPabloItems.filter((item) => item.status === 'rota').length}
		{@const reservadas_s = count_reservas("P", TablaPabloItems.filter((item) => item.status === 'reservada'))}
		{@const reservadas_l = count_reservas("G", TablaPabloItems.filter((item) => item.status === 'reservada'))}
		{@const ocupadas_s = count_reservas("P", TablaPabloItems.filter((item) => item.status === 'ocupada'))}
		{@const ocupadas_l = count_reservas("G", TablaPabloItems.filter((item) => item.status === 'ocupada'))}

		<div class="grid grid-cols-3 place-items-center">
			<div class="text-center" id="pop_reservadas">
				<p class="text-dele-color dark:text-dark-primary recompensa:text-recompensa-primary">Reservadas</p>
				<p class="text-2xl dark:text-dark-accent recompensa:text-recompensa-accent">{reservadas}</p>
			</div>
			<div class="text-center" id="pop_ocupadas">
				<p class="text-dele-color dark:text-dark-primary recompensa:text-recompensa-primary">Ocupadas</p>
				<p class="text-2xl dark:text-dark-accent recompensa:text-recompensa-accent">{ocupadas}</p>
			</div>
			<div class="text-center">
				<p class="text-dele-color dark:text-dark-primary recompensa:text-recompensa-primary">No disponibles</p>
				<p class="text-2xl dark:text-dark-accent recompensa:text-recompensa-accent">{no_disponibles}</p>
			</div>
		</div>

		<Popover class="text-black dark:text-white dark:bg-dark-secondary md:w-1/4 sm:w-1/2 w-10/12 sm:text-md text-sm recompensa:bg-recompensa-secondary" title="Reservadas" triggeredBy="#pop_reservadas">
			<div class="grid grid-cols-2">
				<div class="text-dele-color dark:text-dark-primary text-center recompensa:text-recompensa-primary">Pequeñas<p class="text-black dark:text-white recompensa:text-white">{reservadas_s}</p></div>
				<div class="text-dele-color dark:text-dark-primary text-center recompensa:text-recompensa-primary">Grandes<p class="text-black dark:text-white recompensa:text-white">{reservadas_l}</p></div>
			</div>
		</Popover>

		<Popover class="text-black dark:text-white dark:bg-dark-secondary md:w-1/4 sm:w-1/2 w-10/12 sm:text-md text-sm recompensa:bg-recompensa-secondary" title="Ocupadas" triggeredBy="#pop_ocupadas">
			<div class="grid grid-cols-2 ">
				<div class="text-dele-color dark:text-dark-primary text-center recompensa:text-recompensa-primary">Pequeñas<p class="text-black dark:text-white recompensa:text-white">{ocupadas_s}</p></div>
				<div class="text-dele-color dark:text-dark-primary text-center recompensa:text-recompensa-primary">Grandes<p class="text-black dark:text-white recompensa:text-white">{ocupadas_l}</p></div>
			</div>
		</Popover>

		<TableSearch placeholder="Busca por Nombre" hoverable={true} bind:inputValue={searchTerm}>
			<TableHead>
				<TableHeadCell class="recompensa:bg-recompensa-primary recompensa:text-white">Nombre</TableHeadCell>
				<TableHeadCell class="recompensa:bg-recompensa-primary recompensa:text-white">Nia</TableHeadCell>
				<TableHeadCell class="grid grid-cols-2 recompensa:bg-recompensa-primary recompensa:text-white">
					<div class="cursor-pointer w-1/2 hover:bg-gray-400" on:click={() => change_sorting()}>Taquilla</div>
					{#if sorting}
						{#if sorting_dir}
							<button on:click={() => change_sorting_dir()} class="w-1/12">
								<CaretDownSolid/>
							</button>
						{:else}
							<button on:click={() => change_sorting_dir()} class="w-1/12">
								<CaretUpSolid/>
							</button>
						{/if}
					{/if}
				</TableHeadCell>
				<TableHeadCell class="recompensa:bg-recompensa-primary recompensa:text-white">Código</TableHeadCell>
				<TableHeadCell class="recompensa:bg-recompensa-primary recompensa:text-white">Fecha</TableHeadCell>
				<TableHeadCell class="recompensa:bg-recompensa-primary recompensa:text-white">Estado</TableHeadCell>
				<TableHeadCell class="recompensa:bg-recompensa-primary recompensa:text-white">Acciones</TableHeadCell>
			</TableHead>
			<TableBody tableBodyClass="divide-y">
				{#if sortedItems != null && sortedItems}
					{#each sortedItems as item}
						<TableBodyRow>
							<TableBodyCell class="select-all recompensa:bg-[#e0e0e0]">{item.nombre}</TableBodyCell>
							<TableBodyCell class="select-all recompensa:bg-[#e0e0e0]">{item.nia}</TableBodyCell>
							<TableBodyCell class="select-all recompensa:bg-[#e0e0e0]">{item.taquilla}</TableBodyCell>
							<TableBodyCell class="select-all recompensa:bg-[#e0e0e0]">{item.codigo}</TableBodyCell>
							<TableBodyCell class="select-all recompensa:bg-[#e0e0e0]">{item.date}</TableBodyCell>
							<TableBodyCell class="select-all recompensa:bg-[#e0e0e0]">{item.status.charAt(0).toUpperCase() + item.status.slice(1)}</TableBodyCell>
							<TableBodyCell class="recompensa:bg-[#e0e0e0]">
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
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent recompensa:text-recompensa-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary recompensa:text-recompensa-primary hover:recompensa:text-white sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		{@const reservadas = TablaPabloAsociacionesItems.filter((item) => item.status === 'reservada').length}
		{@const ocupadas = TablaPabloAsociacionesItems.filter((item) => item.status === 'ocupada').length}
		{@const no_disponibles = $page.data.tablaPablo.filter((item) => item.status === 'rota').length}
		{@const reservadas_s = count_reservas("P", TablaPabloAsociacionesItems.filter((item) => item.status === 'reservada'))}
		{@const reservadas_l = count_reservas("G", TablaPabloAsociacionesItems.filter((item) => item.status === 'reservada'))}
		{@const ocupadas_s = count_reservas("P", TablaPabloAsociacionesItems.filter((item) => item.status === 'ocupada'))}
		{@const ocupadas_l = count_reservas("G", TablaPabloAsociacionesItems.filter((item) => item.status === 'ocupada'))}

		<div class="grid grid-cols-3 place-items-center">
			<div class="text-center" id="pop_reservadas_a">
				<p class="text-dele-color dark:text-dark-primary recompensa:text-recompensa-primary">Reservadas</p>
				<p class="text-2xl dark:text-dark-accent recompensa:text-recompensa-accent">{reservadas}</p>
			</div>
			<div class="text-center" id="pop_ocupadas_a">
				<p class="text-dele-color dark:text-dark-primary recompensa:text-recompensa-primary">Ocupadas</p>
				<p class="text-2xl dark:text-dark-accent recompensa:text-recompensa-accent">{ocupadas}</p>
			</div>
			<div class="text-center">
				<p class="text-dele-color dark:text-dark-primary recompensa:text-recompensa-primary">No disponibles</p>
				<p class="text-2xl dark:text-dark-accent recompensa:text-recompensa-accent">{no_disponibles}</p>
			</div>
		</div>

		<Popover class="text-black dark:text-white dark:bg-dark-secondary md:w-1/4 sm:w-1/2 w-10/12 sm:text-md text-sm recompensa:bg-recompensa-secondary" title="Reservadas" triggeredBy="#pop_reservadas_a">
			<div class="grid grid-cols-2">
				<div class="text-dele-color dark:text-dark-primary text-center recompensa:text-recompensa-primary">Pequeñas<p class="text-black dark:text-white recompensa:text-white">{reservadas_s}</p></div>
				<div class="text-dele-color dark:text-dark-primary text-center recompensa:text-recompensa-primary">Grandes<p class="text-black dark:text-white recompensa:text-white">{reservadas_l}</p></div>
			</div>
		</Popover>

		<Popover class="text-black dark:text-white dark:bg-dark-secondary md:w-1/4 sm:w-1/2 w-10/12 sm:text-md text-sm recompensa:bg-recompensa-secondary" title="Ocupadas" triggeredBy="#pop_ocupadas_a">
			<div class="grid grid-cols-2 ">
				<div class="text-dele-color dark:text-dark-primary text-center recompensa:text-recompensa-primary">Pequeñas<p class="text-black dark:text-white recompensa:text-white">{ocupadas_s}</p></div>
				<div class="text-dele-color dark:text-dark-primary text-center recompensa:text-recompensa-primary">Grandes<p class="text-black dark:text-white recompensa:text-white">{ocupadas_l}</p></div>
			</div>
		</Popover>

		<TableSearch placeholder="Busca por Nombre" hoverable={true} bind:inputValue={searchTerm}>
				<TableHead>
					<TableHeadCell class="recompensa:bg-recompensa-primary text-white">Nombre</TableHeadCell>
					<TableHeadCell class="recompensa:bg-recompensa-primary text-white grid grid-cols-2">
						<div class="cursor-pointer w-1/2 hover:bg-gray-400" on:click={() => change_sorting_a()}>Taquilla</div>
						{#if sorting_a}
							{#if sorting_dir_a}
								<button on:click={() => change_sorting_dir_a()} class="w-1/12">
									<CaretDownSolid/>
								</button>
							{:else}
								<button on:click={() => change_sorting_dir_a()} class="w-1/12">
									<CaretUpSolid/>
								</button>
							{/if}
						{/if}
					</TableHeadCell>
					<TableHeadCell class="recompensa:bg-recompensa-primary text-white">Código</TableHeadCell>
					<TableHeadCell class="recompensa:bg-recompensa-primary text-white">Fecha</TableHeadCell>
					<TableHeadCell class="recompensa:bg-recompensa-primary text-white">Estado</TableHeadCell>
					<TableHeadCell class="recompensa:bg-recompensa-primary text-white">Acciones</TableHeadCell>
				</TableHead>
				<TableBody tableBodyClass="divide-y">
					{#if sortedItems_a != null && sortedItems_a}
						{#each sortedItems_a as item}
							<TableBodyRow>
								<TableBodyCell class="select-all recompensa:bg-[#e0e0e0]">{item.nombre}</TableBodyCell>
								<TableBodyCell class="select-all recompensa:bg-[#e0e0e0]">{item.taquilla}</TableBodyCell>
								<TableBodyCell class="select-all recompensa:bg-[#e0e0e0]">{item.codigo}</TableBodyCell>
								<TableBodyCell class="select-all recompensa:bg-[#e0e0e0]">{item.date}</TableBodyCell>
								<TableBodyCell class="select-all recompensa:bg-[#e0e0e0]">{item.status.charAt(0).toUpperCase() + item.status.slice(1)}</TableBodyCell>
								<TableBodyCell class="recompensa:bg-[#e0e0e0]">
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
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent recompensa:text-recompensa-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary recompensa:text-recompensa-primary hover:recompensa:text-white sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		<TableSearch placeholder="Busca por Taquilla" hoverable={true} bind:inputValue={searchTerm}>
			<TableHead>
				<TableHeadCell class="recompensa:bg-recompensa-primary recompensa:text-white">Taquilla</TableHeadCell>
				<TableHeadCell class="recompensa:bg-recompensa-primary recompensa:text-white">No disponible desde</TableHeadCell>
				<TableHeadCell class="recompensa:bg-recompensa-primary recompensa:text-white">Reparar</TableHeadCell>
			</TableHead>
			<TableBody tableBodyClass="divide-y">
				{#if taquillasRotas != null && taquillasRotas}
					{#each taquillasRotas as item}
						<TableBodyRow>
							<TableBodyCell class="recompensa:bg-[#e0e0e0]">{item.taquilla}</TableBodyCell>
							<TableBodyCell class="recompensa:bg-[#e0e0e0]">{item.date}</TableBodyCell>
							<TableBodyCell class="recompensa:bg-[#e0e0e0]">
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
			<Card class="mt-2 recompensa:bg-recompensa-secondary recompensa:border-recompensa-primary">
				<div class="flex place-content-between ">
					<h5 class="text-2xl font-medium underline text-dele-color dark:text-dark-primary recompensa:text-white">
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
						<p class="text-black text-sm mt-4 dark:text-white recompensa:text-white">
							Reservada por {taquilla['nombre']} (<b>{taquilla['nia']}</b>) el {taquilla['date'].split(' ')[0]} a las {taquilla[
								'date'
							].split(' ')[1]}
						</p>
					{:else}
						<p class="text-black text-sm mt-4 dark:text-white recompensa:text-white">
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

<Modal bind:open={formModalReservation} size="xs" autoclose={false} class="w-full recompensa:bg-recompensa-secondary">
	<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white recompensa:text-white">Reservar Taquilla</h3>
	<p class="dark:text-white recompensa:text-white">
		El precio de la taquilla es de
		{#if selectedTaquilla.includes('G')}<span class="font-bold"> 6€ </span>
		{:else}<span class="font-bold"> 4€ </span>
		{/if} el año completo y la mitad por el segundo cuatrimestre.
	</p>
	<Tabs defaultClass="flex flex-coll space-x-2 rtl:space-x-reverse overflow-x-auto">
		<TabItem
			open
			title="Estudiantes"
			class=""
			activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent recompensa:text-recompensa-accent"
			inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary recompensa:text-recompensa-primary hover:recompensa:text-white sm:text-base text-xs"
			>
			<form class="flex flex-col" action="?/registerTaquilla" method="post">
				<Label class="mb-4">
					<span class="recompensa:text-recompensa-primary">NIA:</span>
					<Input class="recompensa:bg-[#e0e0e0]" type="text" id="nia" name="nia" placeholder="100xxxxxx" required />
				</Label>
				<Label class="mb-4">
					<span class="recompensa:text-recompensa-primary">Taquilla</span>
					<Input class="recompensa:bg-[#e0e0e0]" type="text" id="taquilla" name="taquilla" value={selectedTaquilla} readonly required />
				</Label>
				<Label class="mb-4">
					<span class="recompensa:text-recompensa-primary">Nombre:</span>
					<Input class="recompensa:bg-[#e0e0e0]" type="text" id="nombre" name="nombre" required />
				</Label>
				
				<Button
					type="submit"
					class="w-full bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent recompensa:bg-recompensa-primary hover:recompensa:bg-recompensa-accent"
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
			activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent recompensa:text-recompensa-accent"
			inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary recompensa:text-recompensa-primary hover:recompensa:text-white sm:text-base text-xs"
		>
			<form class="flex flex-col" action="?/registerTaquillaAssociation" method="post" on:submit|preventDefault={handleFormSubmit}>
				<Label class="mb-4">
					<span class="recompensa:text-recompensa-primary">Taquilla</span>
					<Input class="recompensa:bg-[#e0e0e0]" type="text" id="taquilla" name="taquilla" value={selectedTaquilla} readonly required />
				</Label>
				<Input type="hidden" id="correo" name="correo" value={association_selected["correo"]} required />
				<Input type="hidden" id="nombre" name="nombre" value={association_selected["nombre"]} required />
				<Label class="mb-4">
					<Button class="w-full bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent recompensa:bg-recompensa-primary hover:recompensa:bg-recompensa-accent">
						Asociación: 
							{#if association_selected["nombre"]}
								{association_selected["nombre"]} 
							{:else}
								
							{/if}
							<ChevronDownOutline class="w-6 h-6 ms-2 text-white dark:text-white" />
					</Button>
					<Dropdown bind:open={openDropdown} class="recompensa:bg-recompensa-secondary">
						<div slot="header" class="px-4 py-2">
							<span class="block text-sm text-gray-900 dark:text-white">Selecciona una asociación</span>
						</div>
						{#each asociaciones as asociacion}
							<DropdownItem 
							class="rounded p-2 hover:bg-gray-100 dark:hover:bg-gray-600 recompensa:text-white hover:recompensa:bg-recompensa-accent"
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
					class="w-full bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent recompensa:bg-recompensa-primary hover:recompensa:bg-recompensa-accent"
					on:click={() => {
						show_results = false;
					}}>Reservar Taquilla</Button
				>
			</form>
		</TabItem>
	</Tabs>
	
</Modal>

<ModalIniciaSesion bind:openForm={openModalIniciaSesion}></ModalIniciaSesion>

<Modal bind:open={deleteModal} size="xs" autoclose={false} class="w-full recompensa:bg-recompensa-secondary">
	<form class="flex flex-col space-y-6">
		<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white recompensa:text-white">Eliminar Reserva</h3>
		<p class="dark:text-white recompensa:text-white">Vas a eliminar una reserva con los siguientes datos:</p>
		<Label class="space-y-2">
			<span class="recompensa:text-recompensa-primary">NIA:</span>
			<Input type="text" id="nia" name="nia" value={currentTaquilla['nia']} readonly required />
		</Label>
		<Label class="space-y-2">
			<span class="recompensa:text-recompensa-primary">Taquilla</span>
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
			class="w-full1 bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent recompensa:bg-recompensa-primary hover:recompensa:bg-recompensa-accent"
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
