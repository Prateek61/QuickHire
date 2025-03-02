<script>
	import { onMount } from 'svelte';
	import { Star, MapPin, Calendar, Clock } from 'lucide-svelte';
	import profile from '$lib/images/profile.jpg';

	export let data;

	const professionalData = data.props.professional;

	let reviews = data.props.reviews;

	let isLoading = false;
	let showHireForm = false;
	let totalHours = '';
	let totalAmount = '';

	const handleHire = () => {
		if (showHireForm) {
			showHireForm = false;
		} else {
			showHireForm = true;
		}
	};

	const handleSubmitHireForm = () => {
		// Handle form submission logic here
		console.log('Hiring professional:', professionalData.professional.id, {
			totalHours,
			totalAmount
		});
		// Reset form and hide it
		totalHours = '';
		totalAmount = '';
		showHireForm = false;
	};

	const formatDate = (dateString) => {
		return new Date(dateString).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'long'
		});
	};

	const calculateAverageRating = (reviews) => {
		if (!reviews.length) return 0;
		return reviews.reduce((acc, review) => acc + review.rating, 0) / reviews.length;
	};

	const renderStars = (rating) => {
		return Array(5)
			.fill(0)
			.map((_, i) => i < rating);
	};
</script>

<div class="min-h-screen bg-gray-50">
	<!-- Profile Header -->
	<div class="bg-white border-b">
		<div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
			<div class="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
				<div class="flex items-center gap-6">
					<div class="relative">
						<img
							src={professionalData.user.profile_pic_url || profile}
							alt={professionalData.user.username}
							class="w-24 h-24 md:w-32 md:h-32 rounded-full object-cover border-4 border-white shadow-lg"
						/>
						{#if professionalData.professional.is_available}
							<span
								class="absolute bottom-2 right-2 w-4 h-4 bg-green-400 border-2 border-white rounded-full"
							></span>
						{/if}
					</div>
					<div>
						<h1 class="text-2xl md:text-3xl font-bold text-gray-900">
							{professionalData.user.first_name}
							{professionalData.user.last_name}
						</h1>
						<p class="text-lg text-gray-600">{professionalData.professional.title}</p>
						<div class="mt-2 flex items-center gap-4">
							<div class="flex items-center text-yellow-400">
								{#each renderStars(calculateAverageRating(reviews)) as isFilled}
									<Star class="w-5 h-5 {isFilled ? 'fill-current' : 'stroke-current fill-none'}" />
								{/each}
								<span class="ml-2 text-gray-600">
									{calculateAverageRating(reviews).toFixed(1)} ({reviews.length} reviews)
								</span>
							</div>
						</div>
					</div>
				</div>
				<div class="flex flex-col gap-4 md:items-end">
					<div class="text-right">
						<p class="text-2xl font-bold text-primary-600">
							${professionalData.professional.hourly_rate}/hr
						</p>
						<p class="text-sm text-gray-500">Hourly Rate</p>
					</div>
					<button
						on:click={handleHire}
						disabled={isLoading || !professionalData.professional.is_available}
						class="px-6 py-3 bg-primary-600 text-white rounded-full font-medium hover:bg-primary-700
              transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-600
              disabled:opacity-50 disabled:cursor-not-allowed"
					>
						{#if isLoading}
							Loading...
						{:else if !professionalData.professional.is_available}
							Not Available
						{:else}
							Hire Now
						{/if}
					</button>
				</div>
			</div>
		</div>
	</div>
	<!-- Hire Form -->
	{#if showHireForm}
		<div
			class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
			fade={{ duration: 200 }}
		>
			<div
				class="bg-white rounded-lg shadow-xl p-8 max-w-md w-full m-4"
				fly={{ y: 20, duration: 300, easing: 'ease-out' }}
			>
				<h2 class="text-2xl font-bold text-gray-900 mb-6">Hire Professional</h2>
				<form on:submit|preventDefault={handleSubmitHireForm} class="space-y-6">
					<div class="space-y-2">
						<label for="totalHours" class="block text-sm font-medium text-gray-700"
							>Total Hours</label
						>
						<div class="relative">
							<input
								id="totalHours"
								type="number"
								bind:value={totalHours}
								required
								min="0"
								step="1"
								class="block w-full pl-4 pr-10 py-3 text-gray-900 placeholder-gray-400 border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 ease-in-out"
								placeholder="Enter total hours"
							/>
							<span class="absolute inset-y-0 right-0 flex items-center pr-3 text-gray-400">
								hrs
							</span>
						</div>
					</div>
					<div class="space-y-2">
						<label for="totalAmount" class="block text-sm font-medium text-gray-700"
							>Total Amount</label
						>
						<div class="relative">
							<span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400">
								$
							</span>
							<input
								id="totalAmount"
								type="number"
								bind:value={totalAmount}
								required
								min="0"
								step="0.01"
								class="block w-full pl-8 pr-4 py-3 text-gray-900 placeholder-gray-400 border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500 transition-all duration-200 ease-in-out"
								placeholder="Enter total amount"
							/>
						</div>
					</div>
					<button
						type="submit"
						class="w-full px-6 py-3 bg-primary-600 text-white rounded-md font-medium hover:bg-primary-700
											transition-all duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-600
											transform hover:scale-105"
					>
						Submit Hire Request
					</button>
				</form>
				<button
					on:click={() => (showHireForm = false)}
					class="mt-4 w-full px-6 py-2 bg-gray-200 text-gray-800 rounded-md font-medium hover:bg-gray-300
										transition-all duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-400"
				>
					Cancel
				</button>
			</div>
		</div>
	{/if}
	<!-- Main Content -->
	<div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
		<div class="grid grid-cols-1 md:grid-cols-3 gap-8">
			<!-- Left Column - Professional Info -->
			<div class="md:col-span-2 space-y-8">
				<!-- About Section -->
				<div class="bg-white rounded-lg shadow-sm border p-6">
					<h2 class="text-xl font-semibold text-gray-900 mb-4">About</h2>
					<div class="space-y-4">
						<div class="flex items-start gap-2">
							<MapPin class="w-5 h-5 text-gray-400 mt-1" />
							<div>
								<p class="font-medium">Location</p>
								<p class="text-gray-600">{professionalData.professional.location}</p>
							</div>
						</div>
						<div class="flex items-start gap-2">
							<Calendar class="w-5 h-5 text-gray-400 mt-1" />
							<div>
								<p class="font-medium">Member since</p>
								<p class="text-gray-600">{formatDate(professionalData.professional.created_at)}</p>
							</div>
						</div>
						<div class="flex items-start gap-2">
							<Clock class="w-5 h-5 text-gray-400 mt-1" />
							<div>
								<p class="font-medium">Experience</p>
								<p class="text-gray-600">{professionalData.professional.experience} years</p>
							</div>
						</div>
					</div>
				</div>

				<!-- Skills & Description -->
				<div class="bg-white rounded-lg shadow-sm border p-6">
					<h2 class="text-xl font-semibold text-gray-900 mb-4">Skills & Expertise</h2>
					<div class="space-y-4">
						<div>
							<span
								class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-50 text-primary-700"
							>
								{professionalData.skill.name}
							</span>
						</div>
						<p class="text-gray-600">{professionalData.skill.description}</p>
					</div>
				</div>

				<!-- Cover Letter -->
				{#if professionalData.professional.cover_letter}
					<div class="bg-white rounded-lg shadow-sm border p-6">
						<h2 class="text-xl font-semibold text-gray-900 mb-4">Cover Letter</h2>
						<p class="text-gray-600 whitespace-pre-line">
							{professionalData.professional.cover_letter}
						</p>
					</div>
				{/if}
			</div>
			<!-- Right Column - Reviews -->
			<div class="space-y-6">
				<div class="bg-white rounded-lg shadow-sm border p-6">
					<h2 class="text-xl font-semibold text-gray-900 mb-4">Client Reviews</h2>
					{#if reviews.length > 0}
						<div class="space-y-6">
							{#each reviews as review}
								<div class="pb-6 border-b last:border-0 last:pb-0">
									<div class="flex items-start gap-4">
										<img
											src={review.reviewer_profile_pic || profile}
											alt={review.reviewer_name}
											class="w-10 h-10 rounded-full"
										/>
										<div class="flex-1">
											<div class="flex items-center justify-between">
												<h3 class="font-medium text-gray-900">{review.reviewer_name}</h3>
												<div class="flex text-yellow-400">
													{#each renderStars(review.rating) as isFilled}
														<Star
															class="w-4 h-4 {isFilled
																? 'fill-current'
																: 'stroke-current fill-none'}"
														/>
													{/each}
												</div>
											</div>
											{#if review.review}
												<p class="mt-2 text-gray-600">{review.review}</p>
											{/if}
										</div>
									</div>
								</div>
							{/each}
						</div>
					{:else}
						<div class="text-center py-6 text-gray-500">No reviews yet</div>
					{/if}
				</div>
			</div>
		</div>
	</div>
</div>

<style>
	input[type='number']::-webkit-inner-spin-button,
	input[type='number']::-webkit-outer-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}
	input[type='number'] {
		-moz-appearance: textfield;
	}
</style>
