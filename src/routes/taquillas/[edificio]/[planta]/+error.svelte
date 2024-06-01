<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
</script>

<h1 class="text-red-600 text-center text-4xl font-semibold">{$page.status}</h1>
<h2 class="text-3xl text-red-500 text-center">{$page.error?.message}</h2>
<div class="text-center">
	<button
		class=" btn-xl bg-slate-400 rounded-lg text-white font-bold py-2 px-4 mt-4"
		on:click={() => goto('./')}
	>
		Volver a la página de taquillas
	</button>
</div>
