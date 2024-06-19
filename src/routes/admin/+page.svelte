<script lang="ts">
	import type { PageData } from './$types';
	import { Tabs, TabItem, Input, Label, Button, Select } from 'flowbite-svelte';
	import { enhance } from '$app/forms';
	import { page } from '$app/stores';

	// Users' rols
	const rols = [
		{ value: 'escuela', name: 'Escuela' },
		{ value: 'atencion', name: 'Atención' },
		{ value: 'general', name: 'General' }
	];

	export let data;

	$: session = $page.data.session;

	setTimeout(() => {
		console.log(session?.user?.email);
	}, 1000);
</script>

<Tabs tabStyle="underline" contentClass="p-4" class="px-8">
	<TabItem
		open
		title="Cambiar Rol"
		class="hover:text-[#3BC4A0] dark:hover:text-dark-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-[#3BC4A0] p-4 dark:hover:text-dark-accent"
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
			<div class="w-screen grid grid-cols-1 place-items-center">
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
				<form action="?/DeleteDB" method="post" use:enhance class="mt-8">
					<Input
						type="hidden"
						required
						id="email_admin"
						name="email_admin"
						value={session?.user?.email}
					/>
					<Button
						type="submit"
						class="w-full1 bg-red-500 hover:bg-[#FF6D2E] dark:bg-red-500 dark:hover:bg-dark-accent"
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
