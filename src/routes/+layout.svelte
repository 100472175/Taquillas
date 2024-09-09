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
		LockOutline,
		UserCircleOutline,
		ArrowLeftToBracketOutline
	} from 'flowbite-svelte-icons';
	import { sineIn } from 'svelte/easing';
	import { onMount } from 'svelte';
	import type { LayoutData } from './$types';
	import { _toLeftRightCenter } from 'chart.js/helpers';
	import { dev } from '$app/environment';
    import { inject } from '@vercel/analytics';
	import { injectSpeedInsights } from '@vercel/speed-insights/sveltekit';

	injectSpeedInsights();
	inject({ mode: dev ? 'development' : 'production' });

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
		let text: String;
		let inTaquillas = false;
		let inEdificio = true;		
		for (let i = 0; i < urlSegments.length; i++) {
			text = urlSegments[i].charAt(0).toUpperCase() + urlSegments[i].slice(1).replace('_', ' ');
			if (inTaquillas) {

				if (inEdificio) {
					text = "Edificio " + text;
					inEdificio = false;
				}
				else {
					text = "Planta " + text;
				}
			}
			if (text === "Taquillas") {
				inTaquillas = true;
			}
			_breadcrumItems.push({
				text: text,
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
		class="bg-dele-color grid sm:grid-cols-5 grid-cols-4 gap-x-4 md:gap-x-10 dark:bg-dark-primary"
	>
		<button class="sm:w-12 sm:h-12 w-16 h-10" on:click={() => (hidden2 = !hidden2)}>
			<BarsOutline class="sm:w-10 sm:h-10 w-8 h-8 ml-2" />
		</button>
		<a href="/" class="sm:block hidden p-1">
			<img class="sm:w-12 sm:h-auto w-10 h-auto bg-white dark:bg-dark-primary rounded-xl p-1" src="/eps_logo.png" alt="logo" />
		</a>
		<button
			class="font-bold-italic text-white text-center py-2 lg:text-2xl sm:text-xl text-base hover:underline w-auto"
			on:click={() => {
				goto('/');
			}}>Delegación EPS</button
		>
		{#if session}
			<div class="grid sm:grid-cols-12 grid-cols-1 place-items-center rtl:space-x-reverse">
				<div class="sm:block hidden col-span-9">
					<a href="/perfil" class="">
						<p class="text-white italic text-center text-xs lg:text-sm">
							{session.user?.name}
						</p>
					</a>
				</div>
				<div class="min-w-10 w-auto ml-12 col-span-3">
					<a href="/perfil" class="">
						<Avatar src={session?.user?.image} class="h-10 w-10" />
					</a>
				</div>
			</div>
			<button on:click={() => logout()} class="bg-red-500 rounded-3xl h-10 w-10 place-self-center">
				<ArrowLeftToBracketOutline class="h-8 w-8 m-auto" />
			</button>
		{:else}
			{#if doing_login}
				<div class="text-right mt-2">
					<Spinner size={8} color="red" />
				</div>
			{:else}
				<div></div>
			{/if}
			<button on:click={() => login()} class="bg-white rounded-3xl h-10 w-10 place-self-center">
				<UserCircleOutline class="h-8 w-8 m-auto" />
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

	<Drawer
		transitionType="fly"
		{transitionParams}
		bind:hidden={hidden2}
		id="sidebar2"
		divClass="overflow-y-auto z-50 p-4 bg-white dark:bg-dark-secondary"
	>
		<div class="flex items-center">
			<h5
				id="drawer-navigation-label-3"
				class="text-base font-semibold text-gray-600 uppercase dark:text-gray-400"
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
					{#await session then}
						{#if session?.user?.email != null}
							<SidebarItem label="Perfil" href="/perfil" on:click={() => hideNavBar()}>
								<svelte:fragment slot="icon">
									<UserCircleOutline
										class="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
									/>
								</svelte:fragment>
							</SidebarItem>
						{/if}
					{/await}
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
