<script>
	import { Breadcrumb, BreadcrumbItem } from 'flowbite-svelte';
	import { afterUpdate, onMount } from 'svelte';
	import Chart from 'chart.js/auto';
	// @ts-ignore
	import { _data } from './+page.ts';

	export function processData() {
		//fetchCSV().then((csv) => {
		const { names, percentages } = _data;

		const colors_array = Array(names.length).fill('#404040');

		colors_array[names.findIndex((name) => name.includes('ESCUELA'))] = '#3BC4A0';
		colors_array[names.findIndex((name) => name.includes('FCSJ'))] = '#FFBF1F';
		colors_array[names.findIndex((name) => name.includes('FHCD'))] = '#5599DD';

		// Customize colors
		colors_array[0] = '#ffc514';
		colors_array[1] = '#d2cdcd';
		colors_array[2] = '#d6772e';

		new Chart(document.getElementById('myChart'), {
			type: 'bar',
			data: {
				labels: names,
				datasets: [
					{
						label: '% de votos',
						data: percentages,
						borderWidth: 1,
						backgroundColor: colors_array
					}
				]
			},
			options: {
				indexAxis: 'y',
				// Elements options apply to all of the options unless overridden in a dataset
				// In this case, we are setting the border of each horizontal bar to be 2px wide
				elements: {
					bar: {
						borderWidth: 2
					}
				},
				responsive: true,
				plugins: {
					legend: {
						display: false,
						position: 'right',
						labels: {
							font: {
								family: 'Montserrat',
								weight: 'bold'
							},
							color: 'black' // Set the color of legend labels here
						}
					},

					title: {
						display: false,
						text: 'Índice de participación por grado',
						font: {
							family: 'Montserrat',
							weight: 'bold',
							size: 20
						}
					}
				}
			}
		});

		Chart.defaults.font.family = 'Montserrat';
	}

	/**
	 * @type {any[]}
	 */
	let breadcrumItems = [];

	function generateBreadcrums() {
		const currentURL = window.location.href;
		const urlSegments = currentURL.split('/').filter((segment) => segment !== '');

		breadcrumItems = urlSegments.map((segment) => {
			return {
				text: segment.charAt(0).toUpperCase() + segment.slice(1),
				href: `/${segment}`
			};
		});
		breadcrumItems.shift();
		breadcrumItems.shift();
	}

	onMount(() => {
		processData();
		generateBreadcrums();
	});
</script>

<body class=" self-center">
	<div class=" text-center">
		<h1 class=" text-black font-bold font-montserrat mt-4">
			Realiza la encuesta de evaluación
			<a
				class=" text-orange-500 font-bolder"
				href="https://aplicaciones.uc3m.es/encuestas/home/index">aquí</a
			>
		</h1>
	</div>

	<div>
		<canvas id="myChart"></canvas>
	</div>

	<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>
</body>
