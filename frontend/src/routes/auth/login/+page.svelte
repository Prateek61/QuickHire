<script>
import { goto } from '$app/navigation';

// Import icons using unplugin-icons
import IconEmail from '~icons/mdi/email';
import IconLock from '~icons/mdi/lock';

/** @type {import('./$types').PageData} */
export let data;

let errorMessage = "";
let loading = false;

async function handleSubmit(event) {
    event.preventDefault();
    loading = true;
    errorMessage = "";

    const formData = new FormData(event.target);
    const email = formData.get('email');
    const password = formData.get('password');

    const result = await data.loginAction({ email, password });
    
    if (result.success) {
        goto('/');
    } else {
        errorMessage = result.error;
    }
    
    loading = false;
}
</script>

<div class="flex items-center justify-center min-h-screen bg-surface-900 text-surface-50">
<div class="bg-surface-800 p-8 rounded-lg shadow-md w-full max-w-md">
<h1 class="text-2xl font-bold text-center text-surface-50 mb-6">Login to QuickHire</h1>

{#if errorMessage}
<div class="bg-error-700 text-error-50 p-3 rounded-md mb-4">
<p>{errorMessage}</p>
</div>
{/if}

<form on:submit={handleSubmit} class="space-y-4">
<div class="flex items-center border border-surface-700 rounded-md px-3 py-2 bg-surface-700">
<IconEmail class="w-5 h-5 text-primary-400 mr-2" />
<input
    type="text"
    id="email"
    name="email"
    required
    placeholder="Email"
    class="w-full focus:outline-none bg-transparent text-surface-50 placeholder-surface-400"
/>
</div>

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

<button
    type="submit"
    class="w-full bg-primary-700 text-surface-50 py-2 rounded-md font-semibold hover:bg-primary-800 transition-colors duration-200"
    disabled={loading}
>
    {loading ? 'Logging in...' : 'Login'}
</button>
</form>
</div>
</div>
