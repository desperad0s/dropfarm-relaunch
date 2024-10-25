<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import { currentSchedule } from '$lib/stores/schedules';
    import { Card, CardHeader, CardTitle, CardContent } from '$lib/components/ui/card';
    import { Button } from '$lib/components/ui/button';
    import { api } from '$lib/api';

    let loading = true;
    let error = '';
    let scheduleId = $page.params.id;

    onMount(async () => {
        try {
            // TODO: Load schedule details
            // TODO: Update currentSchedule store
        } catch (err) {
            error = 'Failed to load schedule';
        } finally {
            loading = false;
        }
    });

    async function toggleSchedule() {
        try {
            // TODO: Implement schedule toggle logic
        } catch (err) {
            error = 'Failed to update schedule';
        }
    }
</script>

<div class="space-y-6">
    {#if loading}
        <p>Loading schedule...</p>
    {:else if error}
        <p class="text-red-500">{error}</p>
    {:else}
        <div class="flex justify-between items-center">
            <h1 class="text-3xl font-bold">Schedule Details</h1>
            <Button on:click={toggleSchedule}>
                {$currentSchedule?.is_active ? 'Disable' : 'Enable'} Schedule
            </Button>
        </div>

        <Card>
            <CardHeader>
                <CardTitle>Schedule Configuration</CardTitle>
            </CardHeader>
            <CardContent>
                <!-- TODO: Implement schedule configuration form -->
            </CardContent>
        </Card>

        <!-- TODO: Add execution history -->
        <!-- TODO: Add routine details reference -->
    {/if}
</div>