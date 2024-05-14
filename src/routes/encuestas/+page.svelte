<script>
	import { afterUpdate, onMount } from 'svelte';
	import Papa from 'papaparse';
	import { goto } from '$app/navigation';
	import Chart from 'chart.js/auto';

	const FCSJ = '26.26%';
	const FHCD = '33.80%';

	/**
	 * @type {string}
	 */
	let csv;
	csv = `GRADO,P
ESCUELA POLITÉCNICA SUPERIOR,33.48%
Doble Grado Ciencia e Ingeniería de Datos - Ingeniería en Tecnologías de Telecomunicación,27.67%
Doble Grado en Ingeniería Física e Ingeniería en Tecnologías Industriales,0.0%
Doble Grado en Ingeniería Informática y Administración de Empresas - Leganés,35.32%
Doble Grado en Ingeniería Informática y Administración de Empresas - Colmenarejo,29.41%
Grado en Ciencia e Ingeniería de Datos,30.48%
Grado en Ciencias,23.29%
Grado en Ingeniería Aeroespacial,49.11%
Grado en Ingeniería Biomédica,36.98%
Grado en Ingeniería de Comunicaciones Móviles y Espaciales,36.85%
Grado en Ingeniería de la Energía,28.35%
Grado en Ingeniería de Sonido e Imagen,35.43%
Grado en Ingeniería Eléctrica,25.32%
Grado en Ingeniería Electrónica Industrial y Automática,32.31%
Grado en Ingeniería en Tecnologías de Telecomunicación,31.86%
Grado en Ingeniería en Tecnologías Industriales,31.87%
Grado en Ingeniería Física,52.98%
Grado en Ingeniería Informática - Leganés,32.87%
Grado en Ingeniería Informática - Colmenarejo,31.88%
Grado en Ingeniería Mecánica,29.61%
Grado en Ingeniería Robótica,31.48%
Grado en Ingeniería Telemática,33.72%
Grado en Matemática Aplicada y Computación,40.72%`;

	/**
	 * @param {string} csv
	 */
	function parseCSV(csv) {
		// Parse CSV
		const parsedData = Papa.parse(csv, { header: true });
		parsedData.data.push({ GRADO: 'FCSJ', P: FCSJ });
		parsedData.data.push({ GRADO: 'FHCD', P: FHCD });

		// Sort data by percentage
		parsedData.data.sort((a, b) => {
			const percentageA = parseFloat(a['P'].replace('%', ''));
			const percentageB = parseFloat(b['P'].replace('%', ''));
			return percentageB - percentageA;
		});

		// Arrays to store names and percentages
		/**
		 * @type {any[]}
		 */
		let names = [];
		/**
		 * @type {any[]}
		 */
		let percentages = [];

		// Iterate through each row of parsed data
		parsedData.data.forEach((row) => {
			// Extract name and percentage from each row
			const name = row['GRADO'];
			const percentage = parseFloat(row['P']);

			// Push name and percentage to respective arrays
			names.push(name);
			percentages.push(percentage);
		});

		// Add the index to the names at the end
		names.forEach((name, index) => {
			names[index] = `${name} (${index + 1})`;
		});

		names.forEach((name, index) => {
			names[index] = name
				.replace(
					'Doble Grado Ciencia e Ingeniería de Datos - Ingeniería en Tecnologías de Telecomunicación',
					'Datos & Teleco'
				)
				.replace(
					'Doble Grado en Ingeniería Física e Ingeniería en Tecnologías Industriales',
					'Física & Industriales'
				)
				.replace('Administración de Empresas', 'ADE')
				.replace('Grado en Ingeniería', '')
				.replace('Ingeniería', '')
				.replace('Tecnologías', '')
				.replace('Grado', '')
				.replace('Doble', '')
				.replace(' de', ' ')
				.replace(' en', ' ')
				.replace(' la', ' ')
				.trimStart();
		});

		// Return the arrays
		return { names, percentages };
	}

	export function processData() {
		//fetchCSV().then((csv) => {
		const { names, percentages } = parseCSV(csv);

		// Call the function with the CSV data
		//const { names, percentages } = parseCSV(csv_);

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
						display: true,
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

	onMount(() => {
		processData();
	});
</script>

<body class=" self-center">
	<div class=" text-center">
		<h1 class=" text-black font-bold font-montserrat">
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
