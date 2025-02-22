<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { slide } from 'svelte/transition';
	import { authStore, auth } from '$lib/auth_store';
	import profile from '$lib/Images/profile.jpg';

	let activePath = '';
	let isMenuOpen = false;

	// Hover state management
	let dashboardHovered = false;
	let profileHovered = false;
	let dashboardTimeout;
	let profileTimeout;

	const handleMouseEnter = (dropdown) => {
		if (dropdown === 'dashboard') {
			clearTimeout(dashboardTimeout);
			dashboardHovered = true;
		} else if (dropdown === 'profile') {
			clearTimeout(profileTimeout);
			profileHovered = true;
		}
	};

	const handleMouseLeave = (dropdown) => {
		if (dropdown === 'dashboard') {
			dashboardTimeout = setTimeout(() => {
				dashboardHovered = false;
			}, 200);
		} else if (dropdown === 'profile') {
			profileTimeout = setTimeout(() => {
				profileHovered = false;
			}, 200);
		}
	};

	onMount(() => {
		page.subscribe(($page) => {
			activePath = $page.url.pathname;
		});

		return () => {
			clearTimeout(dashboardTimeout);
			clearTimeout(profileTimeout);
		};
	});

	const handleLogout = () => {
		auth.logoutfr();
	};
</script>

