import { writable } from 'svelte/store';

export const schedules = writable([]);
export const currentSchedule = writable(null);

// TO-DO: Implement schedules store