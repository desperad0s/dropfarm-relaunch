<script lang="ts">
    import { routines } from '$lib/stores/routines';
    import { schedules } from '$lib/stores/schedules';
    import { isAuthenticated } from '$lib/stores/auth';
</script>

<nav class="bg-white shadow">
    <div class="container mx-auto px-4">
        <div class="flex justify-between h-16">
            <div class="flex">
                <a href="/" class="flex items-center">Dropfarm</a>
                
                {#if $isAuthenticated}
                    <a href="/dashboard" class="ml-8">Dashboard</a>
                    <a href="/routines" class="ml-4">Routines</a>
                    <a href="/schedules" class="ml-4">Schedules</a>
                {/if}
            </div>
            
            <div class="flex items-center">
                {#if $isAuthenticated}
                    <button class="ml-4">Logout</button>
                {:else}
                    <a href="/auth/login">Login</a>
                    <a href="/auth/register" class="ml-4">Register</a>
                {/if}
            </div>
        </div>
    </div>
</nav>