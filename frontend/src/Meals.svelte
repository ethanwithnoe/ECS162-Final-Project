<script lang="ts">
	// import Dashboard from './Dashboard.svelte';
    import { onMount } from 'svelte';
    import  AddFood  from "./AddFood.svelte";
    let showSidebar = false;
    let showAddFood = false;
    let meals = [];
    let error = "";

    async function loadMeals() {
        try {
            const res = await fetch("/api/getuserfoods", {credentials: "include"});
            const data = await res.json();
            if(data.result === 0) {
                meals = data.foodList;
            } else {
                error = "Please Login to View Your Meals."
            }
        } catch (err) {
            error = "Error loading meals."
            console.log(error);
        }
    }

    async function repeatFood(meal: any) {
        try {
            const foodData = {
                name: meal.name,
                brand: meal.brand || "",
                calories: meal.calories,
                protein: meal.protein,
                fat: meal.fat,
                carbohydrates: meal.carbohydrates,
            };

            const res = await fetch("/api/addfood", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(foodData),});
            const data = await res.json();
            if (res.ok){
                console.log("Food added again:", data);
                await loadMeals();
            } else {
                console.error("Failed to re-add food:", data);
            }
        } catch(err) {
            console.error("Error adding food:", data);
        }
    }

    onMount(() => {
        loadMeals();
    })
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
    let currentRoute = window.location.pathname;
    async function handleFoodAdded(foodData: any) {
        console.log("Food added:", foodData);
        showAddFood = false;
        //waits to refresh page so item gets added to list without refreshing
        await loadMeals();
    }
    async function toggleAddFood() {
        showAddFood = !showAddFood;
    }
    // const meals = [
    //     {type: "placeholder1", name: "Meal"},
    //     {type: "placeholder2", name: "Meal"},
    //     {type: "placeholder3", name: "Meal"},
    // ];
</script>

<div class="container">
    <button class="toggle" onclick={toggleSidebar}>≡ Pages</button>
    
    <div class="layout">
        {#if showSidebar}
            <aside class="sidebar">
                <ul>
                    <li onclick={redirectToDashboard}>Dashboard</li>
                    <li>My Meals</li>
                    <li onclick={redirectToGoals}>My Goals</li>
                    <li onclick={redirectToLogout}>Logout</li>
                </ul>
            </aside>
        {/if}

        <main class="content">
            <h1>My Meals</h1>
            <div class="search-filter">
                <input placeholder="Search..."/>
                <button>Filter</button>
                <button onclick={toggleAddFood}> + </button>
            </div>
            {#if showAddFood}
                <div class="addfood-table">
                    <AddFood onFoodAdded={handleFoodAdded} />
                </div>
            {/if}
            <table>
                <thead>
                    <tr>
                        <th>Meal</th>
                        <th>Calories</th>
                        <th>Protein (g)</th>
                        <th>Fat (g)</th>
                        <th>Carbohydrates (g)</th>
                        <th>Re-add Food</th>
                    </tr>
                </thead>
                <tbody>
                    {#each meals as meal}
                        <tr>
                            <td>{meal.name}</td>
                            <td><span class="value">{meal.calories}</span></td>
                            <td><span class="value">{meal.protein}</span></td>
                            <td><span class="value">{meal.fat}</span></td>
                            <td><span class="value">{meal.carbohydrates}</span></td>
                            <td><button onclick={() => repeatFood(meal)}>+</button></td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </main>
    </div>
</div>

<style>
    .container {
        font-family: system-ui, sans-serif;
        /* background-color: #121212; */
        color: #fff;
        min-height: 100vh;
        padding: 1rem;
    }

    .toggle {
        background: #1e1e1e;
        border: none;
        color: white;
        padding: 0.5rem 1rem;
        font-size: 1.1rem;
        cursor: pointer;
        border-radius: 6px;
        margin-bottom: 1rem;
    }

    .layout {
        display: flex;
        gap: 1rem;
    }

    .sidebar {
        min-width: 180px;
        background-color: #1e1e1e;
        border-radius: 8px;
        padding: 1rem;
        min-height: 100vh;
    }

    .sidebar ul {
        list-style: none;
        padding: 0;
    }

    .sidebar li {
        /* width: 100%; */
        padding: 0.75rem;
        cursor: pointer;
        border-radius: 6px;
    }

    .sidebar li:hover, .sidebar li:active {
        background-color: #2a2a2a;
    }

    .content {
        flex: 1;
    }

    .content h1 {
        font-size: 1.8rem;
        margin-bottom: 1rem;
    }

    .search-filter {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .search-filter input {
        flex: 1;
        padding: 0.5rem;
        background-color: #2a2a2a;
    }

    .search-filter button {
        background-color: #2a2a2a;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        cursor: pointer;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        background-color: #1e1e1e;
        border-radius: 8px;
    }

    th,td {
        padding: 0.74rem;
        text-align: left;
        border-bottom: 1px solid #333;
    }

    .value {
        background: #2a2a2a;
        padding: 0.3rem 0.75rem;
        border-radius: 999px;
        font-size: 0.9rem;
        color: #ddd;
    }

</style>