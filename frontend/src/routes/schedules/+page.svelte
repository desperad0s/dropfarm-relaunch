<script lang="ts">
    import { onMount } from 'svelte';
    import { schedules } from '$lib/stores/schedules';
    import { Card, CardHeader, CardTitle, CardContent } from '$lib/components/ui/card';
    import { Button } from '$lib/components/ui/button';
    import { api } from '$lib/api';

    let loading = true;
    let error = '';

    onMount(async () => {
        try {
            // TODO: Load schedules list
            // TODO: Update schedules store
        } catch (err) {
            error = 'Failed to load schedules';
        } finally {
            loading = false;
        }
    });
</script>

<div class="space-y-6">
    <div class="flex justify-between items-center">
        <h1 class="text-3xl font-bold">Schedules</h1>
        <Button href="/schedules/new">Create New Schedule</Button>
    </div>

    {#if loading}
        <p>Loading schedules...</p>
    {:else if error}
        <p class="text-red-500">{error}</p>
    {:else}
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <!-- TODO: Implement schedule cards list -->
        </div>
    {/if}
</div>