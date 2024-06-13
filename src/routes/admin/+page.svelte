<script lang="ts">
	import type { PageData } from './$types';
	import { Tabs, TabItem, Input, Label, Button, Select, Toast } from 'flowbite-svelte';
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';

	// Users' rols
	const rols = [
		{ value: 'escuela', name: 'Escuela' },
		{ value: 'atencion', name: 'Atención' },
		{ value: 'general', name: 'General'}
	];
	
	export let data;

</script>

<Tabs tabStyle="underline" contentClass="p-4 bg-white">
	<TabItem
		open
		title="Añadir Rol"
		class="hover:text-[#3BC4A0]"
		inactiveClasses="text-gray-500 hover:text-[#3BC4A0] p-4"
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
			<Input type="hidden" id="nia_admin" name="nia_admin" value={data.session?.user?.email?.split('@')[0]} />	

			<Input type="hidden" id="nombre_admin" name="nombre_admin" value={data.session?.user?.name} />
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
</Tabs>
