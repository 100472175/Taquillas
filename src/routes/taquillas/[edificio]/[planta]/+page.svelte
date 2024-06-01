<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;
</script>

<h1 class="text-3xl text-center font-montserrat">
	Te encuentras en el edificio {data.edificio}, en la planta {data.planta}.
</h1>

<p>Aquí tendremos el selector de bloque dentro de cada planta.</p>

<p>
	Info <a
		class="text-blue-500 underline"
		href="https://www.w3schools.com/html/html_images_imagemap.asp"
	>
		aqui
	</a>
</p>
