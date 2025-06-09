<script>
	// import Dashboard from './Dashboard.svelte';
    // import Meals from './Meals.svelte';
    import { onMount } from 'svelte';
    //Immediately calls fetchInfo to populate table with userinfo
    onMount(() => {
        fetchInfo();
    });
    //Doesn't show sidebar immediately
    let showSidebar = false;
    let submitMsg = "";
    //Sets userstats to default values if no data there
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
    //Sets usergoals to 0 by default
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
    
    async function submitGoals() {
        const res = await fetch("/api/addgoals", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ...userStats,  ...userGoals})
        });
        const result = await res.json();
        console.log("Saved:", result);
        //Updates submitMsg to update user for 5 seconds that goals were updated
        submitMsg = "Goals Updated!";
        setTimeout(() => {
            submitMsg = "";
        }, 5000);
    }

    //Calculates users goals and pushes them to the table
    function calculateGoals() {
        //Converts weight into kg and heigh into cm
        userStats.HeightCM = 2.54*((userStats.HeightFt * 12) + (userStats.HeightIn));
        userStats.WeightKG = userStats.Weight*0.45359237
        //Calculates BMR per gender using different numbers
        if(userStats.Gender === "F" || userStats.Gender === "f") {
            userStats.BMR = (10 * userStats.WeightKG) + (6.25 * userStats.HeightCM) - (5 * userStats.Age) - 161;
        }
        else if(userStats.Gender === "M" || userStats.Gender === "m") {
            userStats.BMR = 5 + (10 * userStats.WeightKG) + (6.25 * userStats.HeightCM) - (5 * userStats.Age);

        }

        //Calculates AMR based on activity status using different multipliers
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

        //Calculates User Goals based on Calories and rounds to nicer numbers
        userGoals.calories = Math.round(userStats.AMR);
        console.log(userGoals.calories);
        userGoals.protein = Math.round((0.10*userGoals.calories) / 4);
        userGoals.carbohydrates = Math.round((0.45*userGoals.calories) / 4);
        userGoals.fat = Math.round((0.20*userGoals.calories) / 9);

        submitGoals();
    }
    
    
    //Fetches userinfo from the database. Loads it into their stats and displays it in the table
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

            userStats.Age =             data.Age;
            userStats.Gender =          data.Gender;
            userStats.HeightFt =        data.HeightFt;
            userStats.HeightIn =        data.HeightIn;
            userStats.Weight =          data.Weight;
            userStats.Activity =        data.Activity;
            userStats.AMR =             data.AMR;
            userStats.BMR =             data.BMR;
        } catch (e) {               //Catches error
            console.error("No user data", e);   //Prints that user has no data saved in mongo database
        }
    }
    const goals = [
        {type: "placeholder1", name: "goal"},
        {type: "placeholder2", name: "goal"},
        {type: "placeholder3", name: "goal"},
    ];
</script>

<div class="container">
    <!--Button to togglesidebar-->
    <button class="toggle" onclick={toggleSidebar}>≡ Pages</button>
    
    <div class="layout">
        {#if showSidebar}
            <aside class="sidebar">
                <ul>
                    <li onclick={redirectToDashboard}>Dashboard</li>
                    <li onclick={redirectToMeals}>My Meals</li>
                    <li>My Goals</li>
                    <li onclick={redirectToLogout}>Logout</li>
                </ul>
            </aside>
        {/if}

        <main class="content">
            <h1>Goal Editor</h1>
            <!--Calculator Table for users to input data if not already in database, and if there, user can update by binding values-->
            <h3> Calculate your Recommended Calorie Intake! </h3>
            <table>
                <tbody>
                    <tr>
                        <td><strong>Calorie Calculator!</strong></td>
                    </tr>
                    <tr>
                        <td>Age</td>
                        <td><input type="number" bind:value={userStats.Age} /></td>
                    </tr>
                    <!--Input gender info that is case-insensitive using regex-->
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
                    <!--Input Activity info that is case-insensitive using regex-->
                    <tr>
                        <td>Days of Exercise per Week (S: 0, L: 1-3 Days | M: 3-5 Days | A: 6-7 Days | E: 6-7 Days )</td>
                        <td><input type="text" bind:value={userStats.Activity} pattern="^(S|s|L|l|M|m|A|a|E|e)$" /></td>
                    </tr>
                </tbody>
            </table>

            <button onclick={calculateGoals}>Calculate</button>
            
            <h3> Here is your recommended Calorie Intake. For every pound a week you'd like to lose, subtract by 500! Update the values if you wish! The statistics provided in the table below are from the bare minimum multiplier based on your Calories from the USDA's Dietary Guidelines. The general goal of your calorie intake per each following nutrient is: protein: 10-35%, carbohydrates: 45-65%, fat: 20-35%. We suggest {userGoals.calories} Calories/day </h3>
            <!-- <p>{userGoals.calories} Calories/day</p> -->
            <!-- Table to place goals within. User can edit the values already in via bind value. If data already there, will load in user goals automatically on mount-->
            <table>
                <tbody>
                    <tr>
                        <td><strong>Update your Goals Here!</strong></td>
                    </tr>
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
            <!--Ensures submit button doesnt move and is positioned side by side with update status-->
            <div style="display: flex; align-items: center; gap: 10px;">
                <!-- Submit Goals button that will submit Goals to database via backend call-->
                <button onclick={submitGoals}>Submit</button>
                    <p class="success message" style="visibility: {submitMsg ? 'visible' : 'hidden'};">
                        {submitMsg}
                    </p>
            </div>
        </main>
    </div>
</div>

<style>
    /*Makes submitMsg green and bold*/
    .success {
        color: lightgreen;
        font-weight: bold;
    }
    /*Allocates space to prevent submit button moving due to submitMsg appearing*/
    .message {
        min-width: 150px;
        min-height: 1em;
        margin: 0;
        display: flex;
        align-items: center;
    }
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


    table {
        width: 100%;
        border-collapse: collapse;
        background-color: #1e1e1e;
        border-radius: 8px;
        padding: 10px;
        margin-top: 10px;
        margin-bottom: 10px;
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