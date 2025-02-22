<script>
	import { onMount } from 'svelte';
	import { Star, MapPin, Calendar, Clock } from 'lucide-svelte';

	export let data;

	const professionalData = data.props.professional

	// Mock reviews data - replace with your API call
	let reviews = [
		{
			id: 1,
			hire_id: 1,
			rating: 5,
			reviewer_name: 'John Doe',
			reviewer_profile_pic: null,
			review: 'Excellent work ethic and very professional. Would hire again!'
		},
		{
			id: 2,
			hire_id: 2,
			rating: 4,
			reviewer_name: 'Jane Smith',
			reviewer_profile_pic: null,
			review: 'Great communication and delivered on time.'
		}
	];

	let isLoading = false;

	const handleHire = async () => {
		isLoading = true;
		try {
			// Implement your hire logic here
			console.log('Hiring professional:', professionalData.professional.id);
		} catch (error) {
			console.error('Error hiring professional:', error);
		} finally {
			isLoading = false;
		}
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
							src={professionalData.user.profile_pic_url || `/placeholder.svg?height=128&width=128`}
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
											src={review.reviewer_profile_pic || `/placeholder.svg?height=40&width=40`}
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
	:root {
		--primary-50: #f0f9ff;
		--primary-100: #e0f2fe;
		--primary-200: #bae6fd;
		--primary-600: #0284c7;
		--primary-700: #0369a1;
	}
</style>
