<script>
    import '../app.postcss';

    import { computePosition, autoUpdate, flip, shift, offset, arrow } from '@floating-ui/dom';
    import { storePopup, initializeStores, AppShell } from '@skeletonlabs/skeleton';
    storePopup.set({ computePosition, autoUpdate, flip, shift, offset, arrow }); 

    // Initialize the stores
    initializeStores();
</script>

<AppShell>
    <slot />
</AppShell>
