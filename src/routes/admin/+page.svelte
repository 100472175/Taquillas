<script lang="ts">
	import type { PageData } from './$types';
	import { Tabs, TabItem, Input, Label, Button, Select, Modal, Card } from 'flowbite-svelte';
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
	$: session = $page.data.session;


	setTimeout(() => {
		console.log(session?.user?.email);
	}, 1000);

	function change_confirmation_modal() {
		openConfirmation = true;
	}

	async function eliminar_db() {
		openConfirmation = true;

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
		class="hover:text-[#3BC4A0] dark:hover:text-dark-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-[#3BC4A0] p-4 dark:hover:text-dark-accent"
	>
		<form action="?/addUserRol" method="post" use:enhance>
			<div class="grid grid-cols-1 w-auto">
				<div>
					<Label class="w-4/5 text-xl m-auto text-[#3BC4A0]">NIA</Label>
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
				<Label class="text-xl w-auto text-[#3BC4A0]">Selecciona un rol</Label>
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
					class="bg-[#3BC4A0] text-white mt-8 px-8 py-2 text-xl hover:bg-[#3BB4A0] dark:bg-dark-primary dark:hover:bg-dark-accent"
					>Cambiar rol</Button
				>
				<div></div>
			</div>
		</form>
	</TabItem>
	<TabItem
		open
		title="Base de Datos"
		class="hover:text-[#3BC4A0] dark:hover:text-dark-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-[#3BC4A0] p-4 dark:hover:text-dark-accent"
	>
		<h2 class="text-primary dark:text-gray-300 text-center text-4xl font-montserrat">
			Administrar la Base de Datos
		</h2>
		<section class="grid grid-rows-3 place-items-center mt-8">
			<section>
				<form action="?/BackupDB" method="post" use:enhance>
					<Input
						type="hidden"
						required
						id="email_admin"
						name="email_admin"
						value={session?.user?.email}
					/>
					<Button
						type="submit"
						class="w-full1 bg-green-500 hover:bg-[#FF6D2E] dark:bg-dark-primary dark:hover:bg-dark-accent"
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
						class="w-full1 bg-red-500 hover:bg-[#FF6D2E] dark:bg-red-500 dark:hover:bg-dark-accent"
						on:click={() => {change_confirmation_modal();}}
					>
						Eliminar la base de datos</Button
					>
				</form>
			</section>

			<section class="hidden">
				<form action="?/RestoreDB2" method="POST" enctype="multipart/form-data" class="mt-8">
					<Label class="text-xl w-auto text-[#3BC4A0]"
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
						class="w-full1 bg-green-500 hover:bg-[#FF6D2E] dark:bg-dark-primary dark:hover:bg-dark-accent"
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
	<p>Antes de eliminar la base de datos, se te mandará un correo con una copia de seguridad. Haz click en el siguiente botón para confirmar el borrado.</p>
	<div class="grid grid-cols-1 place-items-center">
		<Button
			type="button"
			class="w-full1 bg-green-500 hover:bg-[#FF6D2E] dark:bg-dark-primary dark:hover:bg-dark-accent"
			on:click={() => {
				eliminar_db();
			}}
		>
			Borrar la Base de Datos
		</Button>
	</div>
</Modal>

{#if successToast}
	<div class="fixed bottom-0 right-0 m-5">
		<Card class="bg-green-500 text-white">
			<p class="p-2">Base de datos borrada con éxito.</p>
		</Card>
	</div>
{:else if unSuccessToast}
	<div class="fixed bottom-0 right-0 m-5">
		<Card class="bg-red-500 text-white">
			<p class="p-2">No se ha podido borrar la base de datos.</p>
		</Card>
	</div>
{/if}
