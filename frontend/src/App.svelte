<script lang="ts">
  import { onMount } from 'svelte';
  import Home from './Home.svelte';
  import Dashboard from './Dashboard.svelte';
  import Meals from './Meals.svelte';
  import Goals from './Goals.svelte';
  import AddFood from './AddFood.svelte';

  let currentPath = window.location.pathname;
  let loggedIn = false;
  onMount(async () => {
    const res = await fetch("/api/getinfo");
    const data = await res.json();
    loggedIn = !!data.email;

    if(currentPath === "/dashboard" && !loggedIn){
      window.location.href = '/';
    }
  });
</script>

{#if currentPath === '/dashboard' && loggedIn}
  <Dashboard />
{:else if currentPath === '/meals' && loggedIn}
  <Meals />
{:else if currentPath === '/goals' && loggedIn}
  <Goals />
{:else}
  <Home />
{/if}