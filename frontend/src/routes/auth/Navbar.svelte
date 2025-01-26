<script>
    import favicon from "$lib/images/favicon.png"

	export let isAuthenticated = false;
</script>

<nav class="flex justify-between items-center bg-gradient-to-r from-teal-400 via-blue-500 to-purple-600 text-white p-4 shadow-lg">
	<div class="flex items-center space-x-4">
		<img src={favicon} alt="QuickHire Logo" class="w-10 h-10 rounded-full shadow-md">
		<span class="text-2xl font-extrabold tracking-wide">QuickHire</span>
	</div>
	<ul class="flex space-x-6 text-lg">
		{#if isAuthenticated}
			<li>
				<a href="/auth/logout" class="hover:text-yellow-300 transition-colors duration-200 ease-in-out">Logout</a>
			</li>
		{:else}
			<li>
				<a href="/auth/login" class="hover:text-yellow-300 transition-colors duration-200 ease-in-out">Login</a>
			</li>
			<li>
				<a href="/auth/register" class="hover:text-yellow-300 transition-colors duration-200 ease-in-out">Register</a>
			</li>
		{/if}
	</ul>
</nav>
