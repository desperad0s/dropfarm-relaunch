<script lang="ts">
    import { api } from '$lib/api';
    import { goto } from '$app/navigation';
    import { user, isAuthenticated } from '$lib/stores/auth';
    import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@/components/ui/card';
    import { Input } from '@/components/ui/input';
    import { Button } from '@/components/ui/button';
    import { Label } from '@/components/ui/label';

    let email = '';
    let password = '';
    let error = '';

    async function handleLogin() {
        try {
            // TODO: Implement login logic using api.auth.login
            // TODO: Set user store and isAuthenticated
            // TODO: Redirect to dashboard
        } catch (err) {
            error = 'Login failed. Please check your credentials.';
        }
    }
</script>

<div class="container mx-auto flex items-center justify-center min-h-screen">
    <Card class="w-full max-w-md">
        <CardHeader>
            <CardTitle>Login to Dropfarm</CardTitle>
            <CardDescription>Enter your credentials to access your account</CardDescription>
        </CardHeader>
        <CardContent>
            <form on:submit|preventDefault={handleLogin} class="space-y-4">
                <div class="space-y-2">
                    <Label for="email">Email</Label>
                    <Input type="email" id="email" bind:value={email} required />
                </div>
                <div class="space-y-2">
                    <Label for="password">Password</Label>
                    <Input type="password" id="password" bind:value={password} required />
                </div>
                {#if error}
                    <p class="text-red-500 text-sm">{error}</p>
                {/if}
                <Button type="submit" class="w-full">Login</Button>
            </form>
        </CardContent>
        <CardFooter class="flex justify-center">
            <a href="/auth/register" class="text-sm text-blue-600 hover:underline">
                Don't have an account? Register
            </a>
        </CardFooter>
    </Card>
</div>