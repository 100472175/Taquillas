<script>
	import { AccordionItem, Accordion } from 'flowbite-svelte';
	import { goto } from '$app/navigation';
	import { AnnotationSolid, DrawSquareOutline, LockOpenOutline } from 'flowbite-svelte-icons';
	import Konami from './Konami.svelte';
</script>

<Konami />

<!--Página principal de home-->

<h1 class="sm:text-5xl text-3xl text-center w-full py-6 dark:text-white dark:bg-[#070a17]">Servicios de Delegación</h1>
<div class="grid grid-rows-2 md:grid-rows-4 md:h-4/5 place-items-center dark:bg-[#070a17]">
	<Accordion class="md:w-1/2 w-11/12">
		<AccordionItem
			class="text-white sm:text-3xl text-2xl px-8 py-3 bg-[#3BC4A0] mb-2 rounded-2xl hover:bg-[#FF6D2E] dark:hover:bg-dark-accent dark:text-white dark:border-black dark:bg-dark-primary"
			activeClass="bg-[#FF6D2E]"
		>
			<button
				slot="header"
				class="flex gap-2"
				on:click={() => {
					goto('./taquillas');
				}}
			>
				<LockOpenOutline class="mt-1 h-8 w-8" />
				Taquillas
			</button>
			<p class="sm:text-base text-sm dark:text-white">Reserva o comprueba el estado de una taquilla</p>
		</AccordionItem>
		<AccordionItem
			class="text-white sm:text-3xl text-2xl px-8 py-3 bg-[#3BC4A0] mb-2 hover:bg-[#FF6D2E] dark:hover:bg-dark-accent rounded-2xl dark:text-white dark:border-black dark:bg-dark-primary"
			activeClass="bg-[#FF6D2E]"
		>
			<button
				slot="header"
				class="flex gap-2"
				on:click={() => {
					goto('./osciloscopio');
				}}
			>
				<DrawSquareOutline class="mt-1 h-8 w-8" />
				Osciloscopio
			</button>
			<p class="sm:text-base text-sm dark:text-white">Reserva un osciloscopio en el despacho</p>
		</AccordionItem>
		<AccordionItem
			class="text-white sm:text-3xl text-2xl px-8 py-3 bg-[#3BC4A0] hover:bg-[#FF6D2E] dark:hover:bg-dark-accent rounded-2xl dark:text-white dark:border-black dark:bg-dark-primary"
			activeClass="bg-[#FF6D2E]"
		>
			<button
				slot="header"
				class="flex gap-2"
				on:click={() => {
					goto('./encuestas');
				}}
			>
				<AnnotationSolid class="mt-1 h-8 w-8" />
				Encuestas 2ºC 2024
			</button>
			<p class="sm:text-base text-sm dark:text-white">Consulta el índice de participación de las encuestas</p>
		</AccordionItem>
	</Accordion>
</div>

<!--Info de Taquillas-->

<div
	class="bg-[#3BC4A0] w-full py-6 lg:flex litems-center justify-center lg:gap-24 grid grid-rows-2 place-items-center dark:bg-dark-secondary"
>
	<div
		class="rounded-full bg-white flex items-center justify-center text-center lg:aspect-square lg:w-1/2 border-solid border-4 w-11/12 dark:bg-dark-background dark:text-white dark:border-dark-primary"
	>
		<p class="flex items-center justify-center text-lg lg:px-4 p-8 sm:text-2xl">
			Delegación gestiona las taquillas de la universidad. Si quieres alquilar una, simplemente
			tendrás que elegir la que quieres y luego rellenar un formulario para reservarla.
			<br><br>Para poder reservar, primero debes escoger el edificio y la planta. Tras ello, deberás 
			seleccionar un bloque para escoger la taquilla que quieras reservar. 
		</p>
	</div>

	<button
		class="text-white lg:text-3xl text-xl px-8 lg:py-3 py-6 bg-[#FF6D2E] hover:bg-[#ff8647] rounded-2xl lg:w-1/3 w-5/6 flex gap-2 dark:bg-dark-primary dark:hover:bg-dark-accent"
		on:click={() => {
			goto('./taquillas');
		}}
	>
		<LockOpenOutline class="mt-1 h-8 w-1/4" />
		<p class="text-left text-2xl w-full">Ir a Taquillas</p>
	</button>
</div>

<!--Info de Osciloscopios-->

<div
	class="bg-white w-full py-8 lg:flex items-center justify-center lg:gap-24 grid grid-rows-2 place-items-center dark:bg-dark-background"
>
	<button
		class="text-white lg:text-3xl text-xl px-8 lg:py-3 py-6 bg-[#FF6D2E] hover:bg-[#ff8647] rounded-2xl lg:w-1/3 w-5/6 flex gap-2 dark:bg-dark-primary dark:hover:bg-dark-accent"
		on:click={() => {
			goto('./osciloscopios');
		}}
	>
		<DrawSquareOutline class="mt-1 h-8 w-1/4" />
		<p class="text-left text-2xl w-full">Ir a Osciloscopios</p>
	</button>
	<div
		class="rounded-full bg-[#3BC4A0] py-6 flex items-center justify-center text-center lg:aspect-square lg:w-1/2 border-solid border-4 text-white w-11/12 dark:border-dark-primary dark:bg-dark-secondary"
	>
		<p class="flex items-center justify-center text-lg lg:px-4 p-8 sm:text-2xl">
			El despacho de delegación cuenta con tres osciloscopios que los estudiantes pueden usar. Esta página está
			actualmente en mantenimiento, pero estará habilitada en un futuro.
		</p>
	</div>
</div>

<!--Info de encuestas-->

<div
	class="bg-[#3BC4A0] w-full py-6 lg:flex litems-center justify-center lg:gap-24 grid grid-rows-2 place-items-center dark:bg-dark-secondary"
>
	<div
		class="rounded-full bg-white flex items-center justify-center text-center lg:aspect-square lg:w-1/2 border-solid border-4 w-11/12 dark:bg-dark-background dark:text-white dark:border-dark-primary"
	>
		<p class="flex items-center justify-center text-lg lg:px-4 p-8 sm:text-2xl">
			Si quieres saber el porcentaje de participación por grado en las encuestas de evaluación del
			profesorado, haz click en el siguiente botón. Actualmente, se muestran las encuestas del segundo
			cuatrimeste del curso 2023/2024.
		</p>
	</div>
	<button
		class="text-white lg:text-3xl text-xl px-8 lg:py-3 py-6 bg-[#FF6D2E] hover:bg-[#ff8647] rounded-2xl lg:w-1/3 w-5/6 flex gap-2 dark:bg-dark-primary dark:hover:bg-dark-accent"
		on:click={() => {
			goto('./encuestas');
		}}
	>
		<LockOpenOutline class="mt-1 h-8 w-1/4" />
		<p class="text-left text-2xl w-full">Ver las encuestas</p>
	</button>
</div>
