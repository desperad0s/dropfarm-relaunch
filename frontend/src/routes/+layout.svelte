<script lang="ts">
    import { onMount } from 'svelte';
    import Nav from '$lib/components/Nav.svelte';
    import { isAuthenticated } from '$lib/stores/auth';
    
    onMount(async () => {
        // TODO: Check authentication status
    });
</script>

<Nav />
<main>
    <slot />
</main>