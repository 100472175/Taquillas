<script lang="ts">
	import { page } from '$app/stores';
	import { enhance } from '$app/forms';
	import type { PageData, ActionData } from './$types';
	import { onMount } from 'svelte';
	import { _handleResult } from './+page.ts';
</script>

<div class="grid-rows-2 grid">
	<div class="grid-cols-2 grid place-items-center mb-8 mt-20">
		<div class="w-4/6 bg-black text-white h-48 rounded-2xl">
			<a href="/taquillas/1">
				<img
					src="edificios/1-betancourt.png"
					class="rounded-2xl max-h-full max-w-full object-cover"
					alt="Edificio 1. Agustín de Betancourt"
				/>
			</a>
		</div>
		<div class="w-4/6 h-10 bg-black text-white h-48 rounded-2xl">
			<a href="/taquillas/2">
				<img
					src="edificios/2-sabatini.jpg"
					class="rounded-2xl max-h-full max-w-full object-cover"
					alt="Edificio 2. Sabatini"
				/>
			</a>
		</div>
	</div>
	<div class="grid-cols-2 grid place-items-center">
		<div class="w-4/6 h-10 bg-black text-white h-48 rounded-2xl">
			<a href="/taquillas/4">
				<img
					src="edificios/4-Torres_Quevedo.jpg"
					class="rounded-2xl w-1/2 object-cover"
					alt="Edificio 4. Torres Quevedo"
				/>
			</a>
		</div>
		<div class="w-4/6 h-10 bg-black text-white h-48 rounded-2xl">
			<a href="/taquillas/7">
				<img
					src="edificios/7-Juan_Benet.jpg"
					class="rounded-2xl w-full object-cover"
					alt="Edificio 7. Juan Benet"
				/>
			</a>
		</div>
	</div>
</div>
