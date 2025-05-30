<script>
  import { onMount } from 'svelte';
	import Home from './Home.svelte'
  import Dashboard from './Dashboard.svelte';

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
{:else}
  <Home />
{/if}
