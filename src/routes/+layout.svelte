<script context="module" lang="ts">
</script>

<script lang="ts">
	import '../app.css';
	import { signIn, signOut } from '@auth/sveltekit/client';
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';

	let name: string | undefined | null = '';
	let image: string | undefined | null = null;

	if ($page.data.session) {
		name = $page.data.session?.user?.name;
		image = $page.data.session?.user?.image;
	}

	import {
		Avatar,
		Button,
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
		ChartPieSolid,
		UsersSolid,
		AnnotationSolid,
		DrawSquareOutline,
		HomeSolid
	} from 'flowbite-svelte-icons';
	import { sineIn } from 'svelte/easing';
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
</script>

<link
	href="https://fonts.googleapis.com/css2?family=Montserrat:wght@100;200;300;400;500;600;700;800;900&family=Roboto&display=swap"
	rel="stylesheet"
/>

<header class="bg-[#3BC4A0] grid grid-cols-5">
	<button class="bg-white w-1/3 h-8 mt-2 ml-2 rounded-2xl" on:click={() => (hidden2 = !hidden2)}>Menú</button>
	<img class="" src="" alt="logo" />
	<button class="font-bold-italic text-white text-center py-2 text-2xl hover:underline" on:click={() => {goto('./');}}>Delegación EPS</button>
	{#if $page.data.session}
		<div class="flex items-center space-x-4 rtl:space-x-reverse">
    		<p class="text-white italic text-center">{name}</p>  			
  			<Avatar src="{image}"/>
		</div>
		<button on:click={() => logout()} class="bg-red-500 text-white rounded-2xl h-8 mt-2 ml-8 w-4/5">Sign-out</button>
	{:else}
		{#if doing_login}
			<div class="text-right mt-2">
				<Spinner size={8} color="orange" />
			</div>
		{:else}
			<div></div>
		{/if}
		<button class="bg-white rounded-2xl h-8 mt-2 ml-8 w-4/5" on:click={() => login() }>
			Log-in
		</button>
	{/if}
</header>

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
						<ChartPieSolid
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
