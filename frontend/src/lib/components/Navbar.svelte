<script>
	let searchQuery = "";
	import SearchIcon from '$lib/images/search.png';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';

	let activePath = '';

	onMount(() => {
		page.subscribe(($page) => {
			activePath = $page.url.pathname;
		});
	});
</script>

<nav class="flex justify-between items-center min-h-[10vh] bg-[#23486a] font-[Poppins,sans-serif]">
	<!-- Logo -->
	<span class="text-[#efb036] text-[1.6rem] mx-[20px] font-bold font-[cursive]">QuickHire</span>

	<!-- Navigation Links -->
	<ul class="flex list-none items-center">
		<li>
			<a href="/" class="text-white no-underline text-[1.1rem] mx-[10px] py-[6px] px-[15px] rounded-[5px] transition-all duration-300 ease-in-out hover:bg-[#efb036] hover:text-[#23486a] {activePath === '/' ? 'bg-[#efb036] text-[#23486a]' : ''}">Home</a>
		</li>

		{#if activePath === '/' || activePath === '/about'|| activePath === '/login'}
			<li>
				<a href="/about" class="text-white no-underline text-[1.1rem] mx-[10px] py-[6px] px-[15px] rounded-[5px] transition-all duration-300 ease-in-out hover:bg-[#efb036] hover:text-[#23486a] {activePath === '/about' ? 'bg-[#efb036] text-[#23486a]' : ''}">About</a>
			</li>
			<li>
				<a href="/login" class="text-white no-underline text-[1.1rem] mx-[10px] py-[6px] px-[15px] rounded-[5px] transition-all duration-300 ease-in-out hover:bg-[#efb036] hover:text-[#23486a] {activePath === '/login' ? 'bg-[#efb036] text-[#23486a]' : ''}">Login</a>
			</li>
		{:else}
			<li>
				<a href="/profiles" class="text-white no-underline text-[1.1rem] mx-[10px] py-[6px] px-[15px] rounded-[5px] transition-all duration-300 ease-in-out hover:bg-[#efb036] hover:text-[#23486a] {activePath === '/profiles' ? 'bg-[#efb036] text-[#23486a]' : ''}">Profiles</a>
			</li>

			<li>
				<a href="/hire" class="text-white no-underline text-[1.1rem] mx-[10px] py-[6px] px-[15px] rounded-[5px] transition-all duration-300 ease-in-out hover:bg-[#efb036] hover:text-[#23486a] {activePath === '/hire' ? 'bg-[#efb036] text-[#23486a]' : ''}">Hire</a>
			</li>
					<!-- Search Bar -->
			<div class="flex center mr-[20px]">
				<input
					type="text"
					bind:value={searchQuery}
					placeholder="Search professionals..."
					class=" h-[40px] w-[300px] border-none rounded-[20px] pl-[20px]"
				/>
				<button class="h-[40px] w-[50px] border-none bg-[#efb036] text-[#23486a] font-bold cursor-pointer rounded-tr-[20px] rounded-br-[20px] ml-[-50px]">
					<img class="ml-[12px] h-[20px] w-[20px]" src="{SearchIcon}" alt="Search Icon" />
				</button>
			</div>
		{/if}

	</ul>
</nav>
