<script>
	import { AccordionItem, Accordion } from 'flowbite-svelte';
	import { goto } from '$app/navigation';
	import { AnnotationSolid, DrawSquareOutline, LockOpenOutline } from 'flowbite-svelte-icons';
	import Konami from './Konami.svelte';
</script>

<Konami />

<!--Página principal de home-->

<h1 class="sm:text-5xl text-3xl text-center w-full py-6">Servicios de Delegación</h1>
<div class="grid grid-rows-2 md:grid-rows-4 md:h-4/5 place-items-center">
	<Accordion class="md:w-1/2 w-11/12 ">
		<AccordionItem
			class="text-white sm:text-3xl text-2xl px-8 py-3 bg-[#3BC4A0] mb-2 hover:bg-[#FF6D2E] rounded-2xl"
		>
			<button
				slot="header"
				class="flex gap-2"
				on:click={() => {
					goto('./taquillas');
				}}
			>
				<LockOpenOutline class="mt-2" />
				Taquillas
			</button>
			<p class="sm:text-base text-sm">Reserva o comprueba el estado de una taquilla</p>
		</AccordionItem>
		<AccordionItem
			class="text-white sm:text-3xl text-2xl px-8 py-3 bg-[#3BC4A0] mb-2 hover:bg-[#FF6D2E] rounded-2xl"
		>
			<button
				slot="header"
				class="flex gap-2"
				on:click={() => {
					goto('./osciloscopio');
				}}
			>
				<DrawSquareOutline class="mt-2" />
				Osciloscopio
			</button>
			<p class="sm:text-base text-sm">Reserva un osciloscopio en el despacho</p>
		</AccordionItem>
		<AccordionItem
			class="text-white sm:text-3xl text-2xl px-8 py-3 bg-[#3BC4A0] hover:bg-[#FF6D2E] rounded-2xl"
		>
			<button
				slot="header"
				class="flex gap-2"
				on:click={() => {
					goto('./encuestas');
				}}
			>
				<AnnotationSolid class="mt-2" />
				Encuestas 2ºC 2024
			</button>
			<p class="sm:text-base text-sm">Consulta el índice de participación de las encuestas</p>
		</AccordionItem>
	</Accordion>
</div>

<!--Info de Taquillas-->

<div
	class="bg-[#3BC4A0] w-full py-6 lg:flex litems-center justify-center lg:gap-24 grid grid-rows-2 place-items-center"
>
	<div
		class="rounded-full bg-white flex items-center justify-center text-center lg:aspect-square lg:w-1/2 border-solid border-4 w-11/12"
	>
		<p class="flex items-center justify-center text-lg lg:px-4 p-8 sm:text-2xl">
			Delegación gestiona las taquillas de la universidad. Si quieres alquilar una, simplemente
			tendrás que elegir la que quieres y luego rellenar un formulario para reservarla.
		</p>
	</div>

	<button
		class="text-white lg:text-3xl text-xl px-8 lg:py-3 py-6 bg-[#FF6D2E] hover:bg-[#ff8647] rounded-2xl lg:w-1/3 w-5/6 flex gap-2"
		on:click={() => {
			goto('./osciloscopios');
		}}
	>
		<LockOpenOutline class="mt-2 w-1/4" />
		<p class="text-left text-2xl w-full">Ir a Taquillas</p>
	</button>
</div>

<!--Info de Osciloscopios-->

<div
	class="bg-white w-full py-8 lg:flex items-center justify-center lg:gap-24 grid grid-rows-2 place-items-center"
>
	<button
		class="text-white lg:text-3xl text-xl px-8 lg:py-3 py-6 bg-[#FF6D2E] hover:bg-[#ff8647] rounded-2xl lg:w-1/3 w-5/6 flex gap-2"
		on:click={() => {
			goto('./osciloscopios');
		}}
	>
		<DrawSquareOutline class="mt-2 w-1/4" />
		<p class="text-left text-2xl w-full">Ir a Osciloscopios</p>
	</button>
	<div
		class="rounded-full bg-[#3BC4A0] py-6 flex items-center justify-center text-center lg:aspect-square lg:w-1/2 border-solid border-4 text-white w-11/12"
	>
		<p class="flex items-center justify-center text-lg lg:px-4 p-8 sm:text-2xl">
			El despacho de delegación cuenta con tres osciloscopios que los estudiantes pueden usar. Si
			quieres reservar alguno, sólo tendrás que rellenar un formulario para usarlo.
		</p>
	</div>
</div>

<!--Info de encuestas-->

<div
	class="bg-[#3BC4A0] w-full py-6 lg:flex litems-center justify-center lg:gap-24 grid grid-rows-2 place-items-center"
>
	<div
		class="rounded-full bg-white flex items-center justify-center text-center lg:aspect-square lg:w-1/2 border-solid border-4 w-11/12"
	>
		<p class="flex items-center justify-center text-lg lg:px-4 p-8 sm:text-2xl">
			Si quieres saber el porcentaje de participación por grado en las encuestas de evaluación del
			profesorado, haz click en el siguiente botón.
		</p>
	</div>
	<button
		class="text-white lg:text-3xl text-xl px-8 lg:py-3 py-6 bg-[#FF6D2E] hover:bg-[#ff8647] rounded-2xl lg:w-1/3 w-5/6 flex gap-2"
		on:click={() => {
			goto('./encuestas');
		}}
	>
		<LockOpenOutline class="mt-2 w-1/4" />
		<p class="text-left text-2xl w-full">Ver las encuestas</p>
	</button>
</div>
