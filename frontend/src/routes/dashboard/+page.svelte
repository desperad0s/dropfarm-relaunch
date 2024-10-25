<script lang="ts">
    import { onMount } from 'svelte';
    import { routines, currentRoutine } from '$lib/stores/routines';
    import { schedules } from '$lib/stores/schedules';
    import { Card, CardHeader, CardTitle, CardContent } from '$lib/components/ui/card';
    import { Button } from '$lib/components/ui/button';
    import StatsWidget from '$lib/components/StatsWidget.svelte';

    let stats = {
        activeRoutines: 0,
        scheduledTasks: 0,
        successRate: 0,
    };

    onMount(async () => {
        // TODO: Load dashboard data
        // TODO: Initialize stats
    });
</script>

<div class="space-y-6">
    <h1 class="text-3xl font-bold">Dashboard</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatsWidget {stats} />
        
        <Card>
            <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent>
                <div class="space-y-2">
                    <Button class="w-full" href="/routines/new">Create New Routine</Button>
                    <Button class="w-full" href="/schedules">Manage Schedules</Button>
                </div>
            </CardContent>
        </Card>
    </div>
    
    <!-- TODO: Add recent activity list -->
    <!-- TODO: Add active routines overview -->
</div>
