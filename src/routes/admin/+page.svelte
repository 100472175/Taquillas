<script lang="ts">
	import type { PageData } from './$types';
	import { Tabs, TabItem, Input, Label, Button, Select, Modal, Card, TableSearch, TableHead, TableHeadCell, TableBody, TableBodyRow, TableBodyCell, Popover, Indicator } from 'flowbite-svelte';
	import { QuestionCircleSolid} from 'flowbite-svelte-icons';
	import { enhance } from '$app/forms';
	import { page } from '$app/stores';
	import { Datepicker, themes } from 'svelte-calendar';
	import dayjs from 'dayjs';

	// Users' rols
	const rols = [
		{ value: 'escuela', name: 'Escuela' },
		{ value: 'atencion', name: 'Atención' },
		{ value: 'general', name: 'General' }
	];

	const puestos = [
		{ value: 1, name: "Puesto 1"},
		{ value: 2, name: "Puesto 2"},
		{ value: 3, name: "Puesto 3"}
	];

	const estados = [
		{ value: 0, name: "No Disponible"},
		{ value: 1, name: "Disponible"}
	];

	// Días
	const days = [
		{ name: "Lunes", 		value: 1},
		{ name: "Martes",		value: 2}, 
		{ name: "Miércoles",	value: 3},  
		{ name: "Jueves", 		value: 4},
		{ name: "Viernes", 		value: 5},
	];

	const franjas = [9, 11, 15, 17];

	// Calendar
	const theme = {
		calendar: {
			width: '38vw',
			shadow: '5px 5px 5px rgba(0, 0, 0, 0.25)',
			colors: {
				background: {
					hover: "#FF6D2E",
					highlight: '#3BC4A0',
				}
			},
			grid: {
				"border-radius": '30px',
				"border": "1px black solid",
			},
		}
	};

	// Calendar mobile
	const theme_mobile = {
		calendar: {
			width: '80vw',
			shadow: '0px 0px 5px rgba(0, 0, 0, 0.25)',
			colors: {
				background: {
					highlight: '#3BC4A0'
				}
			}

		}
	};

	export let data;
	let openConfirmation = false;
	let puestoModal = false;
	let successToast = false;
	let unSuccessToast = false;
	let successChangeToast = false;
	let unSuccessChangeToast = false;
	let successBackupToast = false;
	let unSuccessBackupToast = false;
	let unSuccessAvailabilityToast = false;
	let successToastPlantilla = false;
	let unSuccessToastPlantilla = false;
	$: session = $page.data.session;
	let store;
	let plantilla = $page.data.plantilla;
	
	let users = $page.data.users;
	let searchTerm = '';
	$: filteredItems = users.filter((person) =>{
		return (person.rango != "general" && person.nombre.toLowerCase().indexOf(searchTerm.toLowerCase()) !== -1);
	});

	function change_confirmation_modal() {
		openConfirmation = true;
	}

	async function do_backup() {
		
		// Call a function that only runs in the server side:
		let res_email = session?.user?.email || '';
		if (res_email === '') {
			openConfirmation = false;
			return;
		}
		const response = await fetch('/api/backupDB', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ email: res_email })
		});

		let result = await response.json();
		result = result['result']['message'];
		if (result.includes('correctamente')) {
			successBackupToast = true;
			setTimeout(() => {
				successBackupToast = false;
				location.reload();
			}, 2000);
		} else {
			unSuccessBackupToast = true;
		}
	}

	async function eliminar_db() {
		openConfirmation = false;

		// Call a function that only runs in the server side:
		let res_email = session?.user?.email || '';
		if (res_email === '') {
			openConfirmation = false;
			return;
		}
		const response = await fetch('/api/deleteDB', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ email: res_email })
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

	let puestoOsciloscopio;
	let stateOsciloscopio;
	let nameStateOsciloscopio;
	function change_osciloscopio_modal() {
		puestoOsciloscopio = document.getElementById('puesto').value;
		stateOsciloscopio = document.getElementById('estado_puesto').value;
		if (stateOsciloscopio == 1) {
			nameStateOsciloscopio = 'Disponible'
		}
		else {
			nameStateOsciloscopio = 'No Disponible'
		}
		if (puestoOsciloscopio && stateOsciloscopio) {
			puestoModal = true;
		}
	}

	async function change_osciloscopio_state() {
		puestoModal = false;

		// Call a function that only runs in the server side:
		let res_email = session?.user?.email || '';
		if (res_email === '') {
			puestoModal = false;
			return;
		}
		const response = await fetch('/api/change_osciloscopio_state', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ email: res_email, puesto: puestoOsciloscopio, estado: stateOsciloscopio })
		});

		let result = await response.json();
		result = result['result']['message'];
		if (result.includes('cambiado')) {
			successChangeToast = true;
			setTimeout(() => {
				successChangeToast = false;
				location.reload();
			}, 1000);
		} else {
			unSuccessChangeToast = true;
		}
	}

	let availabilityModal;
	let fechaDisponibilidad;
	let horaDisponibilidad;
	let estadoDisponibilidad;

	function change_availability_modal(dia, hora, estado) {
		fechaDisponibilidad = dia;
		horaDisponibilidad = hora;
		estadoDisponibilidad = estado;
		availabilityModal = true;
	}

	async function change_disponibilidad_hora() {
		availabilityModal = false;

		// Call a function that only runs in the server side:
		let res_email = session?.user?.email || '';
		if (res_email === '') {
			availabilityModal = false;
			return;
		}
		const response = await fetch('/api/change_hora_state', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ email: res_email, dia: fechaDisponibilidad, hora: horaDisponibilidad, estado: estadoDisponibilidad })
		});

		let result = await response.json();
		result = result['result']['message'];
		if (result.includes('cambiado')) {
			setTimeout(() => {
				location.reload();
			}, 500);
		} else {
			unSuccessAvailabilityToast = true;
			setTimeout(() => {
				unSuccessAvailabilityToast = false;
			}, 1000);
		}
	}

	export let form;

	async function change_plantilla(dia, hora, estado) {
		let res_email = session?.user?.email || '';
		if (res_email === '') {
			availabilityModal = false;
			return;
		}
		const response = await fetch('/api/change_plantilla', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ email: res_email, dia: dia, hora: hora, estado: estado })
		});

		let result = await response.json();
		result = result['result']['message'];
		if (result.includes('correctamente')) {
			successToastPlantilla = true;
			setTimeout(() => {
				successToast = false;
				location.reload();
			}, 1500);
		} else {
			unSuccessToastPlantilla = true;
		}
	}
	
