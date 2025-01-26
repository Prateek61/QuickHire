<script>
    // Import favicon.png
    import favicon from "$lib/images/favicon.png"

	export let username = "Username";
</script>

<nav class="flex justify-between items-center bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white p-4 shadow-lg">
	<div class="flex items-center space-x-4">
		<img src={favicon} alt="QuickHire Logo" class="w-10 h-10 rounded-full shadow-md">
		<span class="text-2xl font-extrabold tracking-wide">QuickHire</span>
	</div>
	<ul class="flex space-x-6 text-lg">
		<li>
			<a href="/" class="hover:text-yellow-300 transition-colors duration-200 ease-in-out">Home</a>
		</li>
		<li>
			<a href="/professionals" class="hover:text-yellow-300 transition-colors duration-200 ease-in-out">Professionals</a>
		</li>
		<li>
			<a href="/dashboard" class="hover:text-yellow-300 transition-colors duration-200 ease-in-out">Dashboard</a>
		</li>
		<li>
			<a href="/logout" class="hover:text-yellow-300 transition-colors duration-200 ease-in-out">Logout</a>
		</li>
	</ul>
	<div class="bg-white text-gray-800 px-4 py-2 rounded-full shadow-md font-semibold">
		<span>{username}</span>
	</div>
</nav>
