<script lang="ts">
	import { AccordionItem, Accordion, Button, Popover, Alert } from 'flowbite-svelte';
	import { goto } from '$app/navigation';
	import {
		AnnotationSolid,
		DrawSquareOutline,
		LockOpenOutline,
		UsersSolid,
		LockOutline,
		QuestionCircleSolid,
		UserCircleOutline
	} from 'flowbite-svelte-icons';
	import { page } from '$app/stores';
	import Konami from './Konami.svelte';
	import { signIn, signOut } from '@auth/sveltekit/client';
	
	$: session = $page.data.session;
	$: authorizedEmailsEscuela = $page.data.authorizedEmailsLayoutEscuela;
	$: authorizedEmailsDespacho = $page.data.authorizedEmailsLayoutDespacho;
	let infoModal = false;
	$: copied = false;

	const copy = () => {
		navigator.clipboard.writeText("delegeps@uc3m.es");
		copied = true;
		setTimeout(() => {
			copied = false;	
		}, 2000);
	}
</script>

<Konami />

<!--Página principal de home-->

<div class="grid grid-rows-2 place-items-center dark:bg-[#070a17]" style="min-height: 80vh;">
	<h1 class="sm:text-5xl text-3xl text-center w-full py-6 dark:text-white dark:bg-[#070a17]">
		Servicios de Delegación
	</h1>
	
	<div class="w-screen grid grid-cols-1 place-items-center mb-4">
		<Button id="pop_home" class="dark:text-dark-primary dark:hover:text-dark-accent text-dele-color hover:text-dele-accent">
			<QuestionCircleSolid class="md:h-8 md:w-8 h-10 w-10"/>
		</Button>
	</div>
	
	<Popover class="text-black dark:text-white dark:bg-dark-secondary md:w-1/3 sm:w-1/2 w-10/12 sm:text-md text-sm" title="Home" triggeredBy="#pop_home">
		<p class=" dark:text-white text-sm sm:text-base text-justify">
			Para poder reservar una <span class="underline hover:dark:text-dark-accent hover:text-accent"
				><a href="/taquillas">taquilla</a></span
			>, o un osciloscopio, necesitas
			<button
				on:click={() => {
					signIn('google');
				}}
			>
				<span class="underline italic hover:dark:text-dark-accent hover:text-accent"
					>iniciar sesión
				</span>
				</button> 
				con tu cuenta de Google de la universidad. <br><br>
				Si tienes algún problema, puedes contactar con nosotros
				en el despacho de delegación localizado en la sala 1.0.H01 (al lado del banco Santander) o escríbenos un correo a 
				
				<a class="underline text-dele-color dark:text-dark-primary hover:text-dele-accent hover:dark:text-dark-accent cursor-pointer" 
					on:click={copy}>
					delegeps@uc3m.es
				</a>.
		</p>
	</Popover >
	<Accordion class="md:w-1/2 w-11/12 mb-36">
		{#await session then}
			{#if session?.user?.email != null}
				<AccordionItem
					class="text-white sm:text-3xl text-2xl px-8 py-3 mb-2 bg-dele-color hover:bg-dele-accent dark:hover:bg-dark-accent rounded-2xl dark:text-white dark:border-black dark:bg-dark-primary"
					activeClass="bg-dele-accent"
				>
					<p
						slot="header"
						class="flex gap-2 w-full"
					>
						<UserCircleOutline class="mt-1 h-8 w-8" />
						Perfil
					</p>
					<div class="w-full grid grid-cols-1 place-items-center">
						<button class="m-auto sm:text-base text-sm text-white dark:text-white bg-dele-color dark:bg-dark-primary p-2 sm:mb-0 mb-2 rounded-xl cursor-pointer hover:bg-dele-accent dark:hover:bg-dark-accent" on:click={() => {goto("./perfil")}}>
							Comprueba las taquillas que has reservado
						</button>
					</div>
				</AccordionItem>
			{/if}
		{/await}
		<AccordionItem
			class="text-white sm:text-3xl text-2xl px-8 py-3 bg-dele-color mb-2 rounded-2xl hover:bg-dele-accent dark:hover:bg-dark-accent dark:text-white dark:border-black dark:bg-dark-primary"
			activeClass="bg-dele-accent"
		>
			<p
				slot="header"
				class="flex gap-2 w-full"
			>
				<LockOpenOutline class="mt-1 h-8 w-8" />
				Taquillas
			</p>
			
			<div class="grid sm:grid-cols-3 grid-cols-1 place-items-center">
				<button class="sm:col-span-2 sm:text-base text-sm text-white dark:text-white bg-dele-color dark:bg-dark-primary p-2 sm:mb-0 mb-2 rounded-xl cursor-pointer hover:bg-dele-accent dark:hover:bg-dark-accent" on:click={() => {goto("./taquillas")}}>
					Reserva o comprueba el estado de una taquilla
				</button>
				<button class="w-auto sm:text-base text-sm text-white dark:text-white bg-dele-color dark:bg-dark-primary p-2 px-4 rounded-xl hover:bg-dele-accent hover:dark:bg-dark-accent cursor-pointer">
					<a href="#Taquillas" class="w-auto">
							Más info...
					</a>
				</button>
			</div>
		</AccordionItem>
		{#await authorizedEmailsDespacho then}
			{#await session then}
				{#if session?.user?.email != null}
					{#if authorizedEmailsDespacho != null && authorizedEmailsDespacho.includes(session?.user?.email) == true}
						<AccordionItem
							class="text-white sm:text-3xl text-2xl px-8 py-3 mb-2 bg-dele-color hover:bg-dele-accent dark:hover:bg-dark-accent rounded-2xl dark:text-white dark:border-black dark:bg-dark-primary"
							activeClass="bg-dele-accent"
						>
							<p
								slot="header"
								class="flex gap-2 w-full"
							>
								<LockOutline class="mt-1 h-8 w-8" />
								Gestión de Taquillas
							</p>
							<div class="w-full grid grid-cols-1 place-items-center">
								<button class="sm:text-base text-sm text-white dark:text-white bg-dele-color dark:bg-dark-primary p-2 sm:mb-0 mb-2 rounded-xl cursor-pointer hover:bg-dele-accent dark:hover:bg-dark-accent" on:click={() => {goto("./gestion_taquillas")}}>
									Administra y consulta las reservas de las taquillas
								</button>
							</div>
						</AccordionItem>
					{/if}
				{/if}
			{/await}
		{/await}
		<AccordionItem
			class="text-white sm:text-3xl text-2xl px-8 py-3 bg-dele-color mb-2 hover:bg-dele-accent dark:hover:bg-dark-accent rounded-2xl dark:text-white dark:border-black dark:bg-dark-primary"
			activeClass="bg-dele-accent"
		>
			<p
				slot="header"
				class="flex gap-2 w-full"
			>
				<DrawSquareOutline class="mt-1 h-8 w-8" />
				Osciloscopios [WIP]
			</p>
			<div class="grid sm:grid-cols-3 grid-cols-1 place-items-center">
				<button class="sm:col-span-2 sm:text-base text-sm text-white dark:text-white bg-dele-color dark:bg-dark-primary p-2 sm:mb-0 mb-2 rounded-xl cursor-pointer hover:bg-dele-accent dark:hover:bg-dark-accent" on:click={() => {goto("./osciloscopio")}}>
					Reserva un osciloscopio en el despacho [WIP]
				</button>
				<button class="w-auto sm:text-base text-sm text-white dark:text-white bg-dele-color dark:bg-dark-primary p-2 px-4 rounded-xl hover:bg-dele-accent hover:dark:bg-dark-accent cursor-pointer">
					<a href="#Osciloscopios" class="w-auto">
							Más info...
					</a>
				</button>
			</div>
		</AccordionItem>
		{#await authorizedEmailsEscuela then}
			{#await session then}
				{#if session?.user?.email != null}
					{#if authorizedEmailsEscuela != null && authorizedEmailsEscuela.includes(session?.user?.email) == true}
						<AccordionItem
							class="text-white sm:text-3xl text-2xl px-8 py-3 mb-2 bg-dele-color hover:bg-dele-accent dark:hover:bg-dark-accent rounded-2xl dark:text-white dark:border-black dark:bg-dark-primary"
							activeClass="bg-dele-accent"
						>
							<p
								slot="header"
								class="flex gap-2 w-full"
							>
								<UsersSolid class="mt-1 h-8 w-8" />
								Administrador
							</p>
							<div class="w-full grid grid-cols-1 place-items-center">
								<button class="sm:text-base text-sm text-white dark:text-white bg-dele-color dark:bg-dark-primary p-2 sm:mb-0 mb-2 rounded-xl cursor-pointer hover:bg-dele-accent dark:hover:bg-dark-accent" on:click={() => {goto("./admin")}}>
									Administra los roles y la base de datos
								</button>
							</div>
						</AccordionItem>
					{/if}
				{/if}
			{/await}
		{/await}
		<AccordionItem
			class="text-white sm:text-3xl text-2xl px-8 py-3 bg-dele-color hover:bg-dele-accent dark:hover:bg-dark-accent rounded-2xl dark:text-white dark:border-black dark:bg-dark-primary"
			activeClass="bg-dele-accent"
		>
			<p
				slot="header"
				class="flex gap-2 w-full"
			>
				<AnnotationSolid class="mt-1 h-8 w-8" />
				Encuestas 2ºC 2024
			</p>
			<div class="grid sm:grid-cols-3 grid-cols-1 place-items-center">
				<button class="sm:col-span-2 sm:text-base text-sm text-white dark:text-white bg-dele-color dark:bg-dark-primary p-2 sm:mb-0 mb-2 rounded-xl cursor-pointer hover:bg-dele-accent dark:hover:bg-dark-accent" on:click={() => {goto("./encuestas")}}>
					Consulta el índice de participación de las encuestas
				</button>
				<button class="w-auto sm:text-base text-sm text-white dark:text-white bg-dele-color dark:bg-dark-primary p-2 px-4 rounded-xl hover:bg-dele-accent hover:dark:bg-dark-accent cursor-pointer">
					<a href="#Encuestas" class="w-auto">
							Más info...
					</a>
				</button>
			</div>
		</AccordionItem>
	</Accordion>
	
</div>

<Alert class="text-white bg-dele-color dark:text-white dark:bg-dark-primary m-auto sm:w-1/6 w-1/2 absolute bottom-[5vh] right-[5vw] {copied ? "block" : "hidden"}">
	<p class="text-md sm:text-lg w-auto text-center">Correo copiado!</p>
</Alert>

<!--Info de Taquillas-->

<div
	class="bg-dele-color w-full py-6 lg:flex litems-center justify-center lg:gap-24 grid grid-rows-2 place-items-center dark:bg-dark-secondary"
	id="Taquillas"
>
	<div
		class="rounded-full bg-white flex items-center justify-center text-center lg:aspect-square lg:w-1/2 border-solid border-4 w-11/12 dark:bg-dark-background dark:text-white dark:border-dark-primary"
	>
		<p class="flex items-center justify-center text-lg sm:p-12 p-16 sm:text-2xl">
			Delegación gestiona las taquillas de la universidad. Si quieres alquilar una, simplemente
			tendrás que elegir la que quieres y luego rellenar un formulario para reservarla.
			<br /><br />
			Para poder reservar, primero debes escoger el edificio y la planta. Tras ello,
			deberás seleccionar un bloque para escoger la taquilla que quieras reservar.
		</p>
	</div>

	<button
		class="text-white lg:text-3xl text-xl px-8 lg:py-3 py-6 bg-dele-accent hover:bg-dele-accent-hove rounded-2xl lg:w-1/3 w-5/6 flex gap-2 dark:bg-dark-primary dark:hover:bg-dark-accent"
		on:click={() => {
			goto('./taquillas');
		}}
	>
		<LockOpenOutline class="mt-1 h-8 w-1/4" />
		<p class="text-left text-2xl w-full">Taquillas</p>
	</button>
</div>

<!--Info de Osciloscopios-->

<div
	class="bg-white w-full py-8 lg:flex items-center justify-center lg:gap-24 grid grid-rows-2 place-items-center dark:bg-dark-background"
	id="Osciloscopios"
>
	<button
		class="text-white lg:text-3xl text-xl px-8 lg:py-3 py-6 bg-dele-accent hover:bg-dele-accent-hove rounded-2xl lg:w-1/3 w-5/6 flex gap-2 dark:bg-dark-primary dark:hover:bg-dark-accent"
		on:click={() => {
			goto('./osciloscopios');
		}}
	>
		<DrawSquareOutline class="mt-1 h-8 w-1/4" />
		<p class="text-left text-2xl w-full">Osciloscopios</p>
	</button>
	<div
		class="rounded-full bg-dele-color py-6 flex items-center justify-center text-center lg:aspect-square lg:w-1/2 border-solid border-4 text-white w-11/12 dark:border-dark-primary dark:bg-dark-secondary"
	>
		<p class="flex items-center justify-center text-lg sm:p-12 p-16 sm:text-2xl">
			El despacho de delegación cuenta con tres osciloscopios que los estudiantes pueden usar. Esta
			página está actualmente en mantenimiento, pero estará habilitada en un futuro.
		</p>
	</div>
</div>

<!--Info de encuestas-->

<div
	class="bg-dele-color w-full py-6 lg:flex litems-center justify-center lg:gap-24 grid grid-rows-2 place-items-center dark:bg-dark-secondary"
	id="Encuestas"
>
	<div
		class="rounded-full bg-white flex items-center justify-center text-center lg:aspect-square lg:w-1/2 border-solid border-4 w-11/12 dark:bg-dark-background dark:text-white dark:border-dark-primary"
	>
		<p class="flex items-center justify-center text-lg sm:p-12 p-16 sm:text-2xl">
			Si quieres saber el porcentaje de participación por grado en las encuestas de evaluación del
			profesorado, haz click en el siguiente botón. Actualmente, se muestran las encuestas del
			segundo cuatrimeste del curso 2023/2024.
			<br /><br />
			Es muy importante participar en las encuestas, ya que con los resultados, podemos centrar los
			esfuerzos en las asignaturas que más lo necesitan.
		</p>
	</div>
	<button
		class="text-white lg:text-3xl text-xl px-8 lg:py-3 py-6 bg-dele-accent hover:bg-dele-accent-hove rounded-2xl lg:w-1/3 w-5/6 flex gap-2 dark:bg-dark-primary dark:hover:bg-dark-accent"
		on:click={() => {
			goto('./encuestas');
		}}
	>
		<AnnotationSolid class="mt-1 h-8 w-1/4" />
		<p class="text-left text-2xl w-full">Ver las encuestas</p>
	</button>
</div>
