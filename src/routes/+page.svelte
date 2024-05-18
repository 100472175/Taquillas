<script>
	import { AccordionItem, Accordion } from 'flowbite-svelte';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import {
		ChartPieSolid,
		UsersSolid,
		AnnotationSolid,
		DrawSquareOutline,
		HomeSolid,

		LockOpenOutline

	} from 'flowbite-svelte-icons';
	import Konami from './Konami.svelte'

</script>

<Konami />

<div class="h-fit">
	<h1 class="text-5xl text-center w-full my-6">Servicios de Delegación</h1>
	<div class="grid-rows-3 grid place-items-center">
		<Accordion class="w-1/3">
			<AccordionItem class="text-white text-3xl px-8 py-3 bg-[#3BC4A0] mb-2 hover:bg-[#FF6D2E] rounded-2xl">	
				<button slot="header" class="flex gap-2" on:click={() => { goto('./taquillas'); }}>
					<LockOpenOutline class="mt-2"/>
					Taquillas
				</button>
				<p>Reserva o comprueba el estado de una taquilla</p>
			</AccordionItem>
			<AccordionItem class="text-white text-3xl px-8 py-3 bg-[#3BC4A0] mb-2 hover:bg-[#FF6D2E] rounded-2xl">	
				<button slot="header" class="flex gap-2" on:click={() => { goto('./osciloscopio'); }}>
					<DrawSquareOutline class="mt-2"/>
					Osciloscopio
				</button>
				<p>Reserva un osciloscopio en el despacho</p>
			</AccordionItem>
			<AccordionItem class="text-white text-3xl px-8 py-3 bg-[#3BC4A0] hover:bg-[#FF6D2E] rounded-2xl">	
				<button slot="header" class="flex gap-2" on:click={() => {goto('./encuestas');}}>
					<AnnotationSolid class="mt-2"/>
					Encuestas
				</button>
				<p>Consulta el índice de participación de las encuestas</p>
			</AccordionItem>
		</Accordion>
	</div>
</div>
<div class="bg-[#3BC4A0] w-full h-screen flex items-center justify-center gap-24">
	<div class="rounded-full bg-white flex items-center justify-center text-center aspect-square w-5/12 border-solid border-4">
		<p class="flex items-center justify-center text-3xl">
			Delegación gestiona las taquillas de la universidad. Si quieres alquilar una, simplemente tendrás que elegir la que quieres y luego rellenar un formulario para reservarla.
		</p>
	</div>
	<button class="text-white text-3xl px-8 py-3 bg-[#FF6D2E] hover:bg-[#ff8647] rounded-2xl w-1/3 flex gap-2"
			on:click={() => {goto('./taquillas');}}>
		<LockOpenOutline class="mt-2 w-1/4"/> 
		<p class="text-left w-full">Ir a Taquillas</p>
	</button>
</div>
