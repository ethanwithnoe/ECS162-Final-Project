<script lang="ts">
  import { onMount } from 'svelte';
  
  onMount(async () => {
    // const res = await fetch('/getinfo');
    // const data = await res.json();
    // console.log(data);
    try {
      const res = await fetch('/api/getinfo');
      const data = await res.json();
      console.log(data);
    } catch (error) {
      console.error('Failed to fetch info:', error);
    }
  }); 
  /**
   * function to redirect to the login page
   */
  function redirectToLogin() {
    window.location.href = "http://localhost:8000/login";
  }
  /**
   * function to redirect to the logout page
   */
  function redirectToLogout() {
    window.location.href = "http://localhost:8000/logout";
  }
  
  
  async function getinfo() {
    try {
      const res = await fetch('/api/getinfo');
      const data = await res.json();
      console.log(data);
    } catch (error) {
      console.error('Failed to fetch info:', error);
    }
  }

  async function testFetch() {
    try {
      const res = await fetch('/api/testfetch');
      // console.log(res);
      const data = await res.json();
      console.log(data);
    } catch (error) {
      console.error('Failed fetch test:', error);
    }
  }
</script>

<main>
  <button onclick={redirectToLogin}>
    TESTBUTTON LOGIN
  </button>
  <button onclick={redirectToLogout}>
    TESTBUTTON LOGOUT
  </button>
  <button onclick={getinfo}>
    TESTBUTTON GETINFO
  </button>
  <button onclick={testFetch}>
    TESTBUTTON TESTFETCH
  </button>
  
</main>

<style>
  
</style>
