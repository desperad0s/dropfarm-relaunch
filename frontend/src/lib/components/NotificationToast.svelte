<script lang="ts">
    export let message: string;
    export let type: 'success' | 'error' | 'info' = 'info';
</script>

<div class="toast" class:success={type === 'success'} class:error={type === 'error'}>
    {message}
</div>

<style>
    .toast {
        /* TODO: Add toast styles */
    }