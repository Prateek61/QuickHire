<script>
	// Import necessary components and utilities
	import { onMount } from 'svelte';
	import profile from '$lib/images/profile.jpg';

	export let data;

	let professionals = [];

	// Mock data - replace with your actual API call
	if(data.props.ok)
	{	
		professionals = data.props.professionals;
	}
	else
	{
		console.log("Error fetching data");
		console.error(data.props.error);
	}

	let searchQuery = '';
	let selectedSkill = 'all';
	let selectedLocation = 'all';

	$: filteredProfessionals = professionals.filter((prof) => {
		const matchesSearch =
			prof.user.username.toLowerCase().includes(searchQuery.toLowerCase()) ||
			prof.professional.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
			prof.skill.name.toLowerCase().includes(searchQuery.toLowerCase());

		const matchesSkill = selectedSkill === 'all' || prof.skill.name === selectedSkill;
		const matchesLocation =
			selectedLocation === 'all' || prof.professional.location === selectedLocation;

		return matchesSearch && matchesSkill && matchesLocation;
	});

	// Get unique skills and locations for filters
	$: skills = ['all', ...new Set(professionals.map((p) => p.skill.name))];
	$: locations = ['all', ...new Set(professionals.map((p) => p.professional.location))];
</script>

<div class="min-h-screen bg-gray-50">
	<!-- Header Section -->
	<div class="bg-white border-b">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
			<h1 class="text-3xl font-bold text-gray-900">Find Professionals</h1>
			<p class="mt-2 text-gray-600">Connect with talented professionals for your needs</p>
		</div>
	</div>

	<!-- Search and Filters -->
	<div class="bg-white border-b shadow-sm">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
			<div class="flex flex-col md:flex-row gap-4 items-center">
				<!-- Search Input -->
				<div class="relative flex-1 w-full">
					<input
						type="text"
						bind:value={searchQuery}
						placeholder="Search by name, title, or skill..."
						class="w-full px-4 py-2 rounded-md border border-gray-300 focus:ring-2 focus:ring-primary-600 focus:border-primary-600 transition-colors"
					/>
					<svg
						class="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
						/>
					</svg>
				</div>

				<!-- Filters -->
				<div class="flex gap-4 w-full md:w-auto">
					<select
						bind:value={selectedSkill}
						class="px-4 py-2 rounded-md border border-gray-300 focus:ring-2 focus:ring-primary-600 focus:border-primary-600 transition-colors"
					>
						{#each skills as skill}
							<option value={skill}>
								{skill === 'all' ? 'All Skills' : skill}
							</option>
						{/each}
					</select>

					<select
						bind:value={selectedLocation}
						class="px-4 py-2 rounded-md border border-gray-300 focus:ring-2 focus:ring-primary-600 focus:border-primary-600 transition-colors"
					>
						{#each locations as location}
							<option value={location}>
								{location === 'all' ? 'All Locations' : location}
							</option>
						{/each}
					</select>
				</div>
			</div>
		</div>
	</div>

	<!-- Professionals Grid -->
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
			{#each filteredProfessionals as { professional, user, skill }}
				<div class="bg-white rounded-lg shadow-sm border hover:shadow-md transition-shadow">
					<div class="p-6">
						<!-- Professional Header -->
						<div class="flex items-start justify-between">
							<div class="flex items-center space-x-4">
								<div class="relative">
									<img
										src={user.profile_pic_url || profile}
										alt={user.username}
										class="w-12 h-12 rounded-full bg-primary-50 border-2 border-primary-200"
									/>
									<span
										class="absolute bottom-0 right-0 w-3 h-3 rounded-full bg-green-400 border-2 border-white"
									></span>
								</div>
								<div>
									<h3 class="text-lg font-semibold text-gray-900">
										{user.first_name ? `${user.first_name} ${user.last_name}` : user.username}
									</h3>
									<p class="text-sm text-gray-600">{professional.title}</p>
								</div>
							</div>
							<span
								class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-50 text-primary-700"
							>
								${professional.hourly_rate}/hr
							</span>
						</div>

						<!-- Skills and Experience -->
						<div class="mt-4">
							<div class="flex items-center space-x-2">
								<span class="px-3 py-1 rounded-full text-sm bg-primary-50 text-primary-700">
									{skill.name}
								</span>
								<span class="text-sm text-gray-600">
									{professional.experience}
									{professional.experience === 1 ? 'year' : 'years'} exp.
								</span>
							</div>
							<p class="mt-2 text-sm text-gray-600 line-clamp-2">
								{skill.description}
							</p>
						</div>

						<!-- Location and Action -->
						<div class="mt-4 flex items-center justify-between">
							<div class="flex items-center text-sm text-gray-600">
								<svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
									/>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
									/>
								</svg>
								{professional.location}
							</div>
							<button
								class="px-4 py-2 text-sm font-medium text-white bg-primary-600 rounded-md hover:bg-primary-700 transition-colors"
								on:click={() => {
									window.location.href = `/professionals/${user.username}`;
								}}
							>
								View Profile
							</button>
						</div>
					</div>
				</div>
			{/each}
		</div>

		<!-- Empty State -->
		{#if filteredProfessionals.length === 0}
			<div class="text-center py-12">
				<svg
					class="mx-auto h-12 w-12 text-gray-400"
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
					/>
				</svg>
				<h3 class="mt-2 text-sm font-medium text-gray-900">No professionals found</h3>
				<p class="mt-1 text-sm text-gray-500">Try adjusting your search or filter criteria</p>
			</div>
		{/if}
	</div>
</div>

<style>
	/* Add to your global CSS or style block */
	:root {
		--primary-50: #f0f9ff;
		--primary-100: #e0f2fe;
		--primary-200: #bae6fd;
		--primary-600: #0284c7;
		--primary-700: #0369a1;
	}
</style>
