<script>
	// Export form action and error message
	export let errorMessage = "";

	// Import icons using unplugin-icons
	import IconUser from '~icons/mdi/account';
	import IconEmail from '~icons/mdi/email';
	import IconLock from '~icons/mdi/lock';
    import IconPhone from '~icons/mdi/phone';
</script>

<div class="flex items-center justify-center min-h-screen bg-surface-900 text-surface-50">
	<div class="bg-surface-800 p-8 rounded-lg shadow-md w-full max-w-md">
		<h1 class="text-2xl font-bold text-center text-surface-50 mb-6">Register for QuickHire</h1>

		{#if errorMessage}
			<div class="bg-error-700 text-error-50 p-3 rounded-md mb-4">
				<p>{errorMessage}</p>
			</div>
		{/if}

		<form method="POST" action="?/register" class="space-y-4">
			<!-- Username -->
			<div class="flex items-center border border-surface-700 rounded-md px-3 py-2 bg-surface-700">
				<IconUser class="w-5 h-5 text-primary-400 mr-2" />
				<input
					type="text"
					id="username"
					name="name"
					required
					placeholder="Username"
					class="w-full focus:outline-none bg-transparent text-surface-50 placeholder-surface-400"
				/>
			</div>

			<!-- Email -->
			<div class="flex items-center border border-surface-700 rounded-md px-3 py-2 bg-surface-700">
				<IconEmail class="w-5 h-5 text-primary-400 mr-2" />
				<input
					type="email"
					id="email"
					name="email"
					required
					placeholder="Email"
					class="w-full focus:outline-none bg-transparent text-surface-50 placeholder-surface-400"
				/>
			</div>

            <!-- Phone -->
            <div class="flex items-center border border-surface-700 rounded-md px-3 py-2 bg-surface-700">
                <IconPhone class="w-5 h-5 text-primary-400 mr-2" />
                <input
                    type="tel"
                    id="phone"
                    name="phone_no"
                    required
                    placeholder="Phone"
                    class="w-full focus:outline-none bg-transparent text-surface-50 placeholder-surface-400"
                />
            </div>

			<!-- Password -->
			<div class="flex items-center border border-surface-700 rounded-md px-3 py-2 bg-surface-700">
				<IconLock class="w-5 h-5 text-primary-400 mr-2" />
				<input
					type="password"
					id="password"
					name="password"
					required
					placeholder="Password"
					class="w-full focus:outline-none bg-transparent text-surface-50 placeholder-surface-400"
				/>
			</div>

			<!-- Confirm Password -->
			<div class="flex items-center border border-surface-700 rounded-md px-3 py-2 bg-surface-700">
				<IconLock class="w-5 h-5 text-primary-400 mr-2" />
				<input
					type="password"
					id="confirm_password"
					name="passwordConfirm"
					required
					placeholder="Confirm Password"
					class="w-full focus:outline-none bg-transparent text-surface-50 placeholder-surface-400"
				/>
			</div>

			<!-- Submit Button -->
			<button
				type="submit"
				class="w-full bg-primary-700 text-surface-50 py-2 rounded-md font-semibold hover:bg-primary-800 transition-colors duration-200"
			>
				Register
			</button>
		</form>
	</div>
</div>
