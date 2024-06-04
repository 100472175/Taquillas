<script lang="ts">
	import { page } from '$app/stores';
	import { Tabs, TabItem, Input, Label, Helper, Button, Select, A } from 'flowbite-svelte';
	import { EyeOutline, EyeSlashOutline } from 'flowbite-svelte-icons';
	let session;

	// Reactive statement to update session whenever $page.data.session changes
	$: session = $page.data.session;
	
	let show_pwd = false;
	let show_pwd_rep = false;
	
	let rol_sel;
	let rols = [
		{value: "escuela", name: "Escuela"},
		{value: "atencion", name: "Atención"}
	];
</script>

<h1 class="text-4xl text-center text-[#3BC4A0] m-5">Gestión de usuarios</h1>
<Tabs tabStyle="underline" contentClass="p-4 bg-white">
	<TabItem open title="Añadir Usuarios" class="hover:text-[#3BC4A0]" inactiveClasses="text-gray-500 hover:text-[#3BC4A0] p-4">
		<form >
			<div class="grid grid-cols-2 gap-x-20">
				<div class="mb-4">
					<Label class="w-4/5 text-xl text-[#3BC4A0]">Nombre</Label>
					<Input type="text" id="name" placeholder="Nombre del nuevo usuario..." required class=""/>
				</div>
				<div>
					<Label class="w-4/5 text-xl text-[#3BC4A0]">NIA</Label>
					<Input type="text" id="NIA" placeholder="NIA del nuevo usuario..." required class=""/>
				</div>
				<div class="mb-4">
					<Label class="w-4/5 text-xl text-[#3BC4A0]">Contraseña</Label>
					<Input type={show_pwd ? "text" : "password"} id="pwd" placeholder="Contraseña..." required >
						<button slot="left" on:click|preventDefault={() => (show_pwd = !show_pwd)} class="pointer-events-auto">
							{#if show_pwd}
								<EyeOutline class="w-6 h-6" />
							{:else}
								<EyeSlashOutline class="w-6 h-6" />
							{/if}
						</button>
					</Input>
				</div>
				<div>
					<Label class="w-4/5 text-xl text-[#3BC4A0]">Repetir contraseña</Label>
					<Input type={show_pwd_rep ? "text" : "password"} id="pwd_rep" placeholder="Repetir contraseña..." required class="">
						<button slot="left" on:click|preventDefault={() => (show_pwd_rep = !show_pwd_rep)} class="pointer-events-auto">
							{#if show_pwd_rep}
								<EyeOutline class="w-6 h-6" />
							{:else}
								<EyeSlashOutline class="w-6 h-6" />
							{/if}
						</button>
					</Input>
				</div>
			</div>
			<div class="w-screen grid grid-cols-1 place-items-center mt-4">
				<Label class="text-xl text-[#3BC4A0]">
					Selecciona un rol
					<Select class="mt-2 w-full" items={rols} bind:value={rol_sel} required placeholder="Rol"/>
				</Label>
			</div>
			<div class="w-screen grid grid-cols-1 place-items-center">
				<Button type="submit" class="bg-[#3BC4A0] text-black mt-10 hover:bg-[#3BB4A0]">Crear Usuario</Button>
			<div>
		</form>
	</TabItem>
	<TabItem title="Eliminar Usuarios" class="hover:text-[#3BC4A0]" inactiveClasses="text-gray-500 hover:text-[#3BC4A0] p-4">
	</TabItem>
	<TabItem title="Gestionar Reservas" class="hover:text-[#3BC4A0]" inactiveClasses="text-gray-500 hover:text-[#3BC4A0] p-4">
	</TabItem>
</Tabs>
