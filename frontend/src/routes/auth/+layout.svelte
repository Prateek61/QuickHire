<script>
    import { blur } from 'svelte/transition';
    import { LightSwitch } from '@skeletonlabs/skeleton';
</script>

<style>
    .auth-bg {
        position: fixed;
        inset: 0;
        z-index: -1;
    }

    /* Light mode background */
    :global(.light) .auth-bg {
        background: linear-gradient(
            135deg,
            rgb(var(--color-surface-50)) 0%,
            rgb(var(--color-surface-100)) 100%
        );
    }

    :global(.light) .auth-bg::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(
            circle at 70% 30%,
            rgba(var(--color-primary-500), 0.15) 0%,
            transparent 70%
        );
    }

    /* Dark mode background */
    :global(.dark) .auth-bg {
        background: linear-gradient(
            135deg,
            rgb(0, 0, 0) 0%,
            rgba(var(--color-surface-900), 0.95) 100%
        );
    }

    :global(.dark) .auth-bg::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(
            circle at 70% 30%,
            rgba(var(--color-primary-500), 0.2) 0%,
            transparent 70%
        );
    }

    :global(.dark) .auth-bg::after {
        content: '';
        position: absolute;
        inset: 0;
        background: 
            linear-gradient(45deg, transparent 45%, rgba(var(--color-primary-500), 0.1) 50%, transparent 55%),
            linear-gradient(-45deg, transparent 45%, rgba(var(--color-primary-500), 0.1) 50%, transparent 55%);
        background-size: 300% 300%;
        animation: cyberpunkBg 15s linear infinite;
        opacity: 0.5;
    }

    @keyframes cyberpunkBg {
        0% { background-position: 0% 0%; }
        100% { background-position: 300% 300%; }
    }

    .noise {
        position: fixed;
        inset: 0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
        opacity: 0.05;
        pointer-events: none;
        z-index: -1;
    }

    .theme-toggle {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 50;
        background: rgba(var(--color-surface-500), 0.1);
        backdrop-filter: blur(8px);
        padding: 0.5rem;
        border-radius: 9999px;
        border: 1px solid rgba(var(--color-primary-500), 0.2);
        box-shadow: 0 0 15px rgba(var(--color-primary-500), 0.2);
        transition: all 0.3s ease;
    }

    .theme-toggle:hover {
        background: rgba(var(--color-surface-500), 0.15);
        border-color: rgba(var(--color-primary-500), 0.4);
        box-shadow: 0 0 20px rgba(var(--color-primary-500), 0.3);
    }

    :global(.dark) .theme-toggle {
        background: rgba(0, 0, 0, 0.3);
    }

    :global(.dark) .theme-toggle:hover {
        background: rgba(0, 0, 0, 0.4);
    }
</style>

<div class="auth-bg" in:blur={{ duration: 1000, delay: 200 }}></div>
<div class="noise"></div>

<div class="theme-toggle">
    <LightSwitch />
</div>

<main>
    <slot />
</main>