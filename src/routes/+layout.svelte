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
		DarkMode,
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
		LockOpenOutline,
		LockOutline
	} from 'flowbite-svelte-icons';
	import { sineIn } from 'svelte/easing';
	import { onMount } from 'svelte';
	import type { LayoutData } from './$types';
	import { _toLeftRightCenter } from 'chart.js/helpers';

	let hidden2 = true;
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
		function checkEmailDomain(email: String | null | undefined) {
			if (email != null)
				if (!session?.user?.email?.endsWith('uc3m.es')) {
					console.log('Inicia sesión con un correo adecuado', session?.user?.email);
					signOut();
				}
		}
		checkEmailDomain(session?.user?.email);
	});

	afterNavigate(() => {
		breadcrumItems = _generateBreadcrums();
	});

	$: session = $page.data.session;
	$: authorizedEmailsEscuela = $page.data.authorizedEmailsLayoutEscuela;
	$: authorizedEmailsDespacho = $page.data.authorizedEmailsLayoutDespacho;
</script>

<link
	href="https://fonts.googleapis.com/css2?family=Montserrat:wght@100;200;300;400;500;600;700;800;900&family=Roboto&display=swap"
	rel="stylesheet"
/>
<body class="dark:bg-dark-background">
	<header
		class="bg-[#3BC4A0] grid sm:grid-cols-5 grid-cols-4 gap-x-4 md:gap-x-10 dark:bg-dark-primary"
	>
		<button on:click={() => (hidden2 = !hidden2)}>
			<BarsOutline class="sm:w-10 sm:h-10 w-8 h-8 ml-2" />
		</button>
		<img class="sm:w-12 sm:h-auto w-10 h-auto sm:block hidden" src="/logo.webp" alt="logo" />
		<button
			class="font-bold-italic text-white text-center py-2 lg:text-2xl sm:text-xl text-xs hover:underline w-auto"
			on:click={() => {
				goto('/');
			}}>Delegación EPS</button
		>
		{#if session}
			<div class="flex items-center space-x-4 rtl:space-x-reverse">
				<a href="/admin"
					><p class="text-white italic text-center text-xs lg:text-sm sm:block hidden">
						{session.user?.name}
					</p></a
				>
				<a href="/admin"><Avatar src={session.user?.image} class="lg:w-11 sm:w-24 h-auto" /></a>
			</div>
			<button
				on:click={() => logout()}
				class="bg-red-500 text-white rounded-2xl sm:text-base text-xs w-auto mr-2 mt-1 h-8 sm:mt-2 sm:ml-12 sm:w-3/5 lg:w-2/5 lg:ml-24"
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
			<button
				class="bg-white text-black rounded-2xl sm:text-base text-xs w-auto mr-2 mt-1 h-8 sm:mt-2 sm:ml-12 sm:w-3/5 lg:w-2/5 lg:ml-24"
				on:click={() => login()}
			>
				Log-in
			</button>
		{/if}
	</header>

	<Breadcrumb
		solidClass="flex px-5 py-3 text-gray-700 border border-gray-200 rounded-none bg-gray-50 dark:bg-[#111719] dark:border-black"
		aria-label="Solid background breadcrumb example"
		solid
	>
		<BreadcrumbItem href="/" home>Inicio</BreadcrumbItem>
		{#each breadcrumItems as item}
			<BreadcrumbItem href={item.href}>{item.text}</BreadcrumbItem>
		{/each}
	</Breadcrumb>

	<Drawer transitionType="fly" {transitionParams} bind:hidden={hidden2} id="sidebar2" divClass='overflow-y-auto z-50 p-4 bg-white dark:bg-dark-secondary'>
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
			<SidebarWrapper divClass="overflow-y-auto py-4 px-3 rounded dark:bg-dark-secondary">
				<SidebarGroup>
					<SidebarItem label="Inicio" href="/" on:click={() => hideNavBar()}>
						<svelte:fragment slot="icon">
							<HomeSolid
								class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
							/>
						</svelte:fragment>
					</SidebarItem>
					<SidebarItem label="Taquillas" href="/taquillas" on:click={() => hideNavBar()}>
						<svelte:fragment slot="icon">
							<LockOpenOutline
								class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
							/>
						</svelte:fragment>
					</SidebarItem>
					{#await authorizedEmailsDespacho then}
						{#await session then}
							{#if session?.user?.email != null}
								{#if authorizedEmailsDespacho != null && authorizedEmailsDespacho.includes(session?.user?.email) == true}
									<SidebarItem
										label="Gestionar Taquillas"
										href="/gestion_taquillas"
										on:click={() => hideNavBar()}
									>
										<svelte:fragment slot="icon">
											<LockOutline
												class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
											/>
										</svelte:fragment>
									</SidebarItem>
								{/if}
							{/if}
						{/await}
					{/await}

					<SidebarDropdownWrapper label="Osciloscopios">
						<svelte:fragment slot="icon">
							<DrawSquareOutline
								class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
							/>
						</svelte:fragment>
						<SidebarDropdownItem
							label="Reserva"
							href="/osciloscopios"
							on:click={() => hideNavBar()}
						/>
						<SidebarDropdownItem
							label="Estado servicio"
							href="/estado_osciloscopios"
							on:click={() => hideNavBar()}
						/>
					</SidebarDropdownWrapper>
					{#await authorizedEmailsEscuela then}
						{#await session then}
							{#if session?.user?.email != null}
								{#if authorizedEmailsEscuela != null && authorizedEmailsEscuela.includes(session?.user?.email) == true}
									<SidebarItem label="Admin" href="/admin" on:click={() => hideNavBar()}>
										<svelte:fragment slot="icon">
											<UsersSolid
												class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
											/>
										</svelte:fragment>
									</SidebarItem>
								{/if}
							{/if}
						{/await}
					{/await}
					<SidebarItem label="Encuestas" href="/encuestas" on:click={() => (hidden2 = !hidden2)}>
						<svelte:fragment slot="icon">
							<AnnotationSolid
								class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
							/>
						</svelte:fragment>
					</SidebarItem>

					<DarkMode />
				</SidebarGroup>
			</SidebarWrapper>
		</Sidebar>
	</Drawer>

	<slot />
	<DarkMode btnClass="hidden" />
</body>
