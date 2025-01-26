<script>
    import Navbar from "./Navbar.svelte"
</script>

<header>
    <Navbar isAuthenticated={false}/>
</header>
<main>
    <slot />
</main>