<script lang="ts">
	/** @type {import('./$types').ActionData | any} */
	export let form: any;

	import { page } from '$app/stores';
	import { Tabs, TabItem, Input, Label, Button, Modal, Card } from 'flowbite-svelte';
	import { enhance } from '$app/forms';
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
	let session = $page.data.session;

	// Reactive statement to update session whenever $page.data.session changes
	$: session = $page.data.session;

	let successToast = false;
	let unSuccessToast = false;
	let searchTerm = '';
	let deleteModal;
	let completeModal;
	let currentReserva;
	let decompleteModal;
	let banModal;
	let unbanModal;

	const niaRegex = /^100[0-9]{6}$/;

	$: filteredItems = $page.data.tablaPabloOsciloscopios.filter((item) =>{
		return (item.status != "no_disponible" && item.nombre.toLowerCase().indexOf(searchTerm.toLowerCase()) !== -1);
	});

	$: bannedUsers = $page.data.bannedUsers;

	function change_delete_modal(reserva) {
		deleteModal = true;
		currentReserva = reserva;
	}

	async function eliminar_reserva() {
		// Call a function that only runs in the server side:
		let res_email = session?.user?.email || '';
		
		const response = await fetch('/api/eliminar_reserva_osciloscopio', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ puesto: currentReserva["puesto"], hora: currentReserva["hora"], fecha: currentReserva["fecha"], email: res_email })
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

	function change_complete_modal(reserva) {
		currentReserva = reserva;
		completeModal = true;
	}

	async function completar_reserva() {
		// Call a function that only runs in the server side:
		let res_email = session?.user?.email || '';
		
		const response = await fetch('/api/completar_reserva_osciloscopio', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ puesto: currentReserva["puesto"], hora: currentReserva["hora"], fecha: currentReserva["fecha"], email: res_email })
		});

		let result = await response.json();
		result = result['result']['message'];
		if (result.includes('completada')) {
			successToast = true;
			setTimeout(() => {
				successToast = false;
				location.reload();
			}, 1000);
		} else {
			unSuccessToast = true;
		}
	}

	function change_decomplete_modal(reserva) {
		currentReserva = reserva;
		decompleteModal = true;
	}

	async function descompletar_reserva() {
		// Call a function that only runs in the server side:
		let res_email = session?.user?.email || '';
		
		const response = await fetch('/api/descompletar_reserva_osciloscopio', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ puesto: currentReserva["puesto"], hora: currentReserva["hora"], fecha: currentReserva["fecha"], email: res_email })
		});

		let result = await response.json();
		result = result['result']['message'];
		if (result.includes('descompletada')) {
			successToast = true;
			setTimeout(() => {
				successToast = false;
				location.reload();
			}, 1000);
		} else {
			unSuccessToast = true;
		}
	}

	let currentBanNIA;
	let currentBanDays;
	function change_ban_modal() {
		currentBanNIA = document.getElementById('nia_ban').value;
		currentBanDays = document.getElementById('sancion_ban').value;
		if (niaRegex.test(currentBanNIA) && currentBanDays) {
			currentBanDays = Math.min(100, currentBanDays);
			banModal = true;
		}
	}

	async function ban_user() {
		// Call a function that only runs in the server side:
		let res_email = session?.user?.email || '';
		
		const response = await fetch('/api/ban_user', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ user: currentBanNIA, dias: currentBanDays, email: res_email })
		});

		let result = await response.json();
		result = result['result']['message'];
		if (result.includes('sancionado')) {
			successToast = true;
			banModal = false;
			setTimeout(() => {
				successToast = false;
				location.reload();
			}, 1000);
		} else {
			unSuccessToast = true;
		}
	}

	let unbanNIA;
	function change_unban_modal(nia) {
		unbanNIA = nia;
		unbanModal = true;
	}

	async function unban_user() {
		// Call a function that only runs in the server side:
		let res_email = session?.user?.email || '';
		
		const response = await fetch('/api/unban_user', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ user: unbanNIA, email: res_email })
		});

		let result = await response.json();
		result = result['result']['message'];
		if (result.includes('correctamente')) {
			successToast = true;
			unbanModal = false;
			setTimeout(() => {
				successToast = false;
				location.reload();
			}, 1000);
		} else {
			unSuccessToast = true;
		}
	}

</script>

