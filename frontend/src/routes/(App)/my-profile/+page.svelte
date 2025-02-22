<script>
	import { onMount } from 'svelte';
	import {
		PUBLIC_APP_CLOUDINARY_API_KEY,
		PUBLIC_APP_CLOUDINARY_CLOUD_NAME
	} from '$env/static/public';
	import profile from '$lib/images/profile.jpg';
	import { authStore } from '$lib/auth_store';
	
	let user = $authStore.user;
	console.log(authStore.user);

	let isEditing = false;
	let editedUser = { ...user };

	const formatDate = (dateString) => {
		return new Date(dateString).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'long',
			day: 'numeric'
		});
	};


	const handleSubmit = () => {
		// Implement your update logic here
		user = { ...editedUser };
		isEditing = false;
	};

	const handleImageUpload = async (e) => {
		try {
			const resSign = await fetch('/api/cloudinary', {
				method: 'POST'
			});
			const resData = await resSign.json();

			const file = e.target.files[0];
			const formData = new FormData();
			formData.append('file', file);
			formData.append('signature', resData.signature);
			formData.append('timestamp', resData.timestamp);
			formData.append('api_key', PUBLIC_APP_CLOUDINARY_API_KEY);
			const res = await fetch(
				`https://api.cloudinary.com/v1_1/${PUBLIC_APP_CLOUDINARY_CLOUD_NAME}/upload`,
				{
					method: 'POST',
					body: formData
				}
			);
			if (res.status !== 200) {
				throw new Error('Failed to upload image');
			}
			const data = await res.json();
			console.log(data);
			editedUser.profile_pic_url = data.secure_url;
		} catch (err) {
			console.log(err);
		}
	};
</script>

<div class="min-h-screen bg-gray-50">
	<!-- Profile Header -->
	<div class="bg-white border-b">
		<div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
			<div class="flex justify-between items-center">
				<h1 class="text-3xl font-bold text-gray-900">Profile</h1>
				<button
					on:click={() => (isEditing = !isEditing)}
					class="px-4 py-2 text-sm font-medium rounded-md transition-colors
            {isEditing
						? 'bg-gray-200 text-gray-600 hover:bg-gray-300'
						: 'bg-primary-600 text-white hover:bg-primary-700'}"
				>
					{isEditing ? 'Cancel' : 'Edit Profile'}
				</button>
			</div>
		</div>
	</div>

	<!-- Profile Content -->
	<div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
		<div class="bg-white rounded-lg shadow-sm border">
			<div class="p-6">
				<form on:submit|preventDefault={handleSubmit}>
					<!-- Profile Picture Section -->
					<div class="flex flex-col items-center mb-8">
						<div class="relative group">
							<img
								src={editedUser.profile_pic_url || profile}
								alt={editedUser.username}
								class="w-32 h-32 rounded-full object-cover border-4 border-primary-100"
							/>
							{#if isEditing}
								<label
									class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 rounded-full cursor-pointer opacity-0 group-hover:opacity-100 transition-opacity"
								>
									<svg
										class="w-8 h-8 text-white"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"
										/>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"
										/>
									</svg>
									<input
										type="file"
										accept="image/*"
										class="hidden"
										on:change={handleImageUpload}
									/>
								</label>
							{/if}
						</div>
						<div class="mt-4 text-center">
							<h2 class="text-2xl font-bold text-gray-900">
								{user.first_name}
								{user.last_name}
							</h2>
							<p class="text-gray-600">@{user.username}</p>
						</div>
					</div>

					<!-- Profile Information -->
					<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
						<!-- Personal Information -->
						<div class="space-y-6">
							<h3 class="text-lg font-semibold text-gray-900 border-b pb-2">
								Personal Information
							</h3>

							<div class="space-y-4">
								<div>
									<label for="first_name" class="block text-sm font-medium text-gray-700">First Name</label>
									{#if isEditing}
										<input
											type="text"
											id="first_name"
											bind:value={editedUser.first_name}
											class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-600 focus:ring-primary-600"
										/>
									{:else}
										<p class="mt-1 text-gray-900">{user.first_name || 'Not set'}</p>
									{/if}
								</div>

								<div>
									<label class="block text-sm font-medium text-gray-700">Last Name</label>
									{#if isEditing}
										<input
											type="text"
											bind:value={editedUser.last_name}
											class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-600 focus:ring-primary-600"
										/>
									{:else}
										<p class="mt-1 text-gray-900">{user.last_name || 'Not set'}</p>
									{/if}
								</div>

								<div>
									<label class="block text-sm font-medium text-gray-700">Birthday</label>
									{#if isEditing}
										<input
											type="date"
											bind:value={editedUser.birthday}
											class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-600 focus:ring-primary-600"
										/>
									{:else}
										<p class="mt-1 text-gray-900">
											{user.birthday ? formatDate(user.birthday) : 'Not set'}
										</p>
									{/if}
								</div>
							</div>
						</div>

						<!-- Contact Information -->
						<div class="space-y-6">
							<h3 class="text-lg font-semibold text-gray-900 border-b pb-2">Contact Information</h3>

							<div class="space-y-4">
								<div>
									<label class="block text-sm font-medium text-gray-700">Email</label>
									{#if isEditing}
										<input
											type="email"
											bind:value={editedUser.email}
											class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-600 focus:ring-primary-600"
										/>
									{:else}
										<p class="mt-1 text-gray-900">{user.email}</p>
									{/if}
								</div>

								<div>
									<label class="block text-sm font-medium text-gray-700">Phone Number</label>
									{#if isEditing}
										<input
											type="tel"
											bind:value={editedUser.phone_no}
											class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-600 focus:ring-primary-600"
										/>
									{:else}
										<p class="mt-1 text-gray-900">{user.phone_no}</p>
									{/if}
								</div>

								<div>
									<label class="block text-sm font-medium text-gray-700">Username</label>
									<p class="mt-1 text-gray-900">{user.username}</p>
								</div>
							</div>
						</div>
					</div>

					<!-- Account Information -->
					<div class="mt-8">
						<h3 class="text-lg font-semibold text-gray-900 border-b pb-2">Account Information</h3>

						<div class="mt-4 grid grid-cols-1 md:grid-cols-2 gap-6">
							<div>
								<label class="block text-sm font-medium text-gray-700">Account Status</label>
								<div class="mt-1 flex items-center text-black">
									{#if user.is_active}
										<div
											class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium text-green-600"
										>
											Active
										</div>
									{:else}
										<div
											class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium text-red-600"
										>
											Inactive
										</div>
									{/if}
								</div>
							</div>

							<div>
								<label class="block text-sm font-medium text-gray-700">Member Since</label>
								<p class="mt-1 text-gray-900">{formatDate(user.created_at)}</p>
							</div>
						</div>
					</div>

					{#if isEditing}
						<div class="mt-8 flex justify-end">
							<button
								type="submit"
								class="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors"
							>
								Save Changes
							</button>
						</div>
					{/if}
				</form>
			</div>
		</div>
	</div>
</div>

<style>
	input[type='text'],
	input[type='email'],
	input[type='tel'],
	input[type='date'] {
		@apply px-3 py-2 border border-gray-300 rounded-md;
	}

	::placeholder {
		color: #9ca3af;
	}

	input {
		color: black;
	}
</style>
