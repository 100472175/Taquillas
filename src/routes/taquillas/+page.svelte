<script lang="ts">
	import { page } from '$app/stores';
	import { enhance } from '$app/forms';
	import type { PageData, ActionData } from './$types';
	import { onMount } from 'svelte';
	import { _handleResult } from './+page.ts';

	export let data: PageData;
</script>

<div class="grid-rows-2 grid">
	<div class="grid-cols-2 grid place-items-center mb-8 mt-20">
		<div class="w-4/6 h-10 bg-black text-white h-48 rounded-2xl">
			<p>Edificio 1. Agustín de Betancourt</p>
		</div>
		<div class="w-4/6 h-10 bg-black text-white h-48 rounded-2xl">
			<p>Edificio 2. Sabatini</p>
		</div>
	</div>
	<div class="grid-cols-2 grid place-items-center">
		<div class="w-4/6 h-10 bg-black text-white h-48 rounded-2xl">
			<p>Edificio 4. Torres Quevedo</p>
		</div>
		<div class="w-4/6 h-10 bg-black text-white h-48 rounded-2xl">
			<p>Edificio 7. Juan Benet</p>
		</div>
	</div>
</div>

<p class="text-error-500">{$page.form?.problem ?? ''}</p>
<form
	method="post"
	action="?/registerTaquilla"
	use:enhance={({ formElement }) => {
		return async ({ result, update }) => {
			update();
			_handleResult(result);
		};
	}}
>
	<label for="taquilla">Taquilla</label>
	<input type="text" id="taquilla" name="taquilla" />
	<label for="nia">NIA</label>
	<input type="text" id="nia" name="nia" />
	<button class="bg-black text-white h-10 w-20 rounded-2xl mt-8">Reservar</button>
</form>
