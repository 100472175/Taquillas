<script lang="ts">
	import type { PageData } from './routes/$types';
	import { Button, Modal } from 'flowbite-svelte';
	import { signIn } from '@auth/sveltekit/client';

	export let openForm: boolean;
</script>

<Modal bind:open={openForm} size="xs" autoclose={false} class="w-full recompensa:bg-recompensa-secondary">
	<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white recompensa:text-white">Error</h3>
	<p class="dark:text-white recompensa:text-white">Debes iniciar sesión para hacer una reserva</p>
	<Button
		type="button"
		class="w-full1 bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent recompensa:bg-recompensa-primary hover:recompensa:bg-recompensa-accent"
		on:click={() => {
			signIn();
		}}
	>
		Iniciar Sesión
	</Button>
</Modal>
