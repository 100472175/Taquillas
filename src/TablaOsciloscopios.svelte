<script lang="ts">
	import type { PageData } from './$types';	
	import { Modal, Label, Input, Button, Indicator } from 'flowbite-svelte';
	import { signIn, signOut } from '@auth/sveltekit/client';
	import { enhance } from '$app/forms';
	import ModalIniciaSesion from './ModalIniciaSesion.svelte';
  	import moment from 'moment';
	export let week1, week2, data: PageData;

	let formModalReservation = false;
	let formModalInformationError = false;
	let formModalDateError = false;
	let selectedDia;
	let selectedHora;
	let puesto = data.puesto;
	let NIA = data?.session?.user?.email?.split('@')[0] || '100XXXXXX';
	let current_week;
	let plantilla = data.plantilla;

	let reservas: {} = {};
	data.reservas.then((value) => {
		if (value) {
			let reservas_aux = Object.entries(value);
			reservas = reservas_aux.reduce((acc, [key, value]) => {
				acc[key] = value;
				return acc;
			}, {});
    	} else {
        	console.error("Value is null or undefined.");
    	}
	});

	const days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"];
	const franjas = [9, 11, 15, 17];
	
	let selectedWeek = week1;

	function asignar_horas_dia(day: Date, start_hour: Number) {
		selectedDia = day;
		selectedHora = start_hour;
		current_week = moment(selectedDia).isoWeek();
		if (selectedDia < new Date()) {
			formModalDateError = true;
		}
		else if (NIA != '100XXXXXX') {
			formModalReservation = true;
		} else {
			formModalInformationError = true;
		}
	}

	function change_week() {
		if (selectedWeek == week1) {
			selectedWeek = week2;
		}
		else {
			selectedWeek = week1;
		}
	}

</script>

<Modal bind:open={formModalReservation} size="md" autoclose={false} class="w-full">
	<form
		class="flex flex-col space-y-6"
		action="?/registerOsciloscopio"
		method="post"
		use:enhance
		on:submit={() => {
			formModalReservation = false;
		}}
	>
		<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white">Reservar Puesto</h3>
		<p class="dark:text-white">
			Vas a reservar el puesto {puesto} el día {selectedDia.getDate()}/{selectedDia.getMonth()+1}/{selectedDia.getFullYear()}, de {selectedHora}:00 a {selectedHora+2}:00. 
			Para reservarlo, debes de estar de acuerdo con estas normas:
			<br><br>
			- Como mucho podrán acudir 3 personas al puesto reservado. <br>
			- Eres responsable de lo que le ocurra al puesto durante tu reserva. <br>
		</p>
		<Label class="space-y-2">
			<span>Puesto de Electrónica</span>
			<Input
				type="text"
				id="puesto"
				name="puesto"
				placeholder="x"
				value={puesto}
				required
				readonly
			/>
		</Label>

		<Label class="space-y-2">
			<span>Día de Reserva</span>
			<Input
				type="text"
				id="dia"
				name="dia"
				placeholder="dd/mm/yyyy"
				value={selectedDia.getDate()}/{selectedDia.getMonth()+1}/{selectedDia.getFullYear()}
				required
				readonly
			/>
		</Label>

		<Label class="space-y-2">
			<span>Franja Horaria</span>
			<Input
				type="text"
				id="hora"
				name="hora"
				placeholder="xx/yy/zz hh:mm:ss"
				value={selectedHora}:00-{selectedHora+2}:00 
				required
				readonly
			/>
		</Label>

		<Input type="hidden" id="nia" name="nia" value={NIA} />

		<Input type="hidden" id="correo" name="correo" value={data.session?.user?.email} />

		<Input type="hidden" id="nombre" name="nombre" value={data.session?.user?.name} />

		<Input type="hidden" id="semana" name="semana" value={current_week} />
		
		<Button
			type="submit"
			class="w-full1 bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent"
			>Reservar Hora</Button
		>
	</form>
</Modal>

<ModalIniciaSesion bind:openForm={formModalInformationError}></ModalIniciaSesion>

