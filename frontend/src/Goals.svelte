<script>
	// import Dashboard from './Dashboard.svelte';
    // import Meals from './Meals.svelte';
    let showSidebar = false;
    let userStats = {
        Age: 0,
        Gender: "",
        HeightFt: 0,
        HeightIn: 0,
        HeightCM: 0,
        Weight: 0,
        WeightKG: 0,
        Activity: "",
        BMR: 0,
        AMR: 0
    };
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
    function calculateGoals() {
        userStats.HeightCM = 2.54*((userStats.HeightFt * 12) + (userStats.HeightIn));
        userStats.WeightKG = userStats.Weight*0.45359237
        if(userStats.Gender === "F" || userStats.Gender === "f") {
            userStats.BMR = (10 * userStats.WeightKG) + (6.25 * userStats.HeightCM) - (5 * userStats.Age) - 161;
        }
        if(userStats.Gender === "M" || userStats.Gender === "m") {
            userStats.BMR = 5 + (10 * userStats.WeightKG) + (6.25 * userStats.HeightCM) - (5 * userStats.Age);

        }

        if(userStats.Activity === "S" || userStats.Activity === "s") {
            userStats.AMR = userStats.BMR * 1.2;
        }
        if(userStats.Activity === "L" || userStats.Activity === "l") {
            userStats.AMR = userStats.BMR * 1.375;
        }
        if(userStats.Activity === "M" || userStats.Activity === "m") {
            userStats.AMR = userStats.BMR * 1.55;
        }
        if(userStats.Activity === "A" || userStats.Activity === "a") {
            userStats.AMR = userStats.BMR * 1.725;
        }
        if(userStats.Activity === "E" || userStats.Activity === "e") {
            userStats.AMR = userStats.BMR * 1.9;
        }

        //Calculates User Goals based on Calories
        userGoals.calories = Math.round(userStats.AMR);
        userGoals.protein = Math.round((0.10*userGoals.calories) / 4);
        userGoals.carbohydrates = Math.round((0.45*userGoals.calories) / 4);
        userGoals.fat = Math.round((0.20*userGoals.calories) / 9);
    }
    function submitGoals() {
        console.log("yippee");
    }
    const goals = [
        {type: "placeholder1", name: "goal"},
        {type: "placeholder2", name: "goal"},
        {type: "placeholder3", name: "goal"},
    ];
</script>

<div class="container">
    <button class="toggle" on:click={toggleSidebar}>Pages</button>
    
    <div class="layout">
        {#if showSidebar}
            <aside class="sidebar">
                <ul>
                    <li class="active"><button on:click={redirectToDashboard}>Dashboard</button></li>
                    <li class="active"><button on:click={redirectToMeals}>My Meals</button></li>
                    <li class="active"><button on:click={redirectToGoals}>My Goals</button></li>
                </ul>
            </aside>
        {/if}

        <main class="content">
            <h1>My Goals</h1>
            <div class="search-filter">
                <input placeholder="Search..."/>
                <button>Filter</button>
                <button>Edit</button>
            </div>
            <h3> Calculate your Recommended Calorie Intake! </h3>
            <table>
                <tbody>
                    <tr>
                        <td>Age</td>
                        <td><input type="number" bind:value={userStats.Age} /></td>
                    </tr>
                    <tr>
                        <td>Gender (M or F (M for Male, F for Female))</td>
                        <td><input type="text" bind:value={userStats.Gender} pattern="^(F|M|f|m)$" /></td>
                    </tr>
                    <tr>
                        <td>Height (Feet)</td>
                        <td><input type="number" bind:value={userStats.HeightFt} /></td>
                    </tr>
                    <tr>
                        <td>Height (Inches)</td>
                        <td><input type="number" bind:value={userStats.HeightIn} /></td>
                    </tr>
                    <tr>
                        <td>Weight (lbs)</td>
                        <td><input type="number" bind:value={userStats.Weight} /></td>
                    </tr>
                    <tr>
                        <td>Days of Exercise per Week (S: 0, L: 1-3 Days | M: 3-5 Days | A: 6-7 Days | E: 6-7 Days )</td>
                        <td><input type="text" bind:value={userStats.Activity} pattern="^(S|s|L|l|M|m|A|a|E|e)$" /></td>
                    </tr>
                </tbody>
            </table>

            <button on:click={calculateGoals}>Calculate</button>

            <h3> Here is your recommended Calorie Intake. For every pound a week you'd like to lose, subtract by 500! Update the values if you wish! </h3>
            <h3> The statistics provided in the table below are the bare minimum multiplier based on your Calories from the USDA's Dietary Guidelines, for protein: 10-35%, carbohydrates: 45-65%, fat: 20-35%, </h3>
            <p>{userGoals.calories} Calories/day</p>
            <table>
                <tbody>
                    <tr>
                        <td>Calorie Goal</td>
                        <td><input type="number" bind:value={userGoals.calories} /></td>
                    </tr>
                    <tr>
                        <td>Protein Goal (g) (10 for every 100 Calories)</td>
                        <td><input type="number" bind:value={userGoals.protein} /></td>
                    </tr>
                    <tr>
                        <td>Fat (g)</td>
                        <td><input type="number" bind:value={userGoals.fat} /></td>
                    </tr>
                    <tr>
                        <td>Carbohydrates (g)</td>
                        <td><input type="number" bind:value={userGoals.carbohydrates} /></td>
                    </tr>
                </tbody>
            </table>
            <button on:click={submitGoals}>Submit</button>

            <table>
                <thead>
                    <tr>
                        <th>Type</th>
                        <th>Meal</th>
                        <th>Calories</th>
                        <th>Protein</th>
                        <th>Fat</th>
                        <th>Carbohydrates</th>
                    </tr>
                </thead>
                <tbody>
                    {#each goals as goal}
                        <tr>
                            <td>{goal.type}</td>
                            <td>{goal.name}</td>
                            <td><span class="value">Value</span></td>
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