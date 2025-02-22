<script>
	// Mock data - replace with your API call
	let professionalData = {
		professional: {
			user_id: 1,
			skill_id: 3,
			title: 'Senior Non-Sleeper',
			experience: 3,
			hourly_rate: '42',
			location: 'Remote',
			id: 1,
			cover_letter: 'hmm',
			is_available: true,
			updated_at: '2025-02-22T15:29:43.216737',
			created_at: '2025-02-22T15:29:43.216737'
		},
		user: {
			username: 'Prateek',
			email: 'prateekpoudel61@gmail',
			phone_no: '9841234567',
			id: 1,
			first_name: 'Prateek',
			last_name: 'Poudel',
			profile_pic_url: null,
			is_active: true
		},
		skill: {
			name: 'Sleepdeprivation',
			description: 'Professional all-nighter'
		}
	};

	let isEditing = false;
	let formData = professionalData
		? {
				skill: professionalData.skill.name,
				title: professionalData.professional.title,
				experience: professionalData.professional.experience,
				hourly_rate: professionalData.professional.hourly_rate,
				location: professionalData.professional.location,
				cover_letter: professionalData.professional.cover_letter
			}
		: {
				skill: '',
				title: '',
				experience: '',
				hourly_rate: '',
				location: '',
				cover_letter: ''
			};

	const handleSubmit = () => {
		// Implement your create/update logic here
		console.log('Form submitted:', formData);
		isEditing = false;
	};

	const formatDate = (dateString) => {
		return new Date(dateString).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'long',
			day: 'numeric'
		});
	};
</script>

