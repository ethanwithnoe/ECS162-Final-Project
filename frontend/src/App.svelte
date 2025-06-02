<script lang="ts">
  import  AddFood  from "./AddFood.svelte";
  import { onMount } from "svelte";
  let showAddFood = false;
  onMount(async () => {
    // const res = await fetch('/getinfo');
    // const data = await res.json();
    // console.log(data);
    try {
      const res = await fetch("/api/getinfo");
      const data = await res.json();
      console.log(data);
    } catch (error) {
      console.error("Failed to fetch info:", error);
    }

    document
      .getElementById("TESTFORM")!
      .addEventListener("submit", function (e: SubmitEvent) {
        e.preventDefault();

        // See backend for return codes

        let form = <HTMLElement>e.target!;
        let textinput = (<HTMLInputElement>form.children[1]).value;
        makeFriend(textinput);
      });
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
      const res = await fetch("/api/getinfo");
      const data = await res.json();
      console.log(data);
    } catch (error) {
      console.error("Failed to fetch info:", error);
    }
  }

  async function testFetch() {
    try {
      const res = await fetch("/api/testfetch");
      // console.log(res);
      const data = await res.json();
      console.log(data);
    } catch (error) {
      console.error("Failed fetch test:", error);
    }
  }

  async function makeFriend(friend_email: string) {
    try {
      let postdata = new FormData();
      postdata.append("email", friend_email);

      const res = await fetch("/api/post/makefriend", {
        method: "POST",
        body: postdata,
      });
      const data = await res.json();
      console.log(data);
    } catch (error) {
      console.error("Failed to make friends:", error);
    }
  }
  async function handleFoodAdded(foodData: any) {
    console.log("Food added:", foodData);
    showAddFood = false;
  }
  async function toggleAddFood() {
    showAddFood = !showAddFood;
  }
</script>

<main>
  <button onclick={redirectToLogin}> TESTBUTTON LOGIN </button>
  <button onclick={redirectToLogout}> TESTBUTTON LOGOUT </button>
  <button onclick={getinfo}> TESTBUTTON GETINFO </button>
  <button onclick={testFetch}> TESTBUTTON TESTFETCH </button>
  <button onclick={toggleAddFood}> + </button>
  {#if showAddFood} 
    <AddFood onFoodAdded={handleFoodAdded} />
  {/if}
  <!-- See onMount for how this is implemented -->
  <form id="TESTFORM">
    <label>Friend's Email:</label>
    <input type="text" id="fname" name="fname" />
    <button type="submit">Make Friend</button>
  </form>
</main>

<style>
</style>