<Modal bind:open={deleteModal} size="md" autoclose={false} class="w-full">
	<form class="flex flex-col space-y-6">
		<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white">Eliminar Reserva</h3>
		<p>Vas a eliminar una reserva con los siguientes datos:</p>
		<Label class="space-y-2">
			<span>NIA:</span>
			<Input type="text" id="nia" name="nia" value={currentReserva['nia']} readonly required />
		</Label>
		<Label class="space-y-2">
			<span>Puesto</span>
			<Input type="text" id="puesto" name="puesto" value={currentReserva['puesto']} readonly required/>
		</Label>
		<Label class="space-y-2">
			<span>Fecha</span>
			<Input type="text" id="fecha" name="fecha" value={currentReserva['fecha']} readonly required/>
		</Label>
		<Label class="space-y-2">
			<span>Franja Horaria</span>
			<Input type="text" id="hora" name="hora" value={(currentReserva['hora']) + ":00 - " + (currentReserva['hora'] + 2) + ":00"} readonly required/>
		</Label>
		<p class="font-bold text-xl text-center">Hazlo sólo en caso de error de la reserva</p>
		<Button
			type="submit"
			class="w-full1 bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent"
			on:click={(ev) => {
				ev.preventDefault();
				deleteModal = false;
				eliminar_reserva();
			}}>Eliminar Reserva</Button
		>
	</form>
</Modal>

<Modal bind:open={decompleteModal} size="md" autoclose={false} class="w-full">
	<form class="flex flex-col space-y-6">
		<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white">Descompletar Reserva</h3>
		<p>Vas a descompletar una reserva con los siguientes datos:</p>
		<Label class="space-y-2">
			<span>NIA:</span>
			<Input type="text" id="nia_d" name="nia_d" value={currentReserva['nia']} readonly required />
		</Label>
		<Label class="space-y-2">
			<span>Puesto</span>
			<Input type="text" id="puesto_d" name="puesto_d" value={currentReserva['puesto']} readonly required/>
		</Label>
		<Label class="space-y-2">
			<span>Fecha</span>
			<Input type="text" id="fecha_d" name="fecha_d" value={currentReserva['fecha']} readonly required/>
		</Label>
		<Label class="space-y-2">
			<span>Franja Horaria</span>
			<Input type="text" id="hora_d" name="hora_d" value={(currentReserva['hora']) + ":00 - " + (currentReserva['hora'] + 2) + ":00"} readonly required/>
		</Label>
		<p class="font-bold text-xl text-center">Hazlo sólo si has completado una reserva por error</p>
		<Button
			type="submit"
			class="w-full1 bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent"
			on:click={(ev) => {
				ev.preventDefault();
				decompleteModal = false;
				descompletar_reserva();
			}}>Descompletar Reserva</Button
		>
	</form>
</Modal>

<Modal bind:open={banModal} size="xs" autoclose={false} class="w-full">
	<form class="flex flex-col space-y-6">
		<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white">Sancionar Persona</h3>
		<p>Vas a sancionar a una persona con estos datos:</p>
		<Label class="space-y-2">
			<span>NIA:</span>
			<Input type="text" id="nia_b" name="nia_b" value={currentBanNIA} readonly required />
		</Label>
		<Label class="space-y-2">
			<span>Días de Sanción (máx 100):</span>
			<Input type="text" id="dias_b" name="dias_b" value={currentBanDays} readonly required/>
		</Label>
		<p class="font-bold text-xl text-center">Hazlo solo si la persona se merece la sanción (se borrarán sus reservas)</p>
		<Button
			type="submit"
			class="w-full1 bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent"
			on:click={(ev) => {
				ev.preventDefault();
				decompleteModal = false;
				ban_user();
			}}>Sancionar</Button
		>
	</form>
</Modal>

<Modal bind:open={unbanModal} size="xs" autoclose={false} class="w-full">
	<form class="flex flex-col space-y-6">
		<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white">Sancionar Persona</h3>
		<p>Vas a levantar la sanción de la persona con el NIA:</p>
		<Label class="space-y-2">
			<span>NIA:</span>
			<Input type="text" id="nia_ub" name="nia_ub" value={unbanNIA} readonly required />
		</Label>
		
		<p class="font-bold text-xl text-center">Hazlo sólo si te equivocaste al sancionar a la persona (no se recuperarán sus reservas) o si la fecha de fin ha vencido</p>
		<Button
			type="submit"
			class="w-full1 bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent"
			on:click={(ev) => {
				ev.preventDefault();
				unbanModal = false;
				unban_user();
			}}>Levantar la Sanción</Button
		>
	</form>
