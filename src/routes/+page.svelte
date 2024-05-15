<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	onMount(() => {
		//if (!$page.data.session) {
		//	goto('/taquillas');
		//}
		//goto('/taquillas');
	});
</script>

<div>
	<h1 class="text-5xl text-center w-full my-8">Servicios de Delegación</h1>
	<div class="grid-rows-3 grid place-items-center">
		<button
			class="text-white text-3xl px-10 py-3 bg-[#3BC4A0] hover:bg-[#FF6D2E] rounded-2xl w-1/3 my-5 mt-10"
			on:click={() => {
				goto('./taquillas');
			}}>Taquillas</button
		>
		<button
			class="text-white text-3xl px-10 py-3 bg-[#3BC4A0] hover:bg-[#FF6D2E] rounded-2xl w-1/3 my-5"
			on:click={() => {
				goto('./osciloscopio');
			}}>Osciloscopio</button
		>
		<button
			class="text-white text-3xl px-10 py-3 bg-[#3BC4A0] hover:bg-[#FF6D2E] rounded-2xl w-1/3 my-5"
			on:click={() => {
				goto('./encuestas');
			}}>Encuestas</button
		>
	</div>
</div>
