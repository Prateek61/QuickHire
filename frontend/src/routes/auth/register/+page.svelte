<script>
	export let errorMessage = '';
	import IconUser from '~icons/mdi/account';
	import IconEmail from '~icons/mdi/email';
	import IconLock from '~icons/mdi/lock';
	import IconPhone from '~icons/mdi/phone';
	import IconHome from '~icons/mdi/home';

	let showPassword = false;
	let showConfirmPassword = false;
	let password = '';
	let confirmPassword = '';
	let passwordStrength = 0;

	function calculatePasswordStrength(pass) {
		let strength = 0;
		if (pass.length >= 8) strength++;
		if (/[A-Z]/.test(pass)) strength++;
		if (/[0-9]/.test(pass)) strength++;
		if (/[^A-Za-z0-9]/.test(pass)) strength++;
		return strength;
	}

	$: passwordStrength = calculatePasswordStrength(password);
</script>

<div
	class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 via-indigo-900 to-purple-900 py-5 px-4 sm:px-6 lg:px-8"
>
	<!-- Home Button -->
	<a
		href="/"
		class="absolute top-4 left-4 flex items-center justify-center p-2 bg-white/10 hover:bg-white/20 rounded-lg backdrop-blur-lg border border-white/20 transition-all duration-300"
	>
		<IconHome class="h-6 w-6 text-white" />
	</a>

	<div class="w-full max-w-md space-y-5">
		<!-- Header Section -->
		<div class="text-center">
			<h2 class="mt-6 text-4xl font-bold text-white">Create Account</h2>
			<p class="mt-2 text-sm text-blue-200">Join our community of professionals</p>
		</div>

		<!-- Main Form Card -->
		<div class="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl border border-white/20">
			{#if errorMessage}
				<div class="mb-6 bg-red-500/20 backdrop-blur-sm border border-red-500/50 rounded-lg p-4">
					<p class="text-red-200 text-sm flex items-center">
						<svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
							/>
						</svg>
						{errorMessage}
					</p>
				</div>
			{/if}

			<form method="POST" action="?/register" class="space-y-6">
				<!-- Username Input -->
				<div class="space-y-2">
					<label for="username" class="block text-sm font-medium text-blue-200">Username</label>
					<div class="relative">
						<div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
							<IconUser class="h-5 w-5 text-blue-300" />
						</div>
						<input
							type="text"
							id="username"
							name="name"
							required
							class="block w-full pl-10 pr-3 py-3 bg-white/10 border border-white/20 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-blue-300 text-white text-sm transition-all duration-300"
							placeholder="Enter your username"
						/>
					</div>
				</div>

				<!-- Email Input -->
				<div class="space-y-2">
					<label for="email" class="block text-sm font-medium text-blue-200">Email Address</label>
					<div class="relative">
						<div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
							<IconEmail class="h-5 w-5 text-blue-300" />
						</div>
						<input
							type="email"
							id="email"
							name="email"
							required
							class="block w-full pl-10 pr-3 py-3 bg-white/10 border border-white/20 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-blue-300 text-white text-sm transition-all duration-300"
							placeholder="Enter your email"
						/>
					</div>
				</div>

				<!-- Phone Input -->
				<div class="space-y-2">
					<label for="phone" class="block text-sm font-medium text-blue-200">Phone Number</label>
					<div class="relative">
						<div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
							<IconPhone class="h-5 w-5 text-blue-300" />
						</div>
						<input
							type="tel"
							id="phone"
							name="phone_no"
							required
							class="block w-full pl-10 pr-3 py-3 bg-white/10 border border-white/20 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-blue-300 text-white text-sm transition-all duration-300"
							placeholder="Enter your phone number"
						/>
					</div>
				</div>

				<!-- Password Input -->
				<div class="space-y-2">
					<label for="password" class="block text-sm font-medium text-blue-200">Password</label>
					<!-- Password Input -->
					<div class="relative">
						<div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
							<IconLock class="h-5 w-5 text-blue-300" />
						</div>
						{#if showPassword}
							<input
								type="text"
								id="password"
								name="password"
								bind:value={password}
								required
								class="block w-full pl-10 pr-10 py-3 bg-white/10 border border-white/20 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-blue-300 text-white text-sm transition-all duration-300"
								placeholder="Enter your password"
							/>
						{:else}
							<input
								type="password"
								id="password"
								name="password"
								bind:value={password}
								required
								class="block w-full pl-10 pr-10 py-3 bg-white/10 border border-white/20 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-blue-300 text-white text-sm transition-all duration-300"
								placeholder="Enter your password"
							/>
						{/if}
						<button
							type="button"
							class="absolute inset-y-0 right-0 pr-3 flex items-center"
							on:click={() => (showPassword = !showPassword)}
						>
							<!-- Eye icon SVG remains the same -->
							<svg
								class="h-5 w-5 text-blue-300 hover:text-blue-200"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								{#if showPassword}
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
									/>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
									/>
								{:else}
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
									/>
								{/if}
							</svg>
						</button>
					</div>

					<!-- Password Strength Indicator -->
					<div class="mt-2">
						<div class="flex space-x-1">
							{#each Array(4) as _, i}
								<div
									class="h-1 w-1/4 rounded-full transition-all duration-300"
									class:bg-red-500={i < passwordStrength && passwordStrength === 1}
									class:bg-yellow-500={i < passwordStrength && passwordStrength === 2}
									class:bg-green-500={i < passwordStrength && passwordStrength >= 3}
									class:bg-white-20={i >= passwordStrength}
								></div>
							{/each}
						</div>
						<p class="text-xs text-blue-200 mt-1">
							Password strength:
							{#if passwordStrength === 0}
								Too weak
							{:else if passwordStrength === 1}
								Weak
							{:else if passwordStrength === 2}
								Medium
							{:else if passwordStrength === 3}
								Strong
							{:else}
								Very strong
							{/if}
						</p>
					</div>
				</div>

				<!-- Confirm Password Input -->
				<div class="space-y-2">
					<label for="confirm_password" class="block text-sm font-medium text-blue-200"
						>Confirm Password</label
					>
					<!-- Confirm Password Input -->
					<div class="relative">
						<div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
							<IconLock class="h-5 w-5 text-blue-300" />
						</div>
						{#if showConfirmPassword}
							<input
								type="text"
								id="confirm_password"
								name="passwordConfirm"
								bind:value={confirmPassword}
								required
								class="block w-full pl-10 pr-10 py-3 bg-white/10 border border-white/20 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-blue-300 text-white text-sm transition-all duration-300"
								placeholder="Confirm your password"
							/>
						{:else}
							<input
								type="password"
								id="confirm_password"
								name="passwordConfirm"
								bind:value={confirmPassword}
								required
								class="block w-full pl-10 pr-10 py-3 bg-white/10 border border-white/20 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-blue-300 text-white text-sm transition-all duration-300"
								placeholder="Confirm your password"
							/>
						{/if}
						<button
							type="button"
							class="absolute inset-y-0 right-0 pr-3 flex items-center"
							on:click={() => (showConfirmPassword = !showConfirmPassword)}
						>
							<!-- Eye icon SVG remains the same -->
							<svg
								class="h-5 w-5 text-blue-300 hover:text-blue-200"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								{#if showConfirmPassword}
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
									/>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
									/>
								{:else}
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
									/>
								{/if}
							</svg>
						</button>
					</div>
				</div>

				<!-- Submit Button -->
				<button
					type="submit"
					class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300"
				>
					Create Account
				</button>

				<!-- Login Link -->
				<div class="text-center mt-4">
					<p class="text-sm text-blue-200">
						Already have an account?
						<a href="/auth/login" class="font-medium text-blue-300 hover:text-blue-200">Sign in</a>
					</p>
				</div>
			</form>
		</div>
	</div>
</div>
