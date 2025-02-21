<script>
    import { LightSwitch } from '@skeletonlabs/skeleton';
    import { fade } from 'svelte/transition';
</script>

<div class="auth-layout fixed inset-0" in:fade={{duration: 300}}>
    <div class="auth-background fixed inset-0">
        <div class="gradient-1"></div>
        <div class="gradient-2"></div>
    </div>

    <div class="flex flex-col h-full">
        <header class="auth-header flex justify-between items-center p-6 relative z-10">
            <a href="/" class="text-2xl font-bold tracking-tight">
                QuickHire
            </a>
            <LightSwitch />
        </header>

        <main class="flex-1 relative z-10 min-h-0" style="perspective: 1500px;">
            <div class="relative w-full h-full">
                <slot />
            </div>
        </main>

        <footer class="auth-footer p-6 text-center relative z-10">
            <p class="text-sm">© {new Date().getFullYear()} QuickHire. All rights reserved.</p>
        </footer>
    </div>
</div>

<style>
    .auth-layout {
        background-color: rgb(var(--color-surface-50));
    }

    :global(.dark) .auth-layout {
        background-color: rgb(var(--color-surface-900));
    }

    .auth-background {
        z-index: 1;
        opacity: 0.8;
        pointer-events: none;
    }

    .gradient-1 {
        position: absolute;
        top: -10%;
        right: -10%;
        width: 50%;
        height: 50%;
        background: radial-gradient(circle, rgb(var(--color-primary-300)) 0%, transparent 70%);
        filter: blur(100px);
        animation: float 10s ease-in-out infinite;
    }

    .gradient-2 {
        position: absolute;
        bottom: -10%;
        left: -10%;
        width: 50%;
        height: 50%;
        background: radial-gradient(circle, rgb(var(--color-primary-900)) 0%, transparent 70%);
        filter: blur(100px);
        animation: float 15s ease-in-out infinite reverse;
    }

    @keyframes float {
        0% { transform: translate(0, 0); }
        50% { transform: translate(5%, 5%); }
        100% { transform: translate(0, 0); }
    }

    .auth-header, .auth-footer {
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        background-color: rgba(var(--color-surface-50), 0.5);
    }

    :global(.dark) .auth-header,
    :global(.dark) .auth-footer {
        background-color: rgba(var(--color-surface-900), 0.5);
    }
</style>