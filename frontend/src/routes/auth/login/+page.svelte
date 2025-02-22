<script>
	import { goto } from '$app/navigation';
	import IconEmail from '~icons/mdi/email';
	import IconLock from '~icons/mdi/lock';
	import IconHome from '~icons/mdi/home';

	/** @type {import('./$types').PageData} */
	export let data;

	let errorMessage = '';
	let loading = false;
	let showPassword = false;

	async function handleSubmit(event) {
		event.preventDefault();
		loading = true;
		errorMessage = '';

		const formData = new FormData(event.target);
		const email = formData.get('email');
		const password = formData.get('password');

		try {
			const result = await data.loginAction({ email, password });
			if (result.success) {
				goto('/');
			} else {
				errorMessage = result.error;
			}
		} catch (error) {
			errorMessage = 'An unexpected error occurred. Please try again.';
		} finally {
			loading = false;
		}
	}
</script>

<div
	class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-900 via-blue-800 to-blue-900 py-12 px-4 sm:px-6 lg:px-8"
>
	<a
		href="/"
		class="absolute top-4 left-4 flex items-center justify-center p-2 bg-white/10 hover:bg-white/20 rounded-lg backdrop-blur-lg border border-white/20 transition-all duration-300"
	>
		<IconHome class="h-6 w-6 text-white" />
	</a>
	<div class="w-full max-w-md space-y-8">
		<!-- Logo and Title -->
		<div class="text-center">
			<h2 class="text-4xl font-bold text-white mb-2">Welcome Back</h2>
			<p class="text-blue-200">Log in to your QuickHire account</p>
		</div>

		<!-- Main Card -->
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

			<form on:submit={handleSubmit} class="space-y-6">
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

				<!-- Password Input -->
				<div class="space-y-2">
					<label for="password" class="block text-sm font-medium text-blue-200">Password</label>
					<div class="relative">
						<div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
							<IconLock class="h-5 w-5 text-blue-300" />
						</div>
						<input
							type={showPassword ? 'text' : 'password'}
							id="password"
							name="password"
							required
							class="block w-full pl-10 pr-10 py-3 bg-white/10 border border-white/20 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-blue-300 text-white text-sm transition-all duration-300"
							placeholder="Enter your password"
						/>
						<button
							type="button"
							class="absolute inset-y-0 right-0 pr-3 flex items-center"
							on:click={() => (showPassword = !showPassword)}
						>
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
				</div>

				<!-- Login Button -->
				<button
					type="submit"
					class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
					disabled={loading}
				>
					{#if loading}
						<svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
							<circle
								class="opacity-25"
								cx="12"
								cy="12"
								r="10"
								stroke="currentColor"
								stroke-width="4"
							/>
							<path
								class="opacity-75"
								fill="currentColor"
								d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
							/>
						</svg>
						Logging in...
					{:else}
						Sign in
					{/if}
				</button>
			</form>

			<!-- Sign Up Link -->
			<div class="mt-6 text-center">
				<p class="text-sm text-blue-200">
					Don't have an account?
					<a href="/auth/register" class="font-medium text-blue-300 hover:text-blue-200"
						>Sign up now</a
					>
				</p>
			</div>
		</div>
	</div>
</div>
