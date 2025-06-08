<script lang="ts">
	// import Dashboard from './Dashboard.svelte';
    import { onMount } from 'svelte';
    onMount(() => {
        fetchInfo();
    });
    let userEmail = null;
    let showSidebar = false;
    let userGoals = {
        calories: 0,
        protein: 0,
        fat: 0,
        carbohydrates: 0
    }
    function toggleSidebar() {
        showSidebar = !showSidebar;
    }

    function redirectToDashboard() {
        window.location.href = "http://localhost:8000/dashboard";
    }

    function redirectToLogout() {
        window.location.href = "http://localhost:8000/logout";
    }

    function redirectToMeals() {
        window.location.href = "http://localhost:8000/meals";
    }

    function redirectToGoals() {
        window.location.href = "http://localhost:8000/goals";
    }

    onMount(async () => {
        const res = await fetch("/api/getinfo");
        const data = await res.json();
        if (!data.email) {
            window.location.href = "/";
        } else {
            userEmail = data.email;
        }

        setFriendsList();
    });

    async function fetchFriendsList() {
        try {
            const res = await fetch("/api/get/friendslist");
            const data = await res.json();
            return data;
        } catch (error) {
            console.log("Error fetching friends list: ", error);
        }
    }
    async function setFriendsList() {
        const FLelem = <HTMLUListElement>(
            document.getElementById("friendslist")!
        );

        // clear current list
        while (FLelem.lastElementChild) {
            FLelem.removeChild(FLelem.lastElementChild);
        }

        const friendslist = await fetchFriendsList();
        if (friendslist.result == 0) {
            for (
                let index = 0;
                index < friendslist.friendsList.length;
                index++
            ) {
                const friendInfo = friendslist.friendsList[index];
                const newEntry = <HTMLLIElement>document.createElement("li");

                newEntry.textContent = `${friendInfo[1]} (${friendInfo[0]})`;

                FLelem.appendChild(newEntry);
            }
            if (friendslist.friendsList.length == 0) {
                const newEntry = <HTMLLIElement>document.createElement("li");
                newEntry.textContent = `Your Friends List is Empty.`;
                FLelem.appendChild(newEntry);
            }
        } else {
            const newEntry = <HTMLLIElement>document.createElement("li");

            newEntry.textContent = `Error retrieving friends list`;

            FLelem.appendChild(newEntry);
        }
    }
    async function fetchInfo() {
        try {
            const res = await fetch('api/fetchgoals');
            //If fetch fails, print console error that no goals detected
            if(!res.ok) {
                console.error("No goals detected");
                return;
            }
            //Catches data from fetchgoals
            const data = await res.json();
            //Stores users stats and goals from fetchgoals in backend
            userGoals.calories =        data.calories;
            userGoals.protein =         data.protein;
            userGoals.fat =             data.fat;
            userGoals.carbohydrates =   data.carbohydrates;
        } catch (e) {               //Catches error
            console.error("No user data", e);   //Prints that user has no data saved in mongo database
        }
    }
</script>

<div class="dashboard-container">
    <!-- <button onclick={redirectToDashboard}>Dashboard</button>
    <button onclick={redirectToMeals}>Meals</button>
    <button onclick={redirectToGoals}>My Goals</button>
    <button onclick={redirectToLogout}>Log Out</button> -->
    <div class="logout">
            <button onclick={redirectToLogout}> Logout </button>
    </div>
    <div class="goals-page">
        <button onclick={redirectToGoals}> My Goals </button>
    </div>
    <button class="toggle" onclick={toggleSidebar}>Pages</button>
        <div class="top-controls">
            <div class="tabs">
                <button>Today</button>
                <button>This Week</button>
                <button>Last Month</button>
            </div>
        </div>
        <input type="text" placeholder="Search...">
        <div class="summary-cards">
            <div class="card">
                <h3>Calories</h3>
                <p>placeholder</p>
                <small>Calorie Goal: {userGoals.calories}</small>
            </div>

            <div class="card">
                <h3>Protein</h3>
                <p>placeholder</p>
                <small>Protein Goal: {userGoals.protein}</small>
            </div>

            <div class="card">
                <h3>Carbohydrates</h3>
                <p>placeholder</p>
                <small>Carbohydrate Goal: {userGoals.carbohydrates}</small>
            </div>

            <div class="card">
                <h3>Fat</h3>
                <p>placeholder</p>
                <small>Fat Goal: {userGoals.fat}</small>
            </div>
        </div>

        <div class="main-grid">
            <div class="card large">
                <h3>Today's Calories</h3>
                <div class="graph-placeholder">[Bar Graph]</div>
            </div>

            <div class="card">
                <h3>Add from My Meals</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Calories</th>
                            <th>Protein</th>
                        </tr>
                    </thead>
                    
                    <tbody>
                        <tr>
                            <th>Placeholder</th>
                            <th>Placeholder</th>
                            <th>Placeholder</th>
                        </tr>
                        <tr>
                            <th>Placeholder</th>
                            <th>Placeholder</th>
                            <th>Placeholder</th>
                        </tr>
                        <tr>
                            <th>Placeholder</th>
                            <th>Placeholder</th>
                            <th>Placeholder</th>
                        </tr>
                        <tr>
                            <th>Placeholder</th>
                            <th>Placeholder</th>
                            <th>Placeholder</th>
                        </tr>
                        <tr>
                            <th>Placeholder</th>
                            <th>Placeholder</th>
                            <th>Placeholder</th>
                        </tr>
                        <tr>
                            <th>Placeholder</th>
                            <th>Placeholder</th>
                            <th>Placeholder</th>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class=card>
                <h3>My Friends</h3>
                <ul id="friendslist">
                    <li>Name - email</li>
                    <li>Name - email</li>
                    <li>Name - email</li>
                    <li>Name - email</li>
                    <li>Name - email</li>
                    <li>Name - email</li>
                </ul>
            </div>
            <div class="card large">
                <h3>Today's Steps</h3>
                <div class="graph-placeholder">[Line Graph]</div>
            </div>
        </div>
</div>

<style>
    .dashboard-container {
        padding: 2rem;
        /* background-color: #fafafa; */
        /* background-color: #121212; */
        color: white;
        font-family: sans-serif;
    }

    /* h1 {
        font-size: 2rem;
        margin-bottom: 1.5rem;
    } */

    .top-controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        flex-wrap: wrap;
        /* background-color: #121212; */
    }

    .tabs button {
        margin-right: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: bold;
        background-color: #121212;
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
    }

    .summary-cards {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
        /* background-color: #121212; */
    }

    .main-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
    }

    .card {
        background-color: #121212;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 0 4px rgba(0, 0, 0, 0, 0.05);
    }

    .card.large {
        grid-column: span 2;
    }

    table {
        width: 100%;
        border-collapse: collapse;
    }

    th,
    td {
        text-align: left;
        padding: 0.4rem;
    }

    th {
        background-color: #121212;
        /* color: white; */
    }

    ul {
        list-style: none;
        padding: 0;
    }

    .graph-placeholder {
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #121212;
        color: white;
    }
    .logout {
        position: absolute;
        top: 1rem;
        right: 1rem;

        margin-left: 0.5rem;
        padding: 1rem 0.5rem;

        font-weight: bold;

        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
    }
</style>
