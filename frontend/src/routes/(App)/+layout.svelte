<script >
  import { onMount } from 'svelte';
	import { page } from '$app/stores';

	let activePath = '';

	onMount(() => {
		page.subscribe(($page) => {
			activePath = $page.url.pathname;
		});
	});

  
    import Navbar from '$lib/components/Navbar.svelte';
  
  </script>

  <style>
    :global(body) {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: Cambria, Cochin, Georgia, Times, "Times New Roman", serif;
    }
  </style>
  
{#if activePath === '/' || activePath === '/about'|| activePath === '/login'}
  <Navbar />
{/if}
  <slot />
    