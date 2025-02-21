<script>
    import '../app.postcss';
    import { onMount } from 'svelte';
    import { AppShell, AppBar, LightSwitch, Avatar } from '@skeletonlabs/skeleton';
    import { setModeCurrent } from '@skeletonlabs/skeleton';
    import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
    import { storePopup } from '@skeletonlabs/skeleton';
    import { authStore, auth } from '$lib/auth';
    
    storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow });
    
    export let data;
    
    onMount(() => {
        // Set the initial theme
        setModeCurrent('modern');

        if (data?.user) {
            authStore.update(state => ({
                ...state,
                user: data.user,
                token: data.token,
                isAuthenticated: true
            }));
        }
        
        if (data?.token) {
            localStorage.setItem('token', data.token);
        }
    });

    function handleLogout() {
        auth.logout();
    }
</script>

<!-- App Shell -->
<AppShell>
    <div slot="header">
        {#if $authStore.isAuthenticated}
            <AppBar class="px-4">
                <svelte:fragment slot="lead">
                    <a href="/" class="text-xl font-bold">QuickHire</a>
                </svelte:fragment>
                <svelte:fragment slot="trail">
                    <a href="/dashboard" class="btn btn-sm variant-ghost-surface">
                        Dashboard
                    </a>
                    <a href="/jobs" class="btn btn-sm variant-ghost-surface">
                        Jobs
                    </a>
                    <div class="divider-vertical mx-4" />
                    <LightSwitch />
                    <div class="relative group">
                        <button class="btn btn-sm variant-ghost-surface">
                            {#if $authStore.user?.first_name}
                                <Avatar 
                                    initials={`${$authStore.user.first_name[0]}${$authStore.user.last_name?.[0] || ''}`}
                                    background="bg-primary-500"
                                />
                            {:else}
                                <Avatar initials="U" background="bg-primary-500" />
                            {/if}
                        </button>
                        <nav class="card absolute right-0 top-full hidden group-hover:block w-48 p-2 shadow-xl z-50">
                            <a 
                                href="/profile" 
                                class="block px-4 py-2 hover:bg-surface-hover-token rounded-token no-underline"
                            >
                                Profile
                            </a>
                            <div class="divider my-2" />
                            <button 
                                on:click={handleLogout}
                                class="w-full text-left px-4 py-2 hover:bg-surface-hover-token rounded-token text-error-500"
                            >
                                Logout
                            </button>
                        </nav>
                    </div>
                </svelte:fragment>
            </AppBar>
        {/if}
    </div>

    <slot />
</AppShell>
