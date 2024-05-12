
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

<p>
	Visit <a class="underline text-blue-500 font-bold italic w-max" href="https://kit.svelte.dev"
		>kit.svelte.dev</a
	> to read the documentation
</p>
<button
	on:click={() => alert("Se ha hecho click")}
	class="btn-xl bg-black text-blue-400 rounded-2xl shadow-2xl">
	Test
</button>
