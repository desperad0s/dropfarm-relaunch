<script lang="ts">
    import { onMount } from 'svelte';
    import { isAuthenticated } from '$lib/stores/auth';
    import { goto } from '$app/navigation';

    onMount(async () => {
        // TODO: Check authentication status
        // TODO: Redirect to login if not authenticated
    });
</script>

<div class="min-h-screen bg-background">
    <div class="container mx-auto px-4 py-8">
        <slot />
    </div>
</div>