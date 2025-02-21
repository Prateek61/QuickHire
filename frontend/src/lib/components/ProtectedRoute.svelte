<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { authStore } from '$lib/auth';
    
    export let redirect = '/auth/login';
    
    onMount(() => {
        const unsubscribe = authStore.subscribe(({ isAuthenticated }) => {
            if (!isAuthenticated) {
                goto(redirect);
            }
        });
        
        return unsubscribe;
    });
</script>

<slot />