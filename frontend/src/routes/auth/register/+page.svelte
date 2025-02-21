<script>
    import { page } from '$app/stores';
    import { focusTrap } from '@skeletonlabs/skeleton';
    import { fade, fly, scale } from 'svelte/transition';
    import { quintIn, quintOut, elasticOut } from 'svelte/easing';
    import { onMount } from 'svelte';
    
    export let form;
    $: errorMessage = form?.error;
    
    let mounted = false;
    onMount(() => {
        mounted = true;
    });
</script>

<style>
    /* Light mode styles */
    :global(.light) .auth-card {
        box-shadow: 0 0 25px rgba(var(--color-primary-500), 0.3);
        border: 2px solid rgba(var(--color-primary-500), 0.3);
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(12px);
    }
    
    :global(.light) .input {
        transition: all 0.3s ease;
        border: 2px solid rgba(var(--color-primary-500), 0.4);
        background: rgba(255, 255, 255, 0.9);
        box-shadow: 0 0 15px rgba(var(--color-primary-500), 0.1);
        color: rgb(var(--color-surface-900));
        padding: 0.75rem 1rem;
        letter-spacing: 0.5px;
    }
    
    :global(.light) .input:focus {
        box-shadow: 0 0 25px rgba(var(--color-primary-500), 0.2);
        border-color: rgb(var(--color-primary-500));
        background: white;
    }

    :global(.light) .input:hover {
        border-color: rgb(var(--color-primary-500));
        background: white;
    }

    :global(.light) .input::placeholder {
        color: rgba(0, 0, 0, 0.4);
    }

    /* Dark mode styles */
    :global(.dark) .auth-card {
        box-shadow: 0 0 25px rgba(var(--color-primary-500), 0.4);
        border: 2px solid rgba(var(--color-primary-500), 0.3);
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(12px);
    }
    
    :global(.dark) .input {
        transition: all 0.3s ease;
        border: 2px solid rgba(var(--color-primary-500), 0.5);
        background: rgba(0, 0, 0, 0.6);
        box-shadow: 0 0 15px rgba(var(--color-primary-500), 0.15),
                   inset 0 0 20px rgba(var(--color-primary-500), 0.05);
        color: rgb(var(--color-primary-200));
        padding: 0.75rem 1rem;
        letter-spacing: 0.5px;
    }
    
    :global(.dark) .input:focus {
        box-shadow: 0 0 25px rgba(var(--color-primary-500), 0.4),
                   inset 0 0 20px rgba(var(--color-primary-500), 0.15);
        border-color: rgb(var(--color-primary-400));
        background: rgba(0, 0, 0, 0.8);
        color: rgb(var(--color-primary-100));
    }

    :global(.dark) .input:hover {
        border-color: rgba(var(--color-primary-400), 0.8);
        background: rgba(0, 0, 0, 0.7);
        box-shadow: 0 0 20px rgba(var(--color-primary-500), 0.25),
                   inset 0 0 20px rgba(var(--color-primary-500), 0.1);
    }

    :global(.dark) .input::placeholder {
        color: rgba(var(--color-primary-400), 0.5);
    }

    /* Common styles */
    .auth-card {
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .auth-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(
            circle,
            rgba(var(--color-primary-500), 0.1) 0%,
            transparent 60%
        );
        animation: rotate 15s linear infinite;
        z-index: 0;
    }
    
    .auth-card > * {
        position: relative;
        z-index: 1;
    }

    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .label span {
        color: rgb(var(--color-primary-500));
        text-shadow: 0 0 8px rgba(var(--color-primary-500), 0.4);
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    .btn {
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border-width: 2px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .btn.variant-filled-primary {
        box-shadow: 0 0 20px rgba(var(--color-primary-500), 0.4);
        text-shadow: 0 0 10px rgba(var(--color-primary-500), 0.6);
        position: relative;
        overflow: hidden;
    }
    
    .btn.variant-filled-primary:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 30px rgba(var(--color-primary-500), 0.6),
                   0 0 15px rgba(var(--color-primary-500), 0.4) inset;
        text-shadow: 0 0 20px rgba(var(--color-primary-500), 1);
    }

    .btn.variant-filled-primary::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent,
            rgba(var(--color-primary-500), 0.2),
            transparent
        );
        transform: translateX(-100%);
        transition: transform 0.6s;
    }

    .btn.variant-filled-primary:hover::after {
        transform: translateX(100%);
    }

    .neon-text {
        text-shadow: 0 0 15px rgba(var(--color-primary-500), 0.7),
                    0 0 30px rgba(var(--color-primary-500), 0.4);
        animation: glow 2s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { 
            filter: brightness(1); 
            text-shadow: 0 0 15px rgba(var(--color-primary-500), 0.7),
                        0 0 30px rgba(var(--color-primary-500), 0.4);
        }
        50% { 
            filter: brightness(1.3); 
            text-shadow: 0 0 20px rgba(var(--color-primary-500), 0.9),
                        0 0 40px rgba(var(--color-primary-500), 0.6);
        }
    }

    .neon-border {
        border: 2px solid rgb(var(--color-primary-500));
        box-shadow: 0 0 15px rgba(var(--color-primary-500), 0.3);
        opacity: 0.7;
        animation: borderGlow 2s ease-in-out infinite;
    }

    @keyframes borderGlow {
        0%, 100% { 
            box-shadow: 0 0 15px rgba(var(--color-primary-500), 0.3);
            border-color: rgba(var(--color-primary-500), 0.8);
            opacity: 0.7;
        }
        50% { 
            box-shadow: 0 0 25px rgba(var(--color-primary-500), 0.5);
            border-color: rgb(var(--color-primary-500));
            opacity: 1;
        }
    }

    .social-btn {
        transition: all 0.3s ease;
        border: 2px solid rgba(var(--color-primary-500), 0.3);
    }

    .social-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px rgba(var(--color-primary-500), 0.3);
        border-color: rgba(var(--color-primary-500), 0.6);
    }

    .divider-text {
        text-shadow: 0 0 10px rgba(var(--color-primary-500), 0.4);
    }

    .checkbox {
        border: 2px solid rgba(var(--color-primary-500), 0.4);
        transition: all 0.3s ease;
    }

    .checkbox:checked {
        box-shadow: 0 0 15px rgba(var(--color-primary-500), 0.4);
    }
