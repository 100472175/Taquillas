<script lang="ts">
	import { enhance } from '$app/forms';
	import { page } from '$app/stores';
	import { Tabs, TabItem, Input, Label, Button, Select, Toast } from 'flowbite-svelte';
	let session;

	// Reactive statement to update session whenever $page.data.session changes
	$: session = $page.data.session;

	/** @type {import('./$types').ActionData} */
	export let form;

	// Users' rols
	const rols = [
		{ value: 'escuela', name: 'Escuela' },
		{ value: 'atencion', name: 'Atención' }
	];

	// add_user interface
	let NIA_add: String;
	let rol_add: String;

	function add_user() {
		let email: String = NIA_add + '@alumnos.uc3m.es';
		alert('El usuario ' + email + ' tiene el rol ' + rol_add);
	}

	// delete_user interface
	let NIA_del: String;

	function delete_user() {
		let email = NIA_del + '@alumnos.uc3m.es';
		alert(email + ' eliminado');
	}
</script>

<h1 class="text-4xl text-center text-[#3BC4A0] m-5">Gestión de usuarios</h1>
<Tabs tabStyle="underline" contentClass="p-4 bg-white">
	<TabItem
		open
		title="Añadir Rol"
		class="hover:text-[#3BC4A0]"
		inactiveClasses="text-gray-500 hover:text-[#3BC4A0] p-4 sm:text-base text-xs"
	>
		<form action="?/addUserRol" method="post" use:enhance>
			<div class="grid grid-cols-1">
				<div>
					<Label class="w-4/5 m-auto text-xl text-[#3BC4A0]">NIA</Label>
					<Input
						type="text"
						id="NIA_add"
						name="NIA_add"
						placeholder="NIA del usuario..."
						pattern={'100[0-9]{6}'}
						required
						class="w-4/5 m-auto"
						bind:value={NIA_add}
					/>
				</div>
			</div>
			<div class="w-screen grid grid-cols-1 mt-4 place-items-center">
				<Label class="text-xl w-auto text-[#3BC4A0]">Selecciona un rol</Label>
				<Select
					class="mt-2 w-1/5"
					id="rol_add"
					name="rol_add"
					items={rols}
					bind:value={rol_add}
					required
					placeholder="Rol"
				/>
			</div>
			<div class="w-screen grid grid-cols-1 place-items-center">
				<Button
					type="submit"
					class="bg-[#3BC4A0] text-white mt-8 px-8 py-2 text-xl hover:bg-[#3BB4A0]"
					>Añadir rol</Button
				>
				<div></div>
			</div>
		</form>
	</TabItem>
	<TabItem
		title="Eliminar Rol"
		class="hover:text-[#3BC4A0]"
		inactiveClasses="text-gray-500 hover:text-[#3BC4A0] p-4 sm:text-base text-xs"
	>
		<form on:submit={delete_user}>
			<div class="grid grid-cols-1">
				<div>
					<Label class="w-4/5 m-auto text-xl text-[#3BC4A0]">NIA</Label>
					<Input
						type="text"
						id="NIA_delete"
						placeholder="NIA del usuario..."
						pattern={'100[0-9]{6}'}
						required
						class="w-4/5 m-auto"
						bind:value={NIA_del}
					/>
				</div>
			</div>
			<div class="w-screen grid grid-cols-1 place-items-center">
				<Button
					type="submit"
					class="bg-[#3BC4A0] text-white mt-8 px-8 py-2 text-xl hover:bg-[#3BC4A0]"
					>Eliminar rol</Button
				>
			</div>
		</form>
	</TabItem>
	<TabItem
		title="Gestionar Reservas"
		class="hover:text-[#3BC4A0]"
		inactiveClasses="text-gray-500 hover:text-[#3BC4A0] p-4 sm:text-base text-xs"
	></TabItem>
</Tabs>

{#if form}
	<Toast position="bottom-right">{form.message}</Toast>
{/if}

<p>Comentarios:</p>
Estaría bien que fuera un desplegable de NIAS para borrar los roles. También tenemos que hacer una página
para consultar las reservas de los un nia.
