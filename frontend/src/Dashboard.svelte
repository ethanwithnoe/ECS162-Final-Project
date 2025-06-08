<script lang="ts">
	// import Dashboard from './Dashboard.svelte';
    import { onMount } from 'svelte';
    import LineChart from '../components/LineChart.svelte';

    // Mock data to test the graph
    /* 
        TODO - Sort the data here, send it to the graph component using props.
    */
       let foodData = [
        {
            "calories": 300,
            "carbohydrates": 45,
            "fat": 10,
            "protein": 20,
            "description": "Morning Oatmeal",
            "name": "Oatmeal",
            "timestamp": "2025-06-08T08:00:00.000000+00:00",
            "userid": "admin@hw3.com",
            "_id": "6844d54141d108c473d72fd9"
        },
        {
            "calories": 450,
            "carbohydrates": 60,
            "fat": 15,
            "protein": 25,
            "description": "Chicken Salad",
            "name": "Grilled Chicken Salad",
            "timestamp": "2025-06-08T10:15:00.000000+00:00",
            "userid": "admin@hw3.com",
            "_id": "6844d54141d108c473d72fd9"
        },
        {
            "calories": 150,
            "carbohydrates": 20,
            "fat": 5,
            "protein": 10,
            "description": "Apple and Peanut Butter",
            "name": "Snack",
            "timestamp": "2025-06-08T12:30:00.000000+00:00",
            "userid": "admin@hw3.com",
            "_id": "6844d54141d108c473d72fe1"
        },
        {
            "calories": 600,
            "carbohydrates": 75,
            "fat": 20,
            "protein": 40,
            "description": "Dinner – Steak and Potatoes",
            "name": "Steak Dinner",
            "timestamp": "2025-06-08T17:00:00.000000+00:00",
            "userid": "admin@hw3.com",
            "_id": "6844d54141d108c473d72fe2"
        },
        {
            "calories": 200,
            "carbohydrates": 30,
            "fat": 10,
            "protein": 15,
            "description": "Evening Smoothie",
            "name": "Smoothie",
            "timestamp": "2025-06-08T20:00:00.000000+00:00",
            "userid": "admin@hw3.com",
            "_id": "6844d54141d108c473d72fe3"
        }
    ];

    type Meal = {
        calories: number;
        carbohydrates: number;
        fat: number;
        protein: number;
        description: string;
        name: string;
        timestamp: string;
        userid: string;
        _id: string;
    };

    let selectedNutrient: keyof Meal = "calories";  // Define the default selected nutrient

    let filteredData = foodData
        .sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()) // Sort by timestamp
        .map(meal => ({
            timestamp: meal.timestamp,
            nutrientValue: meal[selectedNutrient as keyof Meal] as number,  // Assert nutrientValue is a number
        }));
    //END MOCK SECTION

    let goalValue = 2000;
    let buffer = 10;
    //END MOCK SECTION

    let userEmail = null;
    let showSidebar = false;

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
</script>

<div class="dashboard-container">
    <!-- <button onclick={redirectToDashboard}>Dashboard</button>
    <button onclick={redirectToMeals}>Meals</button>
    <button onclick={redirectToGoals}>My Goals</button>
    <button onclick={redirectToLogout}>Log Out</button> -->
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
                <small>goal placeholder</small>
            </div>

            <div class="card">
                <h3>Protein</h3>
                <p>placeholder</p>
                <small>goal placeholder</small>
            </div>

            <div class="card">
                <h3>Steps</h3>
                <p>placeholder</p>
                <small>goal placeholder</small>
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
                <h3>Today's Calories</h3>
                <LineChart {filteredData} {goalValue} {buffer} height={200} width={600} selectedNutrient={selectedNutrient} />
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

</style>
