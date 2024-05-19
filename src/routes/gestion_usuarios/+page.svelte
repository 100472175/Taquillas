<script lang="ts">
	import { page } from '$app/stores';

	let session;

	// Reactive statement to update session whenever $page.data.session changes
	$: session = $page.data.session;
</script>

<p>{session?.user?.email}</p>
<pre>{session?.user?.name}</pre>