<nav class="bg-white border-b shadow-sm">
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
		<div class="flex justify-between h-16">
			<!-- Logo Section -->
			<div class="flex items-center">
				<a href="/" class="flex items-center">
					<span
						class="text-2xl md:text-3xl font-bold text-primary-600 font-['Poppins'] tracking-tight"
					>
						Quick<span class="text-secondary-600">Hire</span>
					</span>
				</a>
			</div>

			<!-- Mobile menu button -->
			<div class="flex items-center md:hidden">
				<button
					on:click={() => (isMenuOpen = !isMenuOpen)}
					class="inline-flex items-center justify-center p-2 rounded-md text-gray-600 hover:text-primary-600 hover:bg-gray-100 focus:outline-none"
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
			<div class="hidden md:flex md:items-center md:space-x-6">
				<a href="/" class="nav-link {activePath === '/' ? 'text-primary-600' : 'text-gray-600'}">
					Home
				</a>
				<a
					href="/professionals"
					class="nav-link {activePath === '/professionals' ? 'text-primary-600' : 'text-gray-600'}"
				>
					Professionals
				</a>
				<a
					href="/about"
					class="nav-link {activePath === '/about' ? 'text-primary-600' : 'text-gray-600'}"
				>
					About
				</a>

				{#if $authStore.isAuthenticated}
					<!-- Dashboard Dropdown -->
					<!-- svelte-ignore a11y-no-static-element-interactions -->
					<div
						class="relative"
						on:mouseenter={() => handleMouseEnter('dashboard')}
						on:mouseleave={() => handleMouseLeave('dashboard')}
					>
						<button
							class="nav-link flex items-center space-x-1 text-gray-600 hover:text-primary-600"
						>
							<span>Dashboard</span>
							<svg
								class="w-4 h-4 transition-transform duration-200 {dashboardHovered
									? 'rotate-180'
									: ''}"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M19 9l-7 7-7-7"
								/>
							</svg>
						</button>

						{#if dashboardHovered}
							<div
								transition:slide|local={{ duration: 200 }}
								class="absolute right-0 mt-1 w-48 bg-white rounded-md shadow-lg py-1 z-50"
							>
								<a href="/professionals/me" class="dropdown-item group">
									<span class="group-hover:translate-x-1 transition-transform inline-block">
										Professional Dashboard
									</span>
								</a>
								<a href="/my-hires" class="dropdown-item group">
									<span class="group-hover:translate-x-1 transition-transform inline-block">
										My Hires
									</span>
								</a>
							</div>
						{/if}
					</div>

					<!-- Profile Dropdown -->
					<!-- svelte-ignore a11y-no-static-element-interactions -->
					<div
						class="relative"
						on:mouseenter={() => handleMouseEnter('profile')}
						on:mouseleave={() => handleMouseLeave('profile')}
					>
						<button
							class="flex items-center space-x-2 text-gray-600 hover:text-primary-600 focus:outline-none"
						>
							<img
								src={$authStore.user.profile_pic_url || profile}
								alt="Profile"
								class="w-8 h-8 rounded-full border-2 border-primary-200"
							/>
							<span class="font-medium">{$authStore.user.username}</span>
							<svg
								class="w-4 h-4 transition-transform duration-200 {profileHovered
									? 'rotate-180'
									: ''}"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M19 9l-7 7-7-7"
								/>
							</svg>
						</button>

						{#if profileHovered}
							<div
								transition:slide|local={{ duration: 200 }}
								class="absolute right-0 mt-1 w-48 bg-white rounded-md shadow-lg py-1 z-50"
							>
								<a href="/profile" class="dropdown-item group">
									<span class="group-hover:translate-x-1 transition-transform inline-block">
										My Profile
									</span>
								</a>
								<a href="/settings" class="dropdown-item group">
									<span class="group-hover:translate-x-1 transition-transform inline-block">
										Settings
									</span>
								</a>
								<hr class="my-1 border-gray-200" />
								<button
									on:click={handleLogout}
									class="dropdown-item text-red-600 hover:bg-red-50 group w-full text-left"
								>
									<span class="group-hover:translate-x-1 transition-transform inline-block">
										Logout
									</span>
								</button>
							</div>
						{/if}
					</div>
				{:else}
					<div class="flex items-center space-x-4">
						<a href="/auth/login" class="text-gray-600 hover:text-primary-600 font-medium text-sm">
							Login
						</a>
						<a
							href="/auth/register"
							class="bg-primary-600 text-white px-4 py-2 rounded-full text-sm font-medium hover:bg-primary-700 transition-colors"
						>
							Register
						</a>
					</div>
				{/if}
			</div>
		</div>
	</div>

	<!-- Mobile Navigation Menu -->
	{#if isMenuOpen}
		<div class="md:hidden" transition:slide>
			<div class="px-2 pt-2 pb-3 space-y-1 bg-white">
				<a
					href="/"
					class="mobile-nav-link {activePath === '/'
						? 'text-primary-600 bg-primary-50'
						: 'text-gray-600'}"
				>
					Home
				</a>
				<a
					href="/professionals"
					class="mobile-nav-link {activePath === '/professionals'
						? 'text-primary-600 bg-primary-50'
						: 'text-gray-600'}"
				>
					Professionals
				</a>
				<a
					href="/about"
					class="mobile-nav-link {activePath === '/about'
						? 'text-primary-600 bg-primary-50'
						: 'text-gray-600'}"
				>
					About
				</a>

				{#if $authStore.isAuthenticated}
					<div class="border-t border-gray-200 pt-4 mt-4">
						<div class="px-4 py-2">
							<div class="flex items-center space-x-3">
								<img
									src={$authStore.user.profile_pic_url || profile}
									alt="Profile"
									class="w-10 h-10 rounded-full border-2 border-primary-200"
								/>
								<div>
									<p class="font-medium text-gray-900">{$authStore.user.name}</p>
									<p class="text-sm text-gray-500">View Profile</p>
								</div>
							</div>
						</div>

						<div class="mt-3 space-y-1">
							<a href="/dashboard" class="mobile-nav-link">Main Dashboard</a>
							<a href="/professional-dashboard" class="mobile-nav-link">Professional Dashboard</a>
							<a href="/my-hires" class="mobile-nav-link">My Hires</a>
							<a href="/settings" class="mobile-nav-link">Settings</a>
							<button
								on:click={handleLogout}
								class="w-full text-left mobile-nav-link text-red-600 hover:bg-red-50"
							>
								Logout
							</button>
						</div>
					</div>
				{:else}
					<div class="mt-4 space-y-2 px-2">
						<a
							href="/auth/login"
							class="block w-full px-4 py-2 text-center text-primary-600 border border-primary-600 rounded-md hover:bg-primary-50"
						>
							Login
						</a>
						<a
							href="/auth/register"
							class="block w-full px-4 py-2 text-center text-white bg-primary-600 rounded-md hover:bg-primary-700"
						>
							Register
						</a>
					</div>
				{/if}
			</div>
		</div>
	{/if}
</nav>