</script>

<Tabs tabStyle="underline" contentClass="p-4" class="px-8">
	<TabItem
		open
		title="Cambiar Rol"
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		<div class="w-auto grid grid-cols-1 place-items-center mb-4">
			<Button id="pop_change_rol" class="dark:text-dark-primary dark:hover:text-dark-accent text-dele-color hover:text-dele-accent">
				<QuestionCircleSolid class="md:h-8 md:w-8 h-10 w-10"/>
			</Button>
		</div>
		
		<Popover class="text-black dark:text-white dark:bg-dark-secondary md:w-1/3 sm:w-1/2 w-10/12 sm:text-md text-sm" title="Cambiar rol" triggeredBy="#pop_change_rol">
			<p class=" dark:text-white text-sm sm:text-base text-justify">
				Este tab sirve para cambiar el rol de un usuario que ya se haya registrado en el sistema<br><br>
				Para cambiar el rol de esa persona, simplemente introduce su NIA y selecciona el nuevo rol que debe tener.
			</p>
		</Popover >
		<form action="?/addUserRol" method="post" use:enhance>
			<div class="grid grid-cols-1 w-auto">
				<div>
					<Label class="w-4/5 text-xl m-auto text-dele-color">NIA</Label>
					<Input
						type="text"
						id="NIA_add"
						name="NIA_add"
						placeholder="NIA del usuario..."
						pattern={'100[0-9]{6}'}
						required
						class="w-4/5 m-auto"
					/>
				</div>
			</div>
			<div class="grid grid-cols-1 w-auto mt-4 place-items-center">
				<Label class="text-xl w-auto text-dele-color">Selecciona un rol</Label>
				<Select
					class="mt-2 sm:w-1/5 w-2/5"
					id="rol_add"
					name="rol_add"
					items={rols}
					required
					placeholder="Rol"
				/>
			</div>
			<Input
				type="hidden"
				id="nia_admin"
				name="nia_admin"
				value={data.session?.user?.email?.split('@')[0]}
			/>

			<Input type="hidden" id="nombre_admin" name="nombre_admin" value={data.session?.user?.name} />
			<div class="grid grid-cols-1 w-auto place-items-center">
				<Button
					type="submit"
					class="bg-dele-color text-white mt-8 px-8 py-2 text-xl hover:bg-dele-color dark:bg-dark-primary dark:hover:bg-dark-accent"
					>Cambiar rol</Button
				>
				<div></div>
			</div>
		</form>
	</TabItem>
	<TabItem
		title="Roles Usuarios"
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		<div class="w-auto grid grid-cols-1 place-items-center mb-4">
			<Button id="pop_table" class="dark:text-dark-primary dark:hover:text-dark-accent text-dele-color hover:text-dele-accent">
				<QuestionCircleSolid class="md:h-8 md:w-8 h-10 w-10"/>
			</Button>
		</div>
		
		<Popover class="text-black dark:text-white dark:bg-dark-secondary md:w-1/3 sm:w-1/2 w-10/12 sm:text-md text-sm" title="Cambiar rol" triggeredBy="#pop_table">
			<p class=" dark:text-white text-sm sm:text-base text-justify">
				Esta página muestra a todas las personas que tengan un rol de atención o de escuela.
			</p>
		</Popover >
		<TableSearch placeholder="Busca por Nombre" hoverable={true} bind:inputValue={searchTerm}>
			<TableHead>
				<TableHeadCell>Nombre</TableHeadCell>
				<TableHeadCell>Nia</TableHeadCell>
				<TableHeadCell>Correo</TableHeadCell>
				<TableHeadCell>Rango</TableHeadCell>
			</TableHead>
			<TableBody tableBodyClass="divide-y">
				{#if filteredItems != null && filteredItems}
					{#each filteredItems as item}
						<TableBodyRow>
							<TableBodyCell>{item.nombre}</TableBodyCell>
							<TableBodyCell>{item.nia}</TableBodyCell>
							<TableBodyCell>{item.correo}</TableBodyCell>
							<TableBodyCell>{item.rango.charAt(0).toUpperCase() + item.rango.slice(1)}</TableBodyCell>
						</TableBodyRow>
					{/each}
				{/if}
			</TableBody>
		</TableSearch>
	</TabItem>
	<TabItem
		title="Base de Datos"
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		<h2 class="text-primary dark:text-gray-300 text-center text-4xl font-montserrat">
			Administrar la Base de Datos
		</h2>

		<div class="w-auto grid grid-cols-1 place-items-center mb-4">
			<Button id="pop_db" class="dark:text-dark-primary dark:hover:text-dark-accent text-dele-color hover:text-dele-accent">
				<QuestionCircleSolid class="md:h-8 md:w-8 h-10 w-10"/>
			</Button>
		</div>
		
		<Popover class="text-black dark:text-white dark:bg-dark-secondary md:w-1/3 sm:w-1/2 w-10/12 sm:text-md text-sm" title="Base de Datos" triggeredBy="#pop_db">
			<p class=" dark:text-white text-sm sm:text-base text-justify">
				Esta página sirve para hacer copias de seguridad y para eliminar la base de datos.<br><br>
				Antes de eliminar la base de datos se realiza una copia de seguridad, pero no la borres a no ser que tengas que hacerlo.
				Como nota adicional, la eliminación de la base de datos solo borra las reservas y deja a los usuarios intactos. 
			</p>
		</Popover >
		<section class="grid grid-rows-3 place-items-center mt-8">
			<section>
				<form method="post" use:enhance>
					<Input
						type="hidden"
						required
						id="email_admin"
						name="email_admin"
						value={session?.user?.email}
					/>
					<Button
						type="button"
						class="w-full1 bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent"
						on:click={() => {
							do_backup();
						}}
					>
						Hacer una copia de seguridad</Button
					>
				</form>
			</section>
			<section>
				<form method="post" use:enhance class="mt-8">
					<Input
						type="hidden"
						required
						id="email_admin"
						name="email_admin"
						value={session?.user?.email}
					/>
					<Button
						class="w-full1 bg-red-500 hover:bg-dele-accent dark:bg-red-500 dark:hover:bg-dark-accent"
						on:click={() => {
							change_confirmation_modal();
						}}
					>
						Eliminar la base de datos</Button
					>
				</form>
			</section>

			<section class="hidden">
				<form action="?/RestoreDB2" method="POST" enctype="multipart/form-data" class="mt-8">
					<Label class="text-xl w-auto text-dele-color"
						>Selecciona el archivo de la base de datos</Label
					>
					<Input
						type="file"
						id="file"
						name="file"
						accept=".db3"
						required
						class="w-4/5 m-auto my-4"
						enctype="multipart/form-data"
					/>

					<Input type="hidden" id="nia_admin" name="nia_admin" value={data.session?.user?.email} />
					<Button
						type="submit"
						class="w-full1 bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent"
					>
						Restaurar la copia de seguridad del archivo subido</Button
					>
				</form>
			</section>
		</section>
	</TabItem>
	<TabItem
		title="Gestionar Puestos"
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		<h2 class="text-primary dark:text-gray-300 text-center text-4xl font-montserrat">
			Gestionar Puestos
		</h2>

		<div class="w-auto grid grid-cols-1 place-items-center mb-4">
			<Button id="pop_db" class="dark:text-dark-primary dark:hover:text-dark-accent text-dele-color hover:text-dele-accent">
				<QuestionCircleSolid class="md:h-8 md:w-8 h-10 w-10"/>
			</Button>
		</div>
		
		<Popover class="text-black dark:text-white dark:bg-dark-secondary md:w-1/3 sm:w-1/2 w-10/12 sm:text-md text-sm" title="Gestionar Puestos" triggeredBy="#pop_db">
			<p class=" dark:text-white text-sm sm:text-base text-justify">
				Esta página sirve para marcar la disponibilidad de los puestos.<br><br>
				Antes de marcarlo como no disponible ten en cuenta que se mandarán correos a todas las personas afectadas. 
			</p>
		</Popover >
		<section class="grid grid-rows-3 place-items-center mt-8">
			<form method="post" use:enhance>
				<div class="grid grid-cols-1 w-screen">
					<div class="w-4/5 m-auto">
						<Label class="w-4/5 text-xl m-auto text-dele-color">Puesto de Electrónica</Label>
						<Select
							class="mt-2 w-4/5 m-auto"
							id="puesto"
							name="puesto"
							items={puestos}
							required
							placeholder="Puesto:"
						/>
					</div>
					<div class="w-4/5 m-auto">
						<Label class="w-4/5 text-xl m-auto text-dele-color">Estado</Label>
						<Select
							class="mt-2 w-4/5 m-auto"
							id="estado_puesto"
							name="estado_puesto"
							items={estados}
							required
							placeholder="Estado:"
						/>
					</div>
					<Button
						type="button"
						class="w-1/6 m-auto mt-8 text-xl bg-dele-color hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent"
						on:click={() => {
							change_osciloscopio_modal();
						}}
					>
						Cambiar estado</Button
					>
				</div>
			</form>
		</section>
	</TabItem>
	<TabItem
		title="Plantilla de Turnos"
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		<h2 class="text-primary dark:text-gray-300 text-center text-4xl font-montserrat">
			Plantilla de Turnos
		</h2>
		<table
		style="border: 2px solid black; border-radius: 13px; border-spacing: 0;"
		class="m-auto mt-12"
	>
			<thead>
				<tr>
					{#each days as day}
						<th
							style="border: 1px solid black; "
							class="text-center px-3 py-1 border-collapse bg-[#c6c6c6ff]"
							>
							{day["name"]}
						</th>
					{/each}
				</tr>
			</thead>
			<tbody>
				{#if plantilla && plantilla["plantilla"]}
					{#each franjas as start_hour}
						<tr>
							{#each days as day}
								{#if plantilla["plantilla"][day["value"] + "-" + start_hour] == 0}
									<td 
										style="border: 1px solid black;"
										class="bg-black text-white text-center p-3 cursor-pointer"
										on:click={()=> {change_plantilla(day["value"], start_hour, 1);}}
										>
										{start_hour}:00 - {start_hour + 2}:00
									</td>
								{:else}
									<td 
										style="border: 1px solid black;"
										class="bg-green-500 text-black text-center p-3 cursor-pointer"
										on:click={()=> {change_plantilla(day["value"], start_hour, 0);}}
										>
										{start_hour}:00 - {start_hour + 2}:00
									</td>
								{/if}
							{/each}
						</tr>
					{/each}
				{/if}
			</tbody>
		</table>
	</TabItem>
	<TabItem
		title="Turnos de Despacho"
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary sm:text-base text-xs"
		on:focus={() => {
			form = '';
		}}
	>
		<h2 class="text-primary dark:text-gray-300 text-center text-4xl font-montserrat">
			Turnos del Despacho
		</h2>
		<div class="grid grid-cols-1 place-items-center mt-6">
			{#if window.innerWidth <= 768}
				<Datepicker bind:store format='dddd - DD/MM/YYYY' startOfWeekIndex={1} start={new Date()} {theme_mobile}/>
			{:else}
				<Datepicker bind:store format='dddd - DD/MM/YYYY' startOfWeekIndex={1} start={new Date()} {theme}/>
			{/if}
		</div>
		<form action="?/ReservasDia" method="post" use:enhance>
			<div class="grid grid-cols-1 place-items-center mt-6">
				<Input
					type="hidden"
					required
					id="dia_r"
					name="dia_r"
					value={dayjs($store?.selected).format('D-M-YYYY')}
				/>
				<Button
					class="bg-dele-color text-white mt-8 px-8 py-2 text-xl hover:bg-dele-color dark:bg-dark-primary dark:hover:bg-dark-accent"
					type="submit"
					>
					Buscar
				</Button>
			</div>
		</form>
		{#if form != null && form && form.reservas}
			<div class="grid grid-cols-1 place-self-center mt-6">
				<div class="w-auto m-auto dark:text-white grid sm:grid-cols-4 grid-cols-2">
					<span class="flex items-center"
						><Indicator size="lg" color="green" class="me-1.5" />Libre</span
					>
					<span class="flex items-center"
						><Indicator size="lg" color="red" class="me-1.5" />Ocupada</span
					>
					<span class="flex items-center"
						><Indicator size="lg" color="dark" class="me-1.5" />No Disponible</span
					>
					<span class="flex items-center"
						><Indicator size="lg" color="dark" class="me-1.5" />(P) No Disponible en Plantilla</span
					>
				</div>
			</div>
			<table
				style="border: 2px solid black; border-radius: 13px; border-spacing: 0; "
				class="m-auto mt-6"
			>
				<tbody>
					<tr>
						{#if plantilla && plantilla["plantilla"]}
							{#each franjas as start_hour}
								{#if plantilla["plantilla"][(dayjs($store?.selected).format('d')) + "-" + start_hour] != 0}
									{#if form.reservas[(dayjs($store?.selected).format('D/M/YYYY')) + "-" + start_hour]}
										{#if form.reservas[(dayjs($store?.selected).format('D/M/YYYY')) + "-" + start_hour] == 'no_disponible'}
											<td 
												style="border: 1px solid black;"
												class="bg-black text-white text-center p-3 cursor-pointer"
												on:click={()=> {change_availability_modal(dayjs($store?.selected).format('D/M/YYYY'), start_hour, 'disponible');}}
												>
												
												{start_hour}:00 - {start_hour + 2}:00
											</td>
										{:else}
											<td 
												style="border: 1px solid black;"
												class="bg-red-500 text-center p-3 cursor-pointer"
												on:click={()=> {change_availability_modal(dayjs($store?.selected).format('D/M/YYYY'), start_hour, 'no_disponible');}}
												>
												
												{start_hour}:00 - {start_hour + 2}:00
											</td>
										{/if}
									{:else}
										<td 
											style="border: 1px solid black;"
											class="bg-green-500 text-center p-3 cursor-pointer"
											on:click={()=> {change_availability_modal(dayjs($store?.selected).format('D/M/YYYY'), start_hour, 'no_disponible');}}
											>
											
											{start_hour}:00 - {start_hour + 2}:00
										</td>
									{/if}
								{:else}
									<td 
										style="border: 1px solid black;"
										class="bg-black text-white text-center p-3 cursor-pointer">
										
										{start_hour}:00 - {start_hour + 2}:00 (P)
									</td>	
								{/if}
							{/each}
						{/if}
					</tr>
				</tbody>
			</table>
		{/if}
	</TabItem>
</Tabs>

<Modal bind:open={openConfirmation} size="xs" autoclose={false} class="w-full">
	<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white">Eliminar la base de datos</h3>
	<p class="text-black dark:text-white">
		Antes de eliminar la base de datos, se te mandará un correo con una copia de seguridad. Ten en cuenta que este borrado <b>solo</b> afecta a las reservas,
		no a los usuarios.
		<br><br>
		Haz click en el siguiente botón para confirmar el borrado.
	</p>
	<div class="grid grid-cols-1 place-items-center">
		<Button
			type="button"
			class="w-full bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent"
			on:click={() => {
				eliminar_db();
			}}
		>
			Borrar la Base de Datos
		</Button>
	</div>
</Modal>

<Modal bind:open={puestoModal} size="xs" autoclose={false} class="w-full">
	<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white">Eliminar la base de datos</h3>
	<p class="text-black dark:text-white">
		Antes de cambiar el estado del puesto, ten en cuenta que si lo marcas como no disponible se eliminarán las reservas.
	</p>

	<form class="flex flex-col space-y-6">
		<Label class="space-y-2">
			<span>Puesto</span>
			<Input type="text" id="puesto_modal" name="puesto_modal" value={puestoOsciloscopio} readonly required/>
		</Label>
		<Label class="space-y-2">
			<span>Estado</span>
			<Input type="text" id="estado_modal" name="estado_modal" value={nameStateOsciloscopio} readonly required/>
		</Label>
		<p class="font-bold text-xl text-center">Haz click en el siguiente botón para confirmar el cambio</p>
		<Button
			type="button"
			class="w-full bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent"
			on:click={() => {
				change_osciloscopio_state();
			}}
		>
			Cambiar el Estado del Puesto
		</Button>
	</form>

</Modal>

<Modal bind:open={availabilityModal} size="xs" autoclose={false} class="w-full">
	<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white">Cambiar la disponibilidad</h3>
	<p class="text-black dark:text-white">
		Vas a cambiar la disponibilidad de todos los puestos a la siguiente hora y fecha:
	</p>
	<form class="flex flex-col space-y-6">
		<Input type="text" id="fecha_disponibilidad" name="fecha_disponibilidad" value={fechaDisponibilidad} readonly required/>
		<Input type="text" id="hora_disponibilidad" name="hora_disponibilidad" value={(horaDisponibilidad + ":00 - " + (horaDisponibilidad + 2) + ":00")} readonly required/>
		<p class="font-bold text-xl text-center">Vas a cambiarlo al siguiente estado:</p>
		<Input type="text" id="estado_disponibilidad" name="estado_disponibilidad" value={estadoDisponibilidad} readonly required/>
		<p class="font-bold text-xl text-center">¿Quieres cambiarlo?</p>
		<Button
			type="button"
			class="w-full bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent"
			on:click={() => {
				change_disponibilidad_hora();
			}}
		>
			Cambiar el Estado
		</Button>
	</form>
</Modal>

{#if successBackupToast}
	<div class="fixed bottom-0 right-0 m-5">
		<Card class="bg-green-500 dark:text-white text-white dark:bg-green-500">
			<p class="p-2">Se ha realizado con éxito el Backup.</p>
		</Card>
	</div>
{:else if unSuccessBackupToast}
	<div class="fixed bottom-0 right-0 m-5">
		<Card class="bg-red-500 dark:text-white text-white dark:bg-red-500">
			<p class="p-2">No se ha podido realizar el Backup.</p>
		</Card>
	</div>
{/if}

{#if successToast}
	<div class="fixed bottom-0 right-0 m-5">
		<Card class="bg-green-500 dark:text-white text-white dark:bg-green-500">
			<p class="p-2">Base de datos borrada con éxito.</p>
		</Card>
	</div>
{:else if unSuccessToast}
	<div class="fixed bottom-0 right-0 m-5">
		<Card class="bg-red-500 dark:text-white text-white dark:bg-red-500">
			<p class="p-2">No se ha podido borrar la base de datos.</p>
		</Card>
	</div>
{/if}

{#if successChangeToast}
	<div class="fixed bottom-0 right-0 m-5">
		<Card class="bg-green-500 dark:text-white text-white dark:bg-green-500">
			<p class="p-2">Estado del puesto cambiado.</p>
		</Card>
	</div>
{:else if unSuccessChangeToast}
	<div class="fixed bottom-0 right-0 m-5">
		<Card class="bg-red-500 dark:text-white text-white dark:bg-red-500">
			<p class="p-2">No se ha podido cambiar el estado del puesto.</p>
		</Card>
	</div>
{/if}

{#if unSuccessAvailabilityToast}
	<div class="fixed bottom-0 right-0 m-5">
		<Card class="bg-red-500 dark:text-white text-white dark:bg-red-500">
			<p class="p-2">No se ha podido cambiar el estado de la hora</p>
		</Card>
	</div>
{/if}


{#if successToastPlantilla}
	<div class="fixed bottom-0 right-0 m-5">
		<Card class="bg-green-500 dark:text-white text-white dark:bg-green-500">
			<p class="p-2">Estado de la plantilla cambiado</p>
		</Card>
	</div>
{:else if unSuccessToastPlantilla}
	<div class="fixed bottom-0 right-0 m-5">
		<Card class="bg-red-500 dark:text-white text-white dark:bg-red-500">
			<p class="p-2">No se ha podido cambiar el estado de la plantilla</p>
		</Card>
	</div>
{/if}

