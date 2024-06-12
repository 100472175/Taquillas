<script lang="ts">
	
	import { page } from '$app/stores';
	import { Tabs, TabItem, Input, Label, Button, Select, Toast } from 'flowbite-svelte';
	let session;

	// Reactive statement to update session whenever $page.data.session changes
	$: session = $page.data.session;

	/** @type {import('./$types').ActionData} */
	export let form;

	
</script>

<h1 class="text-4xl text-center text-[#3BC4A0] m-5">Gestión de usuarios</h1>
<Tabs tabStyle="underline" contentClass="p-4 bg-white">
	<TabItem
		title="Gestionar Reservas"
		class="hover:text-[#3BC4A0]"
		inactiveClasses="text-gray-500 hover:text-[#3BC4A0] p-4"
	></TabItem>
</Tabs>

{#if form}
	<Toast position="bottom-right">{form.message}</Toast>
{/if}

<p>Comentarios:</p>
Estaría bien que fuera un desplegable de NIAS para borrar los roles. También tenemos que hacer una página
para consultar las reservas de los un nia.
