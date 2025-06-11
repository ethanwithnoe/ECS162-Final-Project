<script lang="ts">
	// import Dashboard from './Dashboard.svelte';
    import { onMount } from 'svelte';
    import  AddFood  from "./AddFood.svelte";
    let showSidebar = false;
    let showAddFood = false;
    let meals = [];
    let error = "";

    let searchFood = "";

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

    async function removeFood(food_Id: string) {
        try {
            const formData = new FormData();
            formData.append("food_id", food_Id);

            const res = await fetch("/api/deletefood", {method: "POST", body: formData,});
            const data = await res.json()
            if (data.result === 0) {
                meals = meals.filter(meal => meal._id !== food_Id);
            } else {
                console.error("Failed to delete food:", data.result);
            }
        } catch(err) {
            console.error("Error deleteing meal:", err);
        }
    }

    $: filteredMeals = meals.filter(meal =>
        meal.name.toLowerCase().includes(searchFood.toLowerCase())
    );
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
                <input placeholder="Search Meals..." bind:value={searchFood}/>
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
                        <th>Remove Item</th>
                    </tr>
                </thead>
                <tbody>
                    {#each filteredMeals as meal (meal._id)}
                        <tr>
                            <td>{meal.name}</td>
                            <td><span class="value">{meal.calories}</span></td>
                            <td><span class="value">{meal.protein}</span></td>
                            <td><span class="value">{meal.fat}</span></td>
                            <td><span class="value">{meal.carbohydrates}</span></td>
                            <td><button onclick={() => repeatFood(meal)}>+</button></td>
                            <td><button onclick={() => removeFood(meal._id)}>-</button></td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        </main>
    </div>
</div>

<style> /* Redoing the color scheme to match the Figma */
.container {
    font-family: 'Inter', system-ui, sans-serif;
    color: black;
    background-color: white;
    min-height: 100vh;
    padding: 1rem;
}

.toggle {
    background: white;
    border: 1px solid #ddd;
    color: black;
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
    background-color: white;
    border-radius: 8px;
    padding: 1rem;
    min-height: 100vh;
    border: 1px solid #ddd;
}

.sidebar ul {
    list-style: none;
    padding: 0;
}

.sidebar li {
    padding: 0.75rem;
    cursor: pointer;
    border-radius: 6px;
}

.sidebar li:hover, .sidebar li:active {
    background-color: #f1f1f1;
}

.content {
    flex: 1;
}

.content h1 {
    font-size: 1.8rem;
    margin-bottom: 1rem;
    color: black;
}

.search-filter {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}

.search-filter input {
    flex: 1;
    padding: 0.5rem 1rem;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 1rem;
    background-color: white;
    color: black;
}

.search-filter button {
    background-color: white;
    color: black;
    border: 1px solid #ddd;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.search-filter button:hover {
    background-color: #f1f1f1;
}

table {
    width: 100%;
    border-collapse: collapse;
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 8px;
}

th, td {
    padding: 0.74rem;
    text-align: left;
    border-bottom: 1px solid #ddd;
    color: black;
}

th {
    background-color: #f9f9f9;
    color: #333;
}

.value {
    background: #f1f1f1;
    padding: 0.3rem 0.75rem;
    border-radius: 999px;
    font-size: 0.9rem;
    color: black;
}

/* Search bar and buttons inside food search menu */
.search-filter input {
    background-color: white;
    color: black;
    border: 1px solid #ddd;
    border-radius: 6px;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    flex: 1;
}

.search-filter button {
    background-color: white;
    color: black;
    border: 1px solid #ddd;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.search-filter button:hover {
    background-color: #f1f1f1;
}

</style>
