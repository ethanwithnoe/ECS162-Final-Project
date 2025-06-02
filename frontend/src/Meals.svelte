<script>
	import Dashboard from './Dashboard.svelte';

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

    const meals = [
        {type: "placeholder1", name: "Meal"},
        {type: "placeholder2", name: "Meal"},
        {type: "placeholder3", name: "Meal"},
    ];
</script>

<div class="container">
    <button class="toggle" onclick={toggleSidebar}>Pages</button>
    
    <div class="layout">
        {#if showSidebar}
            <aside class="sidebar">
                <ul>
                    <li class="active"><button onclick={redirectToDashboard}>Dashboard</button></li>
                    <li class="active"><button onclick={redirectToMeals}>My Meals</button></li>
                </ul>
            </aside>
        {/if}

        <main class="content">
            <h1>My Meals</h1>
            <div class="search-filter">
                <input placeholder="Search..."/>
                <button>Filter</button>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>Type</th>
                        <th>Meal</th>
                        <th>Calories</th>
                        <th>Protein</th>
                        <th>Fat</th>
                    </tr>
                </thead>
                <tbody>
                    {#each meals as meal}
                        <tr>
                            <td>{meal.type}</td>
                            <td>{meal.name}</td>
                            <td><span class="value">Value</span></td>
                            <td><span class="value">Value</span></td>
                            <td><span class="value">Value</span></td>
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
        /* padding: 0; */
    }

    .sidebar li {
        padding: 0.75rem;
        cursor: pointer;
        border-radius: 6px;
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