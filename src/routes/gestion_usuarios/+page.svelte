<script lang="ts">
	import { page } from '$app/stores';

	let session;

	// Reactive statement to update session whenever $page.data.session changes
	$: session = $page.data.session;
</script>

{#if session?.user?.email}
	<p>{session?.user?.email}</p>
	<pre>{session?.user?.name}</pre>
{:else}
	<p>No tienes acceso a esta sección</p>
	<button class=" btn bg-red-500 rounded-lg snap-center" on:click={() => goto('/')}
		>Ir a la página de inicio</button
	>
{/if}