</Modal>

<h1 class="text-4xl text-center text-dele-color m-5 dark:bg-dark-background dark:text-dark-primary">
	Gestión de Puestos
</h1>
<Tabs tabStyle="underline" contentClass="p-4" class="px-8">
	<TabItem
		open
		title="Tabla Puestos de Eléctronica"
		class=""
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		<TableSearch placeholder="Busca por Nombre" hoverable={true} bind:inputValue={searchTerm}>
			<TableHead>
				<TableHeadCell>Nombre</TableHeadCell>
				<TableHeadCell>Nia</TableHeadCell>
				<TableHeadCell>Puesto</TableHeadCell>
				<TableHeadCell>Hora</TableHeadCell>
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
							<TableBodyCell>{item.puesto}</TableBodyCell>
							{#if item.hora != "La base está al"}
								<TableBodyCell>{item.hora}:00 - {item.hora + 2}:00</TableBodyCell>
							{:else}
								<TableBodyCell>{item.hora}</TableBodyCell>
							{/if}
							<TableBodyCell>{item.fecha}</TableBodyCell>
							<TableBodyCell>{item.status.charAt(0).toUpperCase() + item.status.slice(1)}</TableBodyCell>
							<TableBodyCell>
								<div class="grid grid-cols-1 xl:grid-cols-2">
									{#if item.status === "reservada"}
										<Button class="xl:w-[95%] w-full text-xs lg:text-md text-white bg-red-500 rounded p-1"
											on:click={() => {
												change_delete_modal(item);
											}}>
											Eliminar	
										</Button>
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
		title="Añadir Sanción"
		class=""
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
		>
		<form>
			<div class="grid grid-cols-1 w-auto">
				<div>
					<Label class="w-4/5 m-auto text-xl text-dele-color"><span>NIA:</span> </Label>
					<Input type="text" id="nia_ban" name="nia_ban" placeholder="100XXXXXX" pattern={'100[0-9]{6}'} class="w-4/5 m-auto" required />
				</div>
				<div>
					<Label class="w-4/5 m-auto text-xl text-dele-color"><span>Días de Sanción:</span></Label>
					<Input type="text" id="sancion_ban" name="sancion_ban" required class="w-4/5 m-auto"/>
				</div>
			</div>
			<div class="mt-8 grid grid-cols-1 w-auto place-items-center">
				<Button
					on:click={() => {change_ban_modal()}}
					class="bg-dele-color text-white px-8 py-2 text-xl hover:bg-dele-color dark:bg-dark-primary dark:hover:bg-dark-accent"
					>
					Aplicar
				</Button>
			</div>
		</form>
	</TabItem>
	<TabItem
		title="Blacklist"
		class=""
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		<TableSearch placeholder="Busca por Nombre" hoverable={true} bind:inputValue={searchTerm}>
			<TableHead>
				<TableHeadCell>Nombre</TableHeadCell>
				<TableHeadCell>Nia</TableHeadCell>
				<TableHeadCell>Fecha de Inicio</TableHeadCell>
				<TableHeadCell>Fecha de Final</TableHeadCell>
				<TableHeadCell>Acciones</TableHeadCell>
			</TableHead>
			<TableBody tableBodyClass="divide-y">
				{#if bannedUsers != null && bannedUsers}
					{#each bannedUsers as user}
						<TableBodyRow>
							<TableBodyCell>{user.nombre}</TableBodyCell>
							<TableBodyCell>{user.nia}</TableBodyCell>
							<TableBodyCell>{user.start}</TableBodyCell>
							<TableBodyCell>{user.end}</TableBodyCell>
							{#if user.nombre != "No se ha podido"}
								<TableBodyCell>
									<Button class="xl:w-[95%] w-full text-xs lg:text-md text-white bg-red-500 rounded p-1"
										on:click={() => {
											change_unban_modal(user.nia);
										}}>
										Eliminar	
									</Button>
								</TableBodyCell>
							{/if}
						</TableBodyRow>
					{/each}
				{/if}
			</TableBody>
		</TableSearch>
	</TabItem>
</Tabs>

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