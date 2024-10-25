<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { currentRoutine } from '$lib/stores/routines';
    import { Card, CardHeader, CardTitle, CardContent } from '$lib/components/ui/card';
    import { Button } from '$lib/components/ui/button';
    import { api } from '$lib/api';

    let loading = true;
    let error = '';
    let routineId = $page.params.id;

    onMount(async () => {
        try {
            // TODO: Load routine details
            // TODO: Update currentRoutine store
        } catch (err) {
            error = 'Failed to load routine';
        } finally {
            loading = false;
        }
    });

    async function startRoutine() {
        try {
            // TODO: Implement routine start logic
        } catch (err) {
            error = 'Failed to start routine';
        }
    }
</script>

<div class="space-y-6">
    {#if loading}
        <p>Loading routine...</p>
    {:else if error}
        <p class="text-red-500">{error}</p>
    {:else}
        <div class="flex justify-between items-center">
            <h1 class="text-3xl font-bold">{$currentRoutine?.name || 'Routine Details'}</h1>
            <Button on:click={startRoutine}>Start Routine</Button>
        </div>

        <Card>
            <CardHeader>
                <CardTitle>Routine Steps</CardTitle>
            </CardHeader>
            <CardContent>
                <!-- TODO: Implement routine steps visualization -->
            </CardContent>
        </Card>

        <!-- TODO: Add execution history -->
        <!-- TODO: Add schedule management -->
    {/if}
</div>