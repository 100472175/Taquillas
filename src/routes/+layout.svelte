<script lang="ts">
	import '../app.css';
	import { signIn, signOut } from '@auth/sveltekit/client';
	import { goto, afterNavigate } from '$app/navigation';
	import { page } from '$app/stores';
	import {
		Avatar,
		Breadcrumb,
		BreadcrumbItem,
		CloseButton,
		Drawer,
		Sidebar,
		SidebarDropdownItem,
		SidebarDropdownWrapper,
		SidebarGroup,
		SidebarItem,
		SidebarWrapper,
		Spinner
	} from 'flowbite-svelte';
	import {
		UsersSolid,
		AnnotationSolid,
		DrawSquareOutline,
		HomeSolid,
		BarsOutline,
		LockOpenOutline
	} from 'flowbite-svelte-icons';
	import { sineIn } from 'svelte/easing';
	import { onMount } from 'svelte';

	let hidden2 = true;
	let spanClass = 'flex-1 ms-3 whitespace-nowrap';
	let transitionParams = {
		width: 'w-40',
		duration: 200,
		easing: sineIn
	};

	function hideNavBar() {
		hidden2 = true;
	}

	let doing_login = false;
	function login() {
		signIn('google');
		doing_login = true;
	}

	function logout() {
		signOut();
		doing_login = false;
	}

	function _generateBreadcrums() {
		const currentURL = $page.url.pathname;
		const urlSegments = currentURL.split('/').filter((segment) => segment !== '');
		let _breadcrumItems = [];
		console.log(urlSegments);
		for (let i = 0; i < urlSegments.length; i++) {
			_breadcrumItems.push({
				text: urlSegments[i].charAt(0).toUpperCase() + urlSegments[i].slice(1).replace('_', ' '),
				href: `/${urlSegments.slice(0, i + 1).join('/')}`
			});
		}
		return _breadcrumItems;
	}

	let breadcrumItems: any[] = [];
	onMount(() => {
		breadcrumItems = _generateBreadcrums();
	});

	afterNavigate(() => {
		breadcrumItems = _generateBreadcrums();
	});

	$: session = $page.data.session;
</script>

<link
	href="https://fonts.googleapis.com/css2?family=Montserrat:wght@100;200;300;400;500;600;700;800;900&family=Roboto&display=swap"
	rel="stylesheet"
/>

<header class="bg-[#3BC4A0] grid grid-cols-5">
	<button class="w-10" on:click={() => (hidden2 = !hidden2)}>
		<BarsOutline class="w-10 h-10 ml-2 rounded-2xl" />
	</button>
	<img class="w-12 h-auto" src="/logo.png" alt="logo" />
	<button
		class="font-bold-italic text-white text-center py-2 text-2xl hover:underline"
		on:click={() => {
			goto('/');
		}}>Delegación EPS</button
	>
	{#if session}
		<div class="flex items-center space-x-4 rtl:space-x-reverse">
			<a href="/gestion_usuarios"
				><p class="text-white italic text-center text-sm">{session.user?.name}</p></a
			>
			<a href="/gestion_usuarios"><Avatar src={session.user?.image} /></a>
		</div>
		<button on:click={() => logout()} class="bg-red-500 text-white rounded-2xl h-8 mt-2 ml-24 w-2/5"
			>Sign-out</button
		>
	{:else}
		{#if doing_login}
			<div class="text-right mt-2">
				<Spinner size={8} color="orange" />
			</div>
		{:else}
			<div></div>
		{/if}
		<button class="bg-white rounded-2xl h-8 mt-2 ml-24 w-2/5" on:click={() => login()}>
			Log-in
		</button>
	{/if}
</header>

<Breadcrumb class="mt-0" aria-label="Solid background breadcrumb example" solid>
	<BreadcrumbItem href="/" home>Home</BreadcrumbItem>
	{#each breadcrumItems as item}
		<BreadcrumbItem href={item.href}>{item.text}</BreadcrumbItem>
	{/each}
</Breadcrumb>

<Drawer transitionType="fly" {transitionParams} bind:hidden={hidden2} id="sidebar2">
	<div class="flex items-center">
		<h5
			id="drawer-navigation-label-3"
			class="text-base font-semibold text-gray-500 uppercase dark:text-gray-400"
		>
			Menu de Navegación
		</h5>
		<CloseButton on:click={() => (hidden2 = true)} class="mb-4 dark:text-white" />
	</div>
	<Sidebar>
		<SidebarWrapper divClass="overflow-y-auto py-4 px-3 rounded dark:bg-gray-800">
			<SidebarGroup>
				<SidebarItem label="Inicio" href="/" on:click={() => hideNavBar()}>
					<svelte:fragment slot="icon">
						<HomeSolid
							class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
						/>
					</svelte:fragment>
				</SidebarItem>
				<SidebarItem label="Taquillas" href="taquillas" on:click={() => hideNavBar()}>
					<svelte:fragment slot="icon">
						<LockOpenOutline
							class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
						/>
					</svelte:fragment>
				</SidebarItem>
				<SidebarDropdownWrapper label="Osciloscopios">
					<svelte:fragment slot="icon">
						<DrawSquareOutline
							class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
						/>
					</svelte:fragment>
					<SidebarDropdownItem label="Reserva" href="osciloscopios" on:click={() => hideNavBar()} />
					<SidebarDropdownItem
						label="Estado servicio"
						href="estado_osciloscopios"
						on:click={() => hideNavBar()}
					/>
				</SidebarDropdownWrapper>
				{#if $page.data.session?.user}
					<SidebarItem label="Usuarios" href="gestion_usuarios" on:click={() => hideNavBar()}>
						<svelte:fragment slot="icon">
							<UsersSolid
								class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
							/>
						</svelte:fragment>
					</SidebarItem>
				{/if}
				<SidebarItem label="Encuestas" href="./encuestas" on:click={() => (hidden2 = !hidden2)}>
					<svelte:fragment slot="icon">
						<AnnotationSolid
							class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
						/>
					</svelte:fragment>
				</SidebarItem>
			</SidebarGroup>
		</SidebarWrapper>
	</Sidebar>
</Drawer>

<slot />
