<script lang="ts">
	import type { PageData } from './$types';
	export let data: PageData;
</script>

<h1 class=" text-4xl text-center py-8">{@html data.title}</h1>

<div class=" text-center font-montserrat font-bold">{@html data.content}</div>
