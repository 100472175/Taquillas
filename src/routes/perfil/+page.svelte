<script lang="ts">
	/** @type {import('./$types').ActionData | any} */
	import { page } from '$app/stores';
	import { Tabs, TabItem, Input, Label, Button, Modal, Card } from 'flowbite-svelte';
	import ModalIniciaSesion from '../../ModalIniciaSesion.svelte';
	import { goto } from '$app/navigation';

	let session = $page.data.session;
	let reservas = $page.data.reservas.reservas;
	let osciloscopios = $page.data.osciloscopios.reservas;

	// Reactive statement to update session whenever $page.data.session changes
	$: session = $page.data.session;
</script>

<h1 class="text-4xl text-center text-dele-color m-5 dark:bg-dark-background dark:text-dark-primary">
	Perfil
</h1>

<Tabs tabStyle="underline" contentClass="p-4" class="px-8">
	<TabItem
		open
		title="Mis Taquillas"
		class=""
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary sm:text-base text-xs"
	>
		<div class="w-auto grid xl:grid-cols-3 md:grid-cols-2 grid-cols-1 place-items-center mt-6">
			{#if reservas != null && reservas.length != 0}
				{#each reservas as reserva}
					<Card class="mt-2">
						<div class="flex place-content-between">
							<h5 class="text-2xl font-medium underline text-dele-color dark:text-dark-primary">
								{reserva['taquilla']}
							</h5>
							{#if reserva['status'] === 'reservada'}
								<p class="text-center p-1 text-white bg-yellow-400 rounded">
									Reservada: {reserva['codigo']}
								</p>
							{:else if reserva['status'] === 'libre'}
								<p class="text-center p-1 text-white bg-green-500 rounded">Libre</p>
							{:else if reserva['status'] === 'ocupada'}
								<p class="text-center p-1 text-white bg-red-500 rounded">Ocupada</p>
							{:else if reserva['status'] === 'null'}
								<p class="text-center p-1 text-white bg-black rounded">No existe</p>
							{:else}
								<p class="text-center p-1 text-white bg-black rounded">No disponible</p>
							{/if}

						</div>
						{#if reserva['status'] === 'reservada' || reserva['status'] === 'ocupada'}
							<p class="text-black text-sm mt-4 dark:text-white">
								Reservada el {reserva['date'].split(' ')[0]} a las {reserva[
									'date'
								].split(' ')[1]}
							</p>
						{/if}
						
					</Card>
				{/each}
			{:else}
				<p class="text-4xl text-center text-dele-color mt-5 col-span-3 dark:text-white">Todavía no has hecho ninguna reserva</p>
			{/if}
		</div>
	</TabItem>
	<TabItem
		title="Mis Puestos de Electrónica"
		class=""
		activeClasses="sm:text-base text-xs p-4 text-dele-accent dark:text-dark-accent"
		inactiveClasses="text-gray-500 hover:text-dele-color p-4 dark:hover:text-dark-primary sm:text-base text-xs"
	>
		<div class="w-auto grid xl:grid-cols-3 md:grid-cols-2 grid-cols-1 place-items-center mt-6">
			{#if osciloscopios != null && osciloscopios.length != 0}
				{#each osciloscopios as reserva}
					<Card class="mt-2">
						<div class="flex place-content-between">
							<h5 class="text-2xl font-medium underline text-dele-color dark:text-dark-primary">
								{reserva['fecha']} {(reserva['hora']) + ":00 - " + (reserva['hora'] + 2) + ":00"}
							</h5>
							{#if reserva['estado'] === 'reservada'}
								<p class="text-center p-1 text-white bg-red-500 rounded">
									Reservada
								</p>
							{:else if reserva['estado'] === 'completada'}
								<p class="text-center p-1 text-white bg-black rounded">Completa</p>
							{:else}
								<p class="text-center p-1 text-white bg-black rounded">No disponible</p>
							{/if}

						</div>
						<p class="text-black text-sm mt-4 dark:text-white">
							Puesto Reservado: {reserva["puesto"]}
						</p>	
					</Card>
				{/each}
			{:else}
				<p class="text-4xl text-center text-dele-color mt-5 col-span-3 dark:text-white">Todavía no has hecho ninguna reserva</p>
			{/if}
		</div>
	</TabItem>
</Tabs>