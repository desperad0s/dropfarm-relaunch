<script lang="ts">
    import { onMount } from 'svelte';
    import { routines } from '$lib/stores/routines';
    import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
    import { Button } from '@/components/ui/button';
    import { api } from '$lib/api';

    let loading = true;
    let error = '';

    onMount(async () => {
        try {
            // TODO: Load routines list
            // TODO: Update routines store
        } catch (err) {
            error = 'Failed to load routines';
        } finally {
            loading = false;
        }
    });
</script>

<div class="space-y-6">
    <div class="flex justify-between items-center">
        <h1 class="text-3xl font-bold">Routines</h1>
        <Button href="/routines/new">Create New Routine</Button>
    </div>

    {#if loading}
        <p>Loading routines...</p>
    {:else if error}
        <p class="text-red-500">{error}</p>
    {:else}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <!-- TODO: Implement routine cards list -->
        </div>
    {/if}
</div>