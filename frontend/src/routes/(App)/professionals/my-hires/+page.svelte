<script lang="ts">
	import { onMount } from 'svelte';
	import { fly } from 'svelte/transition';
	import { Calendar, MapPin, Clock, DollarSign, Briefcase, Star } from 'lucide-svelte';

	export let data;

	let hires = data.props.hires;
	
	let loading = false;
	let error = null;
	let totalHires = 0;
	let totalAmount = 0;
	let totalHours = 0;

	// onMount(async () => {
	// 	try {
	// 		const response = await fetch('YOUR_API_ENDPOINT_HERE');
	// 		if (!response.ok) {
	// 			throw new Error('Failed to fetch data');
	// 		}
	// 		hires = await response.json();
	// 		calculateSummary();
	// 		loading = false;
	// 	} catch (e) {
	// 		error = e.message;
	// 		loading = false;
	// 	}
	// });

	function calculateSummary() {
		totalHires = hires.length;
		totalAmount = hires.reduce((sum, hire) => sum + hire.hire.total_amount, 0);
		totalHours = hires.reduce((sum, hire) => sum + hire.hire.total_hours, 0);
	}

	function formatDate(dateString: string): string {
		return new Date(dateString).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'long',
			day: 'numeric'
		});
	}

	function getStatusColor(status: string): string {
		switch (status.toLowerCase()) {
			case 'active':
				return 'bg-green-100 text-green-800';
			case 'completed':
				return 'bg-blue-100 text-blue-800';
			case 'pending':
				return 'bg-yellow-100 text-yellow-800';
			default:
				return 'bg-gray-100 text-gray-800';
		}
	}
</script>

<main class="min-h-screen bg-gray-50">
	<div class="container mx-auto px-4 py-8">
		<header class="text-center mb-12">
			<h1 class="text-4xl font-bold text-indigo-900 mb-2">My Professional Hires</h1>
			<p class="text-xl text-indigo-600">Managing Your Talented Team</p>
		</header>

		{#if loading}
			<div class="flex justify-center items-center h-64">
				<div
					class="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-indigo-500"
				></div>
			</div>
		{:else if error}
			<div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-8" role="alert">
				<p class="font-bold">Error</p>
				<p>{error}</p>
			</div>
		{:else}
			<div class="grid grid-cols-1 md:grid-cols-3 gap-6 pb-12">
				<div class="bg-white rounded-lg shadow-lg p-6 flex items-center">
					<div class="rounded-full bg-indigo-100 p-3 mr-4">
						<Briefcase class="text-indigo-600" size="24" />
					</div>
					<div>
						<p class="text-sm text-indigo-600 font-semibold">Total Hires</p>
						<p class="text-2xl font-bold text-indigo-900">{totalHires}</p>
					</div>
				</div>
				<div class="bg-white rounded-lg shadow-lg p-6 flex items-center">
					<div class="rounded-full bg-green-100 p-3 mr-4">
						<DollarSign class="text-green-600" size="24" />
					</div>
					<div>
						<p class="text-sm text-green-600 font-semibold">Total Amount</p>
						<p class="text-2xl font-bold text-green-900">${totalAmount.toFixed(2)}</p>
					</div>
				</div>
				<div class="bg-white rounded-lg shadow-lg p-6 flex items-center">
					<div class="rounded-full bg-blue-100 p-3 mr-4">
						<Clock class="text-blue-600" size="24" />
					</div>
					<div>
						<p class="text-sm text-blue-600 font-semibold">Total Hours</p>
						<p class="text-2xl font-bold text-blue-900">{totalHours}</p>
					</div>
				</div>
			</div>

			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 !pt-10">
				{#each hires as hire, index}
					<div
						class="bg-white rounded-lg shadow-lg overflow-hidden transform transition duration-300 hover:scale-105 mt-10"
						in:fly={{ y: 50, duration: 300, delay: index * 100 }}
					>
						<div class="bg-indigo-600 text-white p-4">
							<h2 class="text-xl font-semibold">{hire.professional_username}</h2>
							<p class="text-indigo-200">{hire.professional_title}</p>
						</div>
						<div class="p-6">
							<p class="flex items-center text-gray-600 mb-2">
								<MapPin class="mr-2" size="18" />
								{hire.professional_location}
							</p>
							<p class="flex items-center text-gray-600 mb-2">
								<Star class="mr-2" size="18" />
								{hire.skill_name}
							</p>
							<p class="flex items-center text-gray-600 mb-2">
								<Calendar class="mr-2" size="18" />
								{formatDate(hire.hire.start_date)} - {formatDate(hire.hire.end_date)}
							</p>
							<p class="flex items-center text-gray-600 mb-4">
								<Clock class="mr-2" size="18" />
								{hire.hire.total_hours} hours
							</p>
							<div class="flex justify-between items-center">
								<span class="font-bold text-indigo-600">${hire.hire.total_amount.toFixed(2)}</span>
								<span
									class={`px-3 py-1 rounded-full text-sm font-semibold ${getStatusColor(hire.hire.status)}`}
								>
									{hire.hire.status}
								</span>
							</div>
						</div>
					</div>
				{/each}
			</div>
		{/if}
	</div>
</main>