<div class="min-h-screen bg-gray-50">
	<!-- Dashboard Header -->
	<div class="bg-white border-b">
		<div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
			<div class="flex justify-between items-center">
				<div>
					<h1 class="text-3xl font-bold text-gray-900">Professional Dashboard</h1>
					<p class="mt-2 text-gray-600">
						{#if professionalData && !isEditing}
							View and manage your professional profile
						{:else}
							{professionalData
								? 'Edit your professional profile'
								: 'Create your professional profile'}
						{/if}
					</p>
				</div>
				{#if professionalData && !isEditing}
					<button
						on:click={() => (isEditing = true)}
						class="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors font-medium"
					>
						Edit Profile
					</button>
				{/if}
			</div>
		</div>
	</div>

	<!-- Content Section -->
	<div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
		{#if professionalData && !isEditing}
			<!-- Display Professional Profile -->
			<div class="bg-white rounded-lg shadow-sm border">
				<div class="p-6 space-y-6">
					<!-- Profile Header -->
					<div class="flex items-center justify-between pb-6 border-b">
						<div class="flex items-center space-x-4">
							<img
								src={professionalData.user.profile_pic_url || `/placeholder.svg?height=64&width=64`}
								alt={professionalData.user.username}
								class="w-16 h-16 rounded-full bg-primary-50 border-2 border-primary-200"
							/>
							<div>
								<h2 class="text-xl font-semibold text-gray-900">
									{professionalData.professional.title}
								</h2>
								<p class="text-gray-600">
									{professionalData.user.first_name}
									{professionalData.user.last_name}
								</p>
							</div>
						</div>
						<div class="text-right">
							<span
								class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-50 text-primary-700"
							>
								${professionalData.professional.hourly_rate}/hr
							</span>
						</div>
					</div>

					<!-- Professional Details -->
					<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
						<div>
							<h3 class="text-sm font-medium text-gray-500">Skill</h3>
							<p class="mt-1 text-base text-gray-900">{professionalData.skill.name}</p>
						</div>

						<div>
							<h3 class="text-sm font-medium text-gray-500">Location</h3>
							<p class="mt-1 text-base text-gray-900">{professionalData.professional.location}</p>
						</div>

						<div>
							<h3 class="text-sm font-medium text-gray-500">Experience</h3>
							<p class="mt-1 text-base text-gray-900">
								{professionalData.professional.experience}
								{professionalData.professional.experience === 1 ? 'year' : 'years'}
							</p>
						</div>

						<div>
							<h3 class="text-sm font-medium text-gray-500">Availability</h3>
							<p class="mt-1">
								<span
									class={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium
                    ${professionalData.professional.is_available ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}
								>
									{professionalData.professional.is_available
										? 'Available for hire'
										: 'Not available'}
								</span>
							</p>
						</div>
					</div>

					<!-- Cover Letter -->
					{#if professionalData.professional.cover_letter}
						<div class="pt-6 border-t">
							<h3 class="text-sm font-medium text-gray-500">Cover Letter</h3>
							<p class="mt-2 text-gray-600 whitespace-pre-line">
								{professionalData.professional.cover_letter}
							</p>
						</div>
					{/if}

					<!-- Profile Info -->
					<div class="pt-6 border-t">
						<div class="grid grid-cols-2 gap-4 text-sm">
							<div>
								<span class="block text-gray-500">Profile Created</span>
								<span class="text-gray-900"
									>{formatDate(professionalData.professional.created_at)}</span
								>
							</div>
							<div>
								<span class="block text-gray-500">Last Updated</span>
								<span class="text-gray-900"
									>{formatDate(professionalData.professional.updated_at)}</span
								>
							</div>
						</div>
					</div>
				</div>
			</div>
		{:else}
			<!-- Professional Profile Form -->
			<div class="bg-white rounded-lg shadow-sm border">
				<form on:submit|preventDefault={handleSubmit} class="p-6 space-y-6">
					<!-- Skill -->
					<div class="space-y-2">
						<label for="skill" class="block text-sm font-medium text-gray-700"> Skill * </label>
						<input
							type="text"
							id="skill"
							bind:value={formData.skill}
							placeholder="e.g. Web Development, UI Design, Data Science"
							class="w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-gray-900 focus:ring-2 focus:ring-primary-600 focus:border-primary-600"
							required
						/>
					</div>

					<!-- Professional Title -->
					<div class="space-y-2">
						<label for="title" class="block text-sm font-medium text-gray-700">
							Professional Title *
						</label>
						<input
							type="text"
							id="title"
							bind:value={formData.title}
							placeholder="e.g. Senior Software Engineer"
							class="w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-gray-900 focus:ring-2 focus:ring-primary-600 focus:border-primary-600"
							required
						/>
					</div>

					<!-- Experience -->
					<div class="space-y-2">
						<label for="experience" class="block text-sm font-medium text-gray-700">
							Years of Experience *
						</label>
						<input
							type="number"
							id="experience"
							bind:value={formData.experience}
							min="0"
							placeholder="e.g. 5"
							class="w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-gray-900 focus:ring-2 focus:ring-primary-600 focus:border-primary-600"
							required
						/>
					</div>

					<!-- Hourly Rate -->
					<div class="space-y-2">
						<label for="hourly_rate" class="block text-sm font-medium text-gray-700">
							Hourly Rate (USD) *
						</label>
						<div class="relative">
							<span class="absolute left-3 top-2 text-gray-500">$</span>
							<input
								type="number"
								id="hourly_rate"
								bind:value={formData.hourly_rate}
								min="0"
								step="0.01"
								placeholder="e.g. 50"
								class="w-full pl-7 pr-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-gray-900 focus:ring-2 focus:ring-primary-600 focus:border-primary-600"
								required
							/>
						</div>
					</div>

					<!-- Location -->
					<div class="space-y-2">
						<label for="location" class="block text-sm font-medium text-gray-700">
							Location *
						</label>
						<input
							type="text"
							id="location"
							bind:value={formData.location}
							placeholder="e.g. Remote, New York, etc."
							class="w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-gray-900 focus:ring-2 focus:ring-primary-600 focus:border-primary-600"
							required
						/>
					</div>

					<!-- Cover Letter -->
					<div class="space-y-2">
						<label for="cover_letter" class="block text-sm font-medium text-gray-700">
							Cover Letter
							<span class="text-gray-500 text-xs">(optional)</span>
						</label>
						<textarea
							id="cover_letter"
							bind:value={formData.cover_letter}
							rows="4"
							placeholder="Tell clients about yourself, your experience, and why they should hire you..."
							class="w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-gray-900 focus:ring-2 focus:ring-primary-600 focus:border-primary-600 resize-y"
						></textarea>
					</div>

					<!-- Submit Button -->
					<div class="pt-4">
						<button
							type="submit"
							class="w-full px-4 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors font-medium focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-600"
						>
							{professionalData ? 'Save Changes' : 'Create Professional Profile'}
						</button>
					</div>
				</form>
			</div>
		{/if}
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

	/* Remove default number input spinners */
	input[type='number']::-webkit-inner-spin-button,
	input[type='number']::-webkit-outer-spin-button {
		-webkit-appearance: none;
		margin: 0;
	}
	input[type='number'] {
		-moz-appearance: textfield;
	}

	/* Style placeholder text */
	::placeholder {
		color: #9ca3af;
	}
</style>
