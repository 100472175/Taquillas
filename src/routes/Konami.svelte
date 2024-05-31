<script>
	import { goto } from '$app/navigation';

	/**
	 * @type {any[]}
	 */
	let combo = [];
	let time = Date.now();

	function combinator({ keyCode }) {
		const list = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];
		const now = Date.now();

		if (!list.includes(keyCode)) return;
		if (now - time > 3000) combo = [];

		combo.push(keyCode);
		time = now;

		if (JSON.stringify(combo) === JSON.stringify(list)) {
			goto('entrada-supersecretisima');
		}
	}
</script>

<svelte:window on:keyup={combinator} />