</style>

<div class="absolute inset-0 flex items-start justify-center p-4 overflow-y-auto">
    <div class="auth-card w-full max-w-md p-8 my-8 rounded-container-token"
        style="transform-style: preserve-3d; backface-visibility: hidden;"
        in:fly="{{
            x: -500,
            y: 0,
            duration: 1000,
            delay: 300,
            easing: elasticOut,
            opacity: 1,
            scale: 1,
            rotate: 0
        }}"
        out:fly="{{
            x: 500,
            y: 100,
            duration: 600,
            easing: quintIn,
            opacity: 0.2,
            scale: 0.85,
            rotate: 5
        }}">
        {#if mounted}
            <header class="text-center mb-8"
                in:fly="{{ y: -20, duration: 500, delay: 500 }}">
                <h1 class="h1 font-bold mb-2 neon-text"
                    in:scale="{{ duration: 400, delay: 800 }}">
                    Create Account
                </h1>
                <p class="text-surface-600-300-token divider-text"
                    in:fade="{{ duration: 400, delay: 1000 }}">
                    Join QuickHire today
                </p>
            </header>

            {#if errorMessage}
                <div class="alert variant-filled-error mb-6 p-4" role="alert"
                    in:fly="{{ y: -20, duration: 300, delay: 200 }}">
                    <p>{errorMessage}</p>
                </div>
            {/if}

            <form method="POST" class="space-y-6" use:focusTrap={true}
                in:fly="{{ y: 20, duration: 600, delay: 500, easing: elasticOut }}">
                <div class="grid grid-cols-2 gap-4" in:fly="{{ y: 20, duration: 400, delay: 600 }}">
                    <label class="label">
                        <span>First Name</span>
                        <input
                            type="text"
                            name="firstName"
                            class="input"
                            placeholder="First name"
                            value={form?.firstName ?? ''}
                        />
                    </label>

                    <label class="label">
                        <span>Last Name</span>
                        <input
                            type="text"
                            name="lastName"
                            class="input"
                            placeholder="Last name"
                            value={form?.lastName ?? ''}
                        />
                    </label>
                </div>

                <label class="label" in:fly="{{ y: 20, duration: 400, delay: 700 }}">
                    <span>Email</span>
                    <input
                        type="email"
                        name="email"
                        class="input"
                        placeholder="your.email@example.com"
                        value={form?.username ?? ''}
                        required
                    />
                </label>

                <label class="label" in:fly="{{ y: 20, duration: 400, delay: 800 }}">
                    <span>Phone</span>
                    <input
                        type="tel"
                        name="phone"
                        class="input"
                        placeholder="Phone number"
                        value={form?.phone ?? ''}
                    />
                </label>

                <label class="label" in:fly="{{ y: 20, duration: 400, delay: 900 }}">
                    <span>Password</span>
                    <input
                        type="password"
                        name="password"
                        class="input"
                        placeholder="Create a password"
                        required
                    />
                </label>

                <label class="label" in:fly="{{ y: 20, duration: 400, delay: 1000 }}">
                    <span>Confirm Password</span>
                    <input
                        type="password"
                        name="confirmPassword"
                        class="input"
                        placeholder="Confirm your password"
                        required
                    />
                </label>

                <div in:fly="{{ y: 20, duration: 400, delay: 1100 }}">
                    <label class="flex items-center space-x-3 cursor-pointer">
                        <input type="checkbox" class="checkbox" required />
                        <span class="text-sm divider-text">
                            I agree to the <a href="/terms" class="anchor hover:underline hover:text-primary-400">Terms of Service</a> 
                            and <a href="/privacy" class="anchor hover:underline hover:text-primary-400">Privacy Policy</a>
                        </span>
                    </label>
                </div>

                <button type="submit"
                    class="btn variant-filled-primary w-full"
                    in:scale="{{ duration: 400, delay: 1200 }}">
                    Create Account
                </button>

                <hr class="neon-border my-8" in:fade="{{ duration: 400, delay: 1300 }}" />
                <div class="text-center -mt-7">
                    <span class="px-4 py-1 text-sm bg-surface-900 rounded-full divider-text">
                        Or continue with
                    </span>
                </div>

                <div class="grid grid-cols-2 gap-4" in:fly="{{ y: 20, duration: 400, delay: 1400 }}">
                    <button
                        type="button"
                        class="btn variant-soft flex items-center justify-center gap-2 social-btn"
                    >
                        <svg class="h-5 w-5" viewBox="0 0 24 24">
                            <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                            <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                            <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                            <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                        </svg>
                        <span>Google</span>
                    </button>
                    <button
                        type="button"
                        class="btn variant-soft flex items-center justify-center gap-2 social-btn"
                    >
                        <svg class="h-5 w-5" viewBox="0 0 24 24">
                            <path fill="currentColor" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z"/>
                        </svg>
                        <span>Facebook</span>
                    </button>
                </div>

                <div class="text-center" in:fly="{{ y: 20, duration: 400, delay: 1500 }}">
                    <p class="text-surface-600-300-token mb-4 divider-text">Already have an account?</p>
                    <a 
                        href="/auth/login"
                        class="btn variant-ringed-primary w-full hover:variant-filled-primary transition-all duration-300"
                    >
                        Sign In
                    </a>
                </div>
            </form>
        {/if}
    </div>
</div>
