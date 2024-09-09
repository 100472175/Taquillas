<script lang="ts">
	import type { PageData } from './$types';
	import { Tabs, TabItem, Input, Label, Button, Select, Modal, Card, TableSearch, TableHead, TableHeadCell, TableBody, TableBodyRow, TableBodyCell, Popover } from 'flowbite-svelte';
	import { QuestionCircleSolid} from 'flowbite-svelte-icons';
	import { enhance } from '$app/forms';
	import { page } from '$app/stores';

	// Users' rols
	const rols = [
		{ value: 'escuela', name: 'Escuela' },
		{ value: 'atencion', name: 'Atención' },
		{ value: 'general', name: 'General' }
	];

	export let data;
	let openConfirmation = false;
	let successToast = false;
	let unSuccessToast = false;
	let successBackupToast = false;
	let unSuccessBackupToast = false;
	$: session = $page.data.session;
	
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
</script>

<Tabs tabStyle="underline" contentClass="p-4" class="px-8">
	<TabItem
		open
		title="Cambiar Rol"
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary sm:text-base text-xs"
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
