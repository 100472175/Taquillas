<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	onMount(() => {
			//if (!$page.data.session) {
			//	goto('/taquillas');
			//}
			goto('/taquillas');
		});

</script>


<div>
	<h1 class="text-5xl text-center w-full my-8">Servicios de la Delegación</h1>
	<div class="grid-cols-max">
		<button class="text-green-500 text-3xl px-10 py-3 bg-black rounded-2xl">Taquillas</button>
		<button class="text-green-500 text-3xl px-10 py-3 bg-black rounded-2xl">Osciloscopio</button>
		<button class="text-green-500 text-3xl px-10 py-3 bg-black rounded-2xl">Encuestas</button>
	</div>
</div>
<p>Visit <a class="underline text-red-500" href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
<button on:click={() => console.log("button clicked")} class="btn-xl bg-black text-blue-400 rounded-2xl shadow-2xl"> Test </button>
