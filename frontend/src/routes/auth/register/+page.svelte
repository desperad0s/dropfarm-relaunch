<script lang="ts">
    import { api } from '$lib/api';
    import { goto } from '$app/navigation';
    import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '$lib/components/ui/card';
    import { Input } from '$lib/components/ui/input';
    import { Button } from '$lib/components/ui/button';
    import { Label } from '$lib/components/ui/label';

    let email = '';
    let password = '';
    let confirmPassword = '';
    let error = '';

    async function handleRegister() {
        try {
            if (password !== confirmPassword) {
                error = 'Passwords do not match';
                return;
            }

            await api.auth.register(email, password);
            await goto('/auth/login');
        } catch (err) {
            error = err instanceof Error ? err.message : 'Registration failed. Please try again.';
        }
    }
</script>

<div class="container mx-auto flex items-center justify-center min-h-screen">
    <Card class="w-full max-w-md">
        <CardHeader>
            <CardTitle>Create an Account</CardTitle>
            <CardDescription>Sign up for Dropfarm</CardDescription>
        </CardHeader>
        <CardContent>
            <form on:submit|preventDefault={handleRegister} class="space-y-4">
                <div class="space-y-2">
                    <Label for="email">Email</Label>
                    <Input type="email" id="email" bind:value={email} required />
                </div>
                <div class="space-y-2">
                    <Label for="password">Password</Label>
                    <Input type="password" id="password" bind:value={password} required />
                </div>
                <div class="space-y-2">
                    <Label for="confirmPassword">Confirm Password</Label>
                    <Input type="password" id="confirmPassword" bind:value={confirmPassword} required />
                </div>
                {#if error}
                    <p class="text-red-500 text-sm">{error}</p>
                {/if}
                <Button type="submit" class="w-full">Register</Button>
            </form>
        </CardContent>
        <CardFooter class="flex justify-center">
            <a href="/auth/login" class="text-sm text-blue-600 hover:underline">
                Already have an account? Login
            </a>
        </CardFooter>
    </Card>
</div>