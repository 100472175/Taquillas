<script lang="ts">
	import { enhance } from '$app/forms';
	import { page } from '$app/stores';
	import { Tabs, TabItem, Input, Label, Button, Select, Toast, Card } from 'flowbite-svelte';
	let session;

	// Reactive statement to update session whenever $page.data.session changes
	$: session = $page.data.session;

	/** @type {import('./$types').ActionData} */
	export let form;
	
	let user_taquillas = [{"taquilla": "1.0.A.G001", "status": "reservada", "date": "01-01-2001"}];
</script>

<h1 class="text-4xl text-center text-[#3BC4A0] m-5">Gestión de Taquillas</h1>
<Tabs tabStyle="underline" contentClass="p-4 bg-white">
	<TabItem
		open
		title="Búsqueda por NIA"
		class="hover:text-[#3BC4A0]"
		inactiveClasses="text-gray-500 hover:text-[#3BC4A0] p-4"
	>
		<form action="" method="post" use:enhance>
			<div class="grid grid-cols-1">
				<div>
					<Label class="w-4/5 m-auto text-xl text-[#3BC4A0]">NIA</Label>
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
			<div class="w-screen mt-8 grid grid-cols-1 place-items-center">
				<Button
					type="submit"
					class="bg-[#3BC4A0] text-white px-8 py-2 text-xl hover:bg-[#3BB4A0]"
						>Buscar</Button
				>
			</div>
		</form>
	</TabItem>
	<TabItem
		title="Búsqueda por Taquilla"
		class="hover:text-[#3BC4A0]"
		inactiveClasses="text-gray-500 hover:text-[#3BC4A0] p-4"
	>
		<form class="w-screen" action="" method="post" use:enhance>
			<div class="grid grid-cols-1">
				<div>
					<Label class="w-4/5 m-auto text-xl text-[#3BC4A0]">Taquilla</Label>
					<Input
						type="text"
						id="Taquilla_s"
						name="Taquilla_s"
						placeholder="Taquilla..."
						pattern={'([0-9]\.){2}[A-Z]\.(G|P)[0-9]{3}'}
						required
						class="w-4/5 m-auto"
					/> 
				</div>
			</div>
			<div class="w-screen grid grid-cols-1 place-items-center">
				<Button
					type="submit"
					class="bg-[#3BC4A0] text-white mt-8 text-xl hover:bg-[#3BB4A0]"
						>Buscar</Button
				>
			</div>
		</form>
	</TabItem>
</Tabs>

<div class="w-screen grid grid-cols-1 place-items-center mt-2">
	{#if user_taquillas.length == 0} 
		<p>No hay taquillas</p>
	{/if}
	{#each user_taquillas as taquilla}
		<Card class="mt-2">
			<div class="grid grid-cols-2">
				<h5 class="text-2xl text-[#3BC4A0]">{taquilla["taquilla"]}</h5>
				<p class="text-right pr-10 p-1 text-black">{taquilla["status"]}</p>
			</div>
			<p class="text-black text-sm">{taquilla["date"]}</p>
			{#if taquilla["status"] === "reservada"}
				<div class="grid grid-cols-2 mt-4 place-items-center">
					<button class="w-2/3 text-white bg-green-500 rounded">Confirmar</button>
					<button class="w-2/3 text-white bg-red-500 rounded">Eliminar</button>
				</div>
			{/if}
		</Card>
	{/each}
</div>

{#if form}
	<Toast position="bottom-right">{form.message}</Toast>
{/if}

<p>Comentarios:</p>
Estaría bien que fuera un desplegable de NIAS para borrar los roles. También tenemos que hacer una página
para consultar las reservas de los un nia.
