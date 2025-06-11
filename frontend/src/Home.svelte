<script lang="ts">
    import AddFood from "./AddFood.svelte";
    import { onMount } from "svelte";
    import Logo from "../assets/Logo.png";
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

        // document
        //     .getElementById("TESTFORM")!
        //     .addEventListener("submit", function (e: SubmitEvent) {
        //         e.preventDefault();

        //         // See backend for return codes

        //         let form = <HTMLElement>e.target!;
        //         let textinput = (<HTMLInputElement>form.children[1]).value;
        //         makeFriend(textinput);
        //     });
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
            const res = await fetch(
                `/api/getuserfoods?range=${encodeURIComponent("custom")}&earliest=${encodeURIComponent("2025-05-09")}`,
            );
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
        <img src={Logo} alt="Logo" class="logo" />
        <h1 class="title">Opter Meal Tracker</h1>
        <h2 class="subtitle">Opt into a healthier life style</h2>
        <h3 class="login-prompt">
            Please <span onclick={redirectToLogin}> Login </span> to Continue.
        </h3>
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
    @import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap");

    .home-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        width: 100%;
        background-color: #ffffff; /* changed background to white */
        flex-direction: column;
        color: #000; /* black text */
        text-align: center;
        overflow: hidden;
        font-family: "Inter", sans-serif;
    }

    .logo {
        width: 250px;
    }

    h1.title {
        font-size: 3rem;
        margin: 0 0 0 0;
    }

    h2.subtitle {
        font-size: 1.5rem;
        font-weight: 400;
        margin: 0 0 0 0;
    }

    h3.login-prompt {
        font-size: 1.2rem;
        font-weight: 500;
        margin: 1;
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
        color: blue; /* Blue text */
        cursor: pointer;
        transition: color 0.2s ease;
    }

    span:hover {
        color: #104e8b; /* Darker blue on hover */
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