<Modal bind:open={formModalInformationError} size="xs" autoclose={false} class="w-full">
	<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white">Error</h3>
	<p>Debes iniciar sesión para reservar un puesto</p>
	<Button
		type="button"
		class="w-full1 bg-green-500 hover:bg-dele-accent dark:bg-dark-primary dark:hover:bg-dark-accent"
		on:click={() => {
			signIn();
		}}
	>
		Iniciar Sesión
	</Button>
</Modal>

<Modal bind:open={formModalDateError} size="xs" autoclose={false} class="w-full">
	<h3 class="text-xl font-medium text-gray-900 dark:text-white">Fecha Errónea</h3>
	<p>Esta fecha ya no está disponible.</p>
</Modal>

{#if selectedWeek == week1} 
	<h1 class="sm:text-5xl text-3xl text-center w-full py-6 dark:text-white dark:bg-[#070a17]">Semana Actual</h1>
{:else}
	<h1 class="sm:text-5xl text-3xl text-center w-full py-6 dark:text-white dark:bg-[#070a17]">Semana Siguiente</h1>
{/if}

<div class="grid grid-cols-1 place-self-center mt-6">
	<div class="w-auto m-auto dark:text-white grid sm:grid-cols-3 grid-cols-2">
		<span class="flex items-center"
			><Indicator size="lg" color="green" class="me-1.5" />Libre</span
		>
		<span class="flex items-center"
			><Indicator size="lg" color="red" class="me-1.5" />Ocupada</span
		>
		<span class="flex items-center"
			><Indicator size="lg" color="dark" class="me-1.5" />No Disponible</span
		>
	</div>
</div>

<div class="w-10/12 overflow-auto m-auto mt-6">
	<table
		style="border: 2px solid black; border-radius: 13px; border-spacing: 0; "
		class="m-auto"
	>
		<thead>
			<tr>
				{#each selectedWeek as day}
					<th
						style="border: 1px solid black; "
						class="text-center px-3 py-1 border-collapse bg-[#c6c6c6ff]">
						{days[day.getDay() - 1]}<br>
						{day.getDate()}/{day.getMonth()+1}/{day.getFullYear()}
					</th>
				{/each}
			</tr>
		</thead>
		<tbody>
			{#each franjas as start_hour}
				<tr>
					{#each selectedWeek as day}
						{#if plantilla["plantilla"][day.getDay() + "-" + start_hour] != 0}
							{#if reservas[day.getDate() + "/" + (day.getMonth() + 1) + "/" + day.getFullYear() + "-" + start_hour]}
								{#if reservas[day.getDate() + "/" + (day.getMonth() + 1) + "/" + day.getFullYear() + "-" + start_hour] == 'no_disponible'}
									<td 
										style="border: 1px solid black;"
										class="bg-black text-white cursor-not-allowed text-center p-3">
										
										{start_hour}:00 - {start_hour + 2}:00
									</td>
								{:else}
									<td 
										style="border: 1px solid black;"
										class="bg-red-500 cursor-not-allowed text-center p-3">
										
										{start_hour}:00 - {start_hour + 2}:00
									</td>
								{/if}
							{:else}
								<td 
									style="border: 1px solid black;"
									class="bg-green-500 cursor-pointer hover:bg-green-400 text-center p-3" 
									on:click={() => {asignar_horas_dia(day, start_hour)}}>
									
									{start_hour}:00 - {start_hour + 2}:00
								</td>
							{/if}
						{:else}
							<td 
								style="border: 1px solid black;"
								class="bg-black text-white cursor-not-allowed text-center p-3">
								
								{start_hour}:00 - {start_hour + 2}:00
							</td>
						{/if}
					{/each}
				</tr>
			{/each}
		</tbody>
	</table>
</div>

<div class="grid grid-cols-1 place-items-center mt-6 mb-12">
	<Button class="dark:bg-dark-primary dark:hover:bg-dark-accent bg-[#3BC4A0] hover:bg-[#FF6D2E]"
		on:click={() => change_week()}>
		Cambiar de Semana
	</Button>
</div>