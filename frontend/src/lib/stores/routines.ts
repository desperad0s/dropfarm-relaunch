import { writable } from 'svelte/store';

export const routines = writable([]);
export const currentRoutine = writable(null);

// TO-DO: Implement routines store
