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
	
	onMount(() => {
		//if (!$page.data.session) {
		//	goto('/taquillas');
		//}
		//goto('/taquillas');
	});
</script>

<div>
	<h1 class="text-5xl text-center w-full my-8">Servicios<a class="cursor-text" href="/entrada-supersecretisima">&nbsp</a>de Delegación</h1>
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
