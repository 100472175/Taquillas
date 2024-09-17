<script lang="ts">
  import Confetti from 'svelte-confetti';
	import TablaOsciloscopios from '../../../TablaOsciloscopios.svelte';
	import type { PageData } from './$types';
	import { Card, Indicator } from 'flowbite-svelte';
	export let data: PageData;

	function getMonday(d: Date) {
		d = new Date(d);
		var day = d.getDay(),
		diff = d.getDate() - day + (day == 0 ? -6 : 1); // adjust when day is sunday
		return new Date(d.setDate(diff));
	}

	let monday1 = getMonday(new Date());	
	let monday2 = new Date();
	monday2.setDate(monday1.getDate() + 7);
	
	let week1 = [monday1];
	let week2 = [monday2];
	for (let i = 0; i < 4; i++) {
		let day = new Date();
		day.setMonth(week1[i].getMonth());
		day.setFullYear(week1[i].getFullYear());
		day.setDate(week1[i].getDate() + 1);
		week1.push(day);

		let day_2 = new Date();
		day_2.setMonth(week2[i].getMonth());
		day_2.setFullYear(week2[i].getFullYear());
		day_2.setDate(week2[i].getDate() + 1);
		week2.push(day_2);
	}

	function handleReload() {
		setTimeout(() => {
			location.reload();
		}, 2000);
	}

	function clearForm(time: number) {
		setTimeout(() => {
			form = null;
		}, time);
	}

	export let form;
	
</script>

<h1 class="text-3xl sm:text-4xl lg:text-5xl xl:text-7xl text-center font-montserrat mt-4 mb-4 text-dele-color dark:text-dark-primary">
	Selección de Hora
</h1>

<TablaOsciloscopios bind:week1 bind:week2 bind:data></TablaOsciloscopios>

{#if form}
	{#if form.message.includes('Error')}
		<div
			class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 border-dashed border-4 border-red-500 dark:border-red-500 p-4 mx-auto text-center"
		>
			<Card class="text-white bg-red-500 dark:text-white dark:bg-red-500">
				<p class="p-2">{form.message}</p>
			</Card>
		</div>
		<div class="text-white dark:text-dark-background">
			{clearForm(2000)}
		</div>
	{:else}
		<div
			class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 border-dashed border-4 border-green-500 dark:border-green-500 p-4 mx-auto text-center"
		>
			<Card class="text-white bg-green-500 dark:text-white dark:bg-green-500">
				<p class="p-2">{form.message}</p>
			</Card>
			<Confetti amount={500} x={[-0.5, 3.5]} delay={[0, 2000]} duration={2000} infinite />
		</div>
		<div class="text-white dark:text-dark-background">
			{handleReload()}
		</div>
	{/if}
{/if}