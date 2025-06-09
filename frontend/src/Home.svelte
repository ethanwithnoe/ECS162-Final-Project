<script lang="ts">
    import  AddFood  from "./AddFood.svelte";
    import { onMount } from "svelte";
    //   import Dashboard from './Dashboard.svelte';

    let showAddFood = false;
    onMount(async () => {
        // const res = await fetch('/getinfo');
        // const data = await res.json();
        // console.log(data);
        let userEmail = null;
        let loggedIn = false;
        try {
            const res = await fetch("/api/getinfo");
            const data = await res.json();
            console.log(data);
            if (data.email) {
                loggedIn = true;
                userEmail = data.email;
            }
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

    // function goToDashboard() {
    //     window.location.href = '/dashboard';
    // }

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
    async function getFoodList() {
        try {
            const res = await fetch(`/api/getuserfoods?range=${encodeURIComponent("custom")}&earliest=${encodeURIComponent("2025-05-09")}`);
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

    let currentRoute = window.location.pathname;
    async function handleFoodAdded(foodData: any) {
        console.log("Food added:", foodData);
        showAddFood = false;
    }
    async function toggleAddFood() {
        showAddFood = !showAddFood;
    }
</script>

<main>
    <div class="home-container">
        <h1 class="welcome">Welcome to Our Meal Tracker! We Help Users Track Their Daily Calories, Protein, Carbohydrates, and Fat Intake For The Day. Please <span onclick={redirectToLogin}> Login </span> to Continue.</h1>
        <!-- <div class="button-row">
            <button onclick={redirectToLogin}> TESTBUTTON LOGIN </button>
            <button onclick={redirectToLogout}> TESTBUTTON LOGOUT </button>
            <button onclick={getinfo}> TESTBUTTON GETINFO </button>
            <button onclick={testFetch}> TESTBUTTON TESTFETCH </button>
            <button onclick={getFoodList}> TESTBUTTON GETFOODLIST </button>
            <button onclick={toggleAddFood}> + </button>
            {#if showAddFood}
                <AddFood onFoodAdded={handleFoodAdded} />
            {/if}
        </div>
        <!- See onMount for how this is implemented --
        <div class="form-row">
            <form id="TESTFORM">
                <label>Friend's Email:</label>
                <input type="text" id="fname" name="fname" />
                <button type="submit">Make Friend</button>
            </form>
        </div> -->
    </div>
</main>

<style>
    .home-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        width: 100%;
        background-color: #1e1e1e;
        flex-direction: column;
        color: #fff;
        text-align: center;
        overflow: hidden;
    }

    h1 {
        font-size: 3rem;
        margin-bottom: 2rem;
        width: 75%;
    }

    .button-row {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin-bottom: 2rem;
        justify-content: center;
    }

    span {
        text-decoration: underline;
        /* color:#666; */
    }

    span:hover{
        background-color: #2a2a2a;
        cursor: pointer;
        color: #ccc;
    }

    button {
        background-color: #121212;
        color: white;
        border: none;
        padding: 0.7em 1.2em;
        border-radius: 6px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.2s ease;
    }

    button:hover {
        background-color: #2a2a2a;
    }

    .form-row {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    input[type="email"] {
        padding: 0.5em;
        border-radius: 4px;
        border: 1px solid #666;
        background-color: #2a2a2a;
        color: white;
    }

    label {
        margin-right: 0.5rem;
        font-weight: 500;
    }
</style>
