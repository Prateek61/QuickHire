<script>
	import '../../app.postcss';

	let searchQuery = '';
	import SearchIcon from '$lib/images/search.png';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';

	let activePath = '';
	let isMenuOpen = false;

	onMount(() => {
		page.subscribe(($page) => {
			activePath = $page.url.pathname;
		});
	});
</script>

<nav class="bg-gradient-to-r from-blue-900 to-blue-800 shadow-lg">
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
		<div class="flex justify-between h-16">
			<!-- Logo Section -->
			<div class="flex items-center">
				<a href="/" class="flex items-center">
					<span
						class="text-2xl md:text-3xl font-bold text-yellow-400 font-['Poppins'] tracking-tight"
					>
						Quick<span class="text-white">Hire</span>
					</span>
				</a>
			</div>

			<!-- Mobile menu button -->
			<div class="flex items-center md:hidden">
				<button
					on:click={() => (isMenuOpen = !isMenuOpen)}
					class="inline-flex items-center justify-center p-2 rounded-md text-white hover:text-yellow-400 focus:outline-none"
				>
					<svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						{#if !isMenuOpen}
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M4 6h16M4 12h16M4 18h16"
							/>
						{:else}
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M6 18L18 6M6 6l12 12"
							/>
						{/if}
					</svg>
				</button>
			</div>

			<!-- Desktop Navigation -->
			<div class="hidden md:flex md:items-center md:space-x-4">
				<a
					href="/"
					class="nav-link {activePath === '/'
						? 'bg-yellow-400 text-blue-900'
						: 'text-white hover:bg-blue-700'}"
				>
					Home
				</a>

				{#if activePath === '/' || activePath === '/about' || activePath === '/login'}
					<a
						href="/about"
						class="nav-link {activePath === '/about'
							? 'bg-yellow-400 text-blue-900'
							: 'text-white hover:bg-blue-700'}"
					>
						About
					</a>
					<a
						href="/auth/login"
						class="nav-link {activePath === '/auth/login'
							? 'bg-yellow-400 text-blue-900'
							: 'text-white hover:bg-blue-700'}"
					>
						Login
					</a>
				{:else}
					<a
						href="/profiles"
						class="nav-link {activePath === '/profiles'
							? 'bg-yellow-400 text-blue-900'
							: 'text-white hover:bg-blue-700'}"
					>
						Profiles
					</a>
					<a
						href="/hire"
						class="nav-link {activePath === '/hire'
							? 'bg-yellow-400 text-blue-900'
							: 'text-white hover:bg-blue-700'}"
					>
						Hire
					</a>

					<!-- Search Bar -->
					<div class="relative ml-4">
						<input
							type="text"
							bind:value={searchQuery}
							placeholder="Search professionals..."
							class="w-64 px-4 py-2 rounded-full bg-blue-700 text-white placeholder-blue-300 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:bg-blue-600 transition-all duration-300"
						/>
						<button
							class="absolute right-0 top-0 h-full px-4 flex items-center justify-center rounded-r-full hover:bg-yellow-400 transition-colors duration-300"
						>
							<img src={SearchIcon} alt="Search" class="w-5 h-5 opacity-75" />
						</button>
					</div>
				{/if}
			</div>
		</div>
	</div>

	<!-- Mobile Navigation Menu -->
	{#if isMenuOpen}
		<div class="md:hidden">
			<div class="px-2 pt-2 pb-3 space-y-1">
				<a
					href="/"
					class="mobile-nav-link {activePath === '/'
						? 'bg-yellow-400 text-blue-900'
						: 'text-white'}"
				>
					Home
				</a>

				{#if activePath === '/' || activePath === '/about' || activePath === '/login'}
					<a
						href="/about"
						class="mobile-nav-link {activePath === '/about'
							? 'bg-yellow-400 text-blue-900'
							: 'text-white'}"
					>
						About
					</a>
					<a
						href="/auth/login"
						class="mobile-nav-link {activePath === '/login'
							? 'bg-yellow-400 text-blue-900'
							: 'text-white'}"
					>
						Login
					</a>
				{:else}
					<a
						href="/profiles"
						class="mobile-nav-link {activePath === '/profiles'
							? 'bg-yellow-400 text-blue-900'
							: 'text-white'}"
					>
						Profiles
					</a>
					<a
						href="/hire"
						class="mobile-nav-link {activePath === '/hire'
							? 'bg-yellow-400 text-blue-900'
							: 'text-white'}"
					>
						Hire
					</a>

					<!-- Mobile Search -->
					<div class="px-2 py-2">
						<div class="relative">
							<input
								type="text"
								bind:value={searchQuery}
								placeholder="Search professionals..."
								class="w-full px-4 py-2 rounded-full bg-blue-700 text-white placeholder-blue-300 focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:bg-blue-600"
							/>
							<button
								class="absolute right-0 top-0 h-full px-4 flex items-center justify-center rounded-r-full hover:bg-yellow-400 transition-colors duration-300"
							>
								<img src={SearchIcon} alt="Search" class="w-5 h-5 opacity-75" />
							</button>
						</div>
					</div>
				{/if}
			</div>
		</div>
	{/if}
</nav>
