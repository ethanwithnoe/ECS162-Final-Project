<script lang="ts">
    // import Dashboard from './Dashboard.svelte';
    import { onMount } from "svelte";
    import LineChart from "../components/LineChart.svelte";
    import BarChart from "../components/BarChart.svelte";
    import ProgressChart from "../components/RadialProgress.svelte";

    let searchEmail = "";
    let addFriendMsg = "";
    let friendList = [];
    let meals = [];
    let error = "";
    let userGoalProgress = {
        calories: 0,
        protein: 0,
        fat: 0,
        carbohydrates: 0,
        caloriesleft: 0,
        proteinleft: 0,
        fatleft: 0,
        carbohydratesleft: 0,
    };
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
    let selectedNutrient: keyof Meal = "calories";
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    let filteredData: any = null;
    let filteredProgress: any = null;
    let progressData = [];
    let foodData: Meal[] = [];
    // let filteredData = foodData
    //     .sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()) // Sort by timestamp
    //     .map(meal => ({
    //         timestamp: meal.timestamp,
    //         nutrientValue: meal[selectedNutrient as keyof Meal] as number,  // Assert nutrientValue is a number
    //     }));
    //END MOCK SECTION
    async function loaddailyMeals() {
        try {
            //Calls backend function that gets the foods user added from today
            const res = await fetch("/api/getuserfoodsTD", {
                credentials: "include",
            });
            const data = await res.json();
            if (data.result === 0) {
                //stores meals and calls trackgoalprogress to fill in goal progress data
                meals = data.foodList;
                trackGoalProgress();
            } else {
                error = "Please Login to View Your Meals.";
            }
        } catch (err) {
            error = "Error loading meals.";
            console.log(error);
        }
    }

    async function getFoodLogs() {
        selectedNutrient = "calories"; // Define the default selected nutrient

        try {
            const res = await fetch(
                `/api/getuserfoods?range=${encodeURIComponent("")}`,
            );
            const data = await res.json();
            foodData = data.foodList;

            console.log(foodData);

            // filteredData = foodData
            // .sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()) // Sort by timestamp
            // .map(meal => ({
            //     timestamp: meal.timestamp,
            //     nutrientValue: meal[selectedNutrient as keyof Meal] as number,  // Assert nutrientValue is a number
            // }));

            filteredData = foodData
                .filter((meal) => {
                    const mealDate = new Date(meal.timestamp);
                    mealDate.setHours(0, 0, 0, 0);
                    return mealDate.getTime() === today.getTime();
                })
                .sort(
                    (a, b) =>
                        new Date(a.timestamp).getTime() -
                        new Date(b.timestamp).getTime(),
                )
                .map((meal) => ({
                    timestamp: meal.timestamp,
                    nutrientValue: meal[
                        selectedNutrient as keyof Meal
                    ] as number,
                }));
        } catch (error) {
            console.error("Failed fetch food data:", error);
        }
    }
    let buffer = 10;
    //END MOCK SECTION FOR LINE/BAR

    // MOCK SECTION FOR PROGRESS FILTERING
    let view: "today" | "lastWeek" | "lastMonth" = "today";

    $: if (view) {
        (async () => {
            filteredProgress = await filterProgressData(view);
        })();
    }
    $: goalValue = (() => {
        if (selectedNutrient == "calories") {
            return userGoals.calories;
        }
        if (selectedNutrient == "protein") {
            return userGoals.protein;
        }
        if (selectedNutrient == "fat") {
            return userGoals.fat;
        }
        if (selectedNutrient == "carbohydrates") {
            return userGoals.carbohydrates;
        } else {
            return 0;
        }
    })();
    $: if (foodData && selectedNutrient) {
        filteredData = foodData
            .filter((meal) => {
                const mealDate = new Date(meal.timestamp);
                mealDate.setHours(0, 0, 0, 0);
                return mealDate.getTime() === today.getTime();
            })
            .sort(
                (a, b) =>
                    new Date(a.timestamp).getTime() -
                    new Date(b.timestamp).getTime(),
            )
            .map((meal) => ({
                timestamp: meal.timestamp,
                nutrientValue: meal[selectedNutrient as keyof Meal] as number,
            }));
    }

    async function filterProgressData(view: string) {
        try {
            const res = await fetch(`/api/fetchrecords/${100}`);
            if (!res.ok) {
                console.error("Failed to fetch Progress Data");
                return;
            }
            const data = await res.json();
            console.log(data);
            progressData = data.records;
            // console.log(progressData);
        } catch (error) {
            console.error("Failed to fetch Progress Data: ", error);
            return;
        }

        const today = new Date();
        today.setHours(0, 0, 0, 0); // normalize to start of day

        if (view === "lastWeek") {
            // last 7 days including today
            const sevenDaysAgo = new Date(today);
            sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 6); // 6 because inclusive of today

            return progressData.filter((item) => {
                const itemDate = new Date(item.timestamp);
                return itemDate >= sevenDaysAgo && itemDate <= today;
            });
        } else if (view === "lastMonth") {
            // previous calendar month
            const firstDayThisMonth = new Date(
                today.getFullYear(),
                today.getMonth(),
                1,
            );
            const lastMonthEnd = new Date(firstDayThisMonth);
            lastMonthEnd.setDate(0); // last day of previous month
            const lastMonthStart = new Date(
                lastMonthEnd.getFullYear(),
                lastMonthEnd.getMonth(),
                1,
            );

            return progressData.filter((item) => {
                const itemDate = new Date(item.timestamp);
                return itemDate >= lastMonthStart && itemDate <= lastMonthEnd;
            });
        } else {
            // Default to show all data or today
            return progressData;
        }
    }

    // END MOCK SECTION FOR PROGRESS FILTERING

    let userEmail = null;
    let showSidebar = false;
    let userGoals = {
        calories: 0,
        protein: 0,
        fat: 0,
        carbohydrates: 0,
    };
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

    async function fetchFriendsList() {
        try {
            const res = await fetch("/api/get/friendslist");
            const data = await res.json();
            // return data;
            if (data.result === 0) {
                friendList = data.friendsList;
            } else {
                console.log("Failed to fetch friends:", data);
            }
        } catch (error) {
            console.log("Error fetching friends list: ", error);
        }
    }

    async function fetchInfo() {
        try {
            const res = await fetch("/api/fetchgoals");
            //If fetch fails, print console error that no goals detected
            // console.log(res);
            if (!res.ok) {
                console.error("No goals detected");
                return;
            }
            //Catches data from fetchgoals
            const data = await res.json();
            //Stores users stats and goals from fetchgoals in backend
            userGoals.calories = data.calories;
            userGoals.protein = data.protein;
            userGoals.fat = data.fat;
            userGoals.carbohydrates = data.carbohydrates;
        } catch (e) {
            //Catches error
            console.error("No user data", e); //Prints that user has no data saved in mongo database
        }
    }
    //Calculates goal progress using the food from today
    async function trackGoalProgress() {
        userGoalProgress.calories = 0;
        userGoalProgress.protein = 0;
        userGoalProgress.fat = 0;
        userGoalProgress.carbohydrates = 0;
        for (let meal of meals) {
            userGoalProgress.calories = Math.round(
                userGoalProgress.calories + meal.calories,
            );
            userGoalProgress.protein = Math.round(
                userGoalProgress.protein + meal.protein,
            );
            userGoalProgress.fat = Math.round(userGoalProgress.fat + meal.fat);
            userGoalProgress.carbohydrates = Math.round(
                userGoalProgress.carbohydrates + meal.carbohydrates,
            );
        }
        userGoalProgress.caloriesleft =
            userGoals.calories - userGoalProgress.calories;
        userGoalProgress.proteinleft =
            userGoals.protein - userGoalProgress.protein;
        userGoalProgress.fatleft = userGoals.fat - userGoalProgress.fat;
        userGoalProgress.carbohydratesleft =
            userGoals.carbohydrates - userGoalProgress.carbohydrates;
    }

    async function addFriend() {
        if (!searchEmail) {
            addFriendMsg = "Please enter an Email.";
            return;
        }
        const formData = new FormData();
        formData.append("email", searchEmail);

        try {
            const res = await fetch("/api/post/makefriend", {
                method: "POST",
                body: formData,
            });
            const data = await res.json();

            switch (data.result) {
                case 0:
                    addFriendMsg = "Successfully added Friend";
                    fetchFriendsList();
                    break;
                case 1:
                    addFriendMsg = "You are already Friends.";
                    break;
                case 10:
                    addFriendMsg = "You must be Logged In";
                    break;
                case 11:
                    addFriendMsg = "Error: could not access friend list.";
                    break;
                case 12:
                    addFriendMsg = "Error: user does not exist.";
                    break;
                case 13:
                    addFriendMsg = "You cannot add yourself.";
                    break;
                default:
                    addFriendMsg = "Unknown Error Occurred.";
                    break;
            }
        } catch (err) {
            addFriendMsg = "Failed to add friend.";
            console.error(err);
        }
        searchEmail = "";
    }

    async function removeFriend(email: string) {
        try {
            const formData = new FormData();
            formData.append("email", email);
            const res = await fetch("/api/post/removefriend", {
                method: "POST",
                body: formData,
            });
            const data = await res.json();

            switch (data.result) {
                case 0:
                    addFriendMsg = "Successfully removed Friend";
                    fetchFriendsList();
                    break;
                case 1:
                    addFriendMsg = "You are already not Friends.";
                    break;
                case 10:
                    addFriendMsg = "You must be Logged In";
                    break;
                case 11:
                    addFriendMsg = "Error: could not access friend list.";
                    break;
                case 12:
                    addFriendMsg = "Error: user does not exist.";
                    break;
                case 13:
                    addFriendMsg = "You cannot remove yourself.";
                    break;
                default:
                    addFriendMsg = "Unknown Error Occurred.";
                    break;
            }
        } catch (err) {
            addFriendMsg = "Failed to remove friend.";
            console.error(err);
        }
    }

    onMount(async () => {
        const res = await fetch("/api/getinfo");
        const data = await res.json();
        if (!data.email) {
            window.location.href = "/";
        } else {
            userEmail = data.email;
        }
        await fetchInfo();
        await loaddailyMeals();
        getFoodLogs();
        filteredProgress = await filterProgressData(view);
        fetchFriendsList();
    });

    function capitalize(str: string): string {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
</script>

<div class="dashboard-container">
    <button class="toggle" onclick={toggleSidebar}>≡ Pages</button>

    <div class="layout">
        {#if showSidebar}
            <aside class="sidebar">
                <ul>
                    <li>Dashboard</li>
                    <li onclick={redirectToMeals}>My Meals</li>
                    <li onclick={redirectToGoals}>My Goals</li>
                    <li onclick={redirectToLogout}>Logout</li>
                </ul>
            </aside>
        {/if}

        <main class="content">
            <header>
                <h1>My Dashboard</h1>
                <div class="tabs">
                    <button onclick={() => (view = "today")}>Today</button>
                    <button onclick={() => (view = "lastWeek")}
                        >This Week</button
                    >
                    <button onclick={() => (view = "lastMonth")}
                        >Last Month</button
                    >

                    <button
                        onclick={() => {
                            selectedNutrient = "calories";
                            goalValue = userGoals.calories;
                        }}>Calorie Chart</button
                    >
                    <button
                        onclick={() => {
                            selectedNutrient = "protein";
                            goalValue = userGoals.protein;
                        }}>Protein Chart</button
                    >
                    <button
                        onclick={() => {
                            selectedNutrient = "fat";
                            goalValue = userGoals.fat;
                        }}>Fat Chart</button
                    >
                    <button
                        onclick={() => {
                            selectedNutrient = "carbohydrates";
                            goalValue = userGoals.carbohydrates;
                        }}>Carb Chart</button
                    >
                </div>
            </header>

            <div class="summary-cards">
                <div class="card">
                    <h3>Calories</h3>
                    {#if filteredProgress && view !== "today"}
                        <div class="ProgressChart">
                            <ProgressChart
                                filteredData={filteredProgress}
                                selectedNutrient={"calories"}
                                width={150}
                                height={150}
                            />
                        </div>
                    {:else if filteredProgress}
                        <p>Current Progress: {userGoalProgress.calories}</p>
                        <small class="goalDiff">
                            Calories Goal: {userGoals.calories},
                            {#if userGoalProgress.caloriesleft > 0}
                                just {userGoalProgress.caloriesleft} off!
                            {:else}
                                complete!
                            {/if}
                        </small>
                    {/if}
                </div>

                <div class="card">
                    <h3>Protein</h3>
                    {#if filteredProgress && view !== "today"}
                        <div class="ProgressChart">
                            <ProgressChart
                                filteredData={filteredProgress}
                                selectedNutrient={"protein"}
                                width={150}
                                height={150}
                            />
                        </div>
                    {:else if filteredProgress}
                        <p>Current Progress: {userGoalProgress.protein}</p>
                        <small class="goalDiff">
                            Protein Goal: {userGoals.protein},
                            {#if userGoalProgress.proteinleft > 0}
                                just {userGoalProgress.proteinleft} off!
                            {:else}
                                complete!
                            {/if}
                        </small>
                    {/if}
                </div>

                <div class="card">
                    <h3>Carbohydrates</h3>
                    {#if filteredProgress && view !== "today"}
                        <div class="ProgressChart">
                            <ProgressChart
                                filteredData={filteredProgress}
                                selectedNutrient={"carbohydrates"}
                                width={150}
                                height={150}
                            />
                        </div>
                    {:else if filteredProgress}
                        <p>
                            Current Progress: {userGoalProgress.carbohydrates}
                        </p>
                        <small class="goalDiff">
                            Carbohydrate Goal: {userGoals.carbohydrates},
                            {#if userGoalProgress.carbohydratesleft > 0}
                                just {userGoalProgress.carbohydratesleft} off!
                            {:else}
                                complete!
                            {/if}
                        </small>
                    {/if}
                </div>

                <div class="card">
                    <h3>Fat</h3>
                    {#if filteredProgress && view !== "today"}
                        <div class="ProgressChart">
                            <ProgressChart
                                filteredData={filteredProgress}
                                selectedNutrient={"fat"}
                                width={150}
                                height={150}
                            />
                        </div>
                    {:else if filteredProgress}
                        <p>Current Progress: {userGoalProgress.fat}</p>
                        <small class="goalDiff">
                            Fat Goal: {userGoals.fat},
                            {#if userGoalProgress.fatleft > 0}
                                just {userGoalProgress.fatleft} off!
                            {:else}
                                complete!
                            {/if}
                        </small>
                    {/if}
                </div>
            </div>

            <div class="main-grid">
                <!-- Bottom Row -->
                <div class="card large">
                    <div class="card-content">
                        <h3>
                            Today's {capitalize(selectedNutrient)}
                        </h3>
                        {#if filteredData}
                            <BarChart
                                {filteredData}
                                {goalValue}
                                {buffer}
                                height={400}
                                width={600}
                                {selectedNutrient}
                                startHour={6}
                                endHour={23}
                            />
                        {/if}
                    </div>
                </div>

                <div class="card flexible">
                    <h3>Your Meals so Far</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Meal</th>
                                <th>Calories</th>
                                <th>Protein</th>
                                <th>Fat</th>
                                <th>Carbs</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each meals as meal}
                                <tr>
                                    <td>{meal.name}</td>
                                    <td
                                        ><span class="value"
                                            >{meal.calories}</span
                                        ></td
                                    >
                                    <td
                                        ><span class="value"
                                            >{meal.protein}</span
                                        ></td
                                    >
                                    <td
                                        ><span class="value">{meal.fat}</span
                                        ></td
                                    >
                                    <td
                                        ><span class="value"
                                            >{meal.carbohydrates}</span
                                        ></td
                                    >
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>

                <div class="card flexible">
                    <h3>My Friends</h3>
                    <input
                        type="email"
                        bind:value={searchEmail}
                        placeholder="Enter Email"
                        class="input-style"
                    />
                    <button onclick={addFriend}>Add</button>
                    {#if addFriendMsg}
                        <p>{addFriendMsg}</p>
                    {/if}
                    {#if friendList && friendList.length > 0}
                        <ul id="friendslist">
                            {#each friendList as [email, username]}
                                <li class="friend-list">
                                    {username} ({email})
                                    <button
                                        class="friend_remove_button"
                                        onclick={(e) => {
                                            removeFriend(email);
                                        }}
                                    >
                                        Remove
                                    </button>
                                </li>
                            {/each}
                        </ul>
                    {:else}
                        <p>Your Friends List is Empty.</p>
                    {/if}
                </div>

                <div class="card large">
                    <h3>
                        Today's {capitalize(selectedNutrient)}
                    </h3>
                    {#if filteredData}
                        <LineChart
                            {filteredData}
                            {goalValue}
                            {buffer}
                            height={400}
                            width={600}
                            {selectedNutrient}
                        />
                    {/if}
                </div>
            </div>
        </main>
    </div>
</div>

<style>
    /* Attempt at swapping color schemes to the figma, cleaning simple comments, only keeping new ones*/
    .dashboard-container {
        font-family: "Inter", system-ui, sans-serif;
        color: #000;
        min-height: 100vh;
        padding: 1rem;
        background-color: white;
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
    }

    .sidebar li {
        padding: 0.75rem;
        cursor: pointer;
        border-radius: 6px;
    }

    .sidebar li:hover,
    .sidebar li:active {
        background-color: #f1f1f1;
    }

    header {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        align-items: center;
    }

    .tabs button {
        margin-right: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: bold;
        background-color: white;
        color: black;
        border: 1px solid #ddd;
        border-radius: 6px;
        cursor: pointer;
    }

    .summary-cards {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }

    .card {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
        border: 1px solid #ddd;
    }

    .card h2,
    .card h3 {
        margin-top: 0;
        color: black;
    }

    .card p {
        font-size: 1.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
        color: black;
    }

    .card small {
        color: #333;
    }

    main {
        width: 100%;
    }

    .main-grid {
        display: grid;
        grid-template-columns: minmax(0, 3fr) minmax(0, 2fr);
        gap: 1.5rem;
        margin-top: 1.5rem;
        grid-template-rows: auto auto;
    }

    .card.large {
        grid-column: span 2;
        text-align: center;
        padding: 2rem;
    }

    .card.large .card-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }

    .card.large h3 {
        margin: 0;
        padding-bottom: 1rem;
        text-align: center;
        color: black;
    }

    .card.large svg {
        height: 400px;
        width: 100%;
        object-fit: contain;
    }

    .card {
        grid-column: span 1;
    }

    /* Position cards explicitly because formatting sucked*/
    .main-grid .card:nth-child(1) {
        /* Bar Graph */
        grid-row: 1;
    }

    .main-grid .card:nth-child(2) {
        /* Meals */
        grid-row: 1;
    }

    .main-grid .card:nth-child(3) {
        /* Friends */
        grid-row: 2;
    }

    .main-grid .card:nth-child(4) {
        /* Line Graph */
        grid-row: 2;
    }

    .card.flexible {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        color: black;
    }

    th,
    td {
        text-align: left;
        padding: 0.4rem;
        border-bottom: 1px solid #ddd;
    }

    th {
        background-color: #f9f9f9;
        color: #333;
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
        background-color: #2a2a2a;
        border-radius: 6px;
        color: aaa;
    }
    /* .logout {
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
    } */
    .friend-list {
        padding: 0.5rem;
        background: #2a2a2a;
        margin-bottom: 0.5rem;
        border-radius: 5px;
        color: white;
    }
    .graph-placeholder {
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #f1f1f1;
        border-radius: 6px;
        color: #333;
    }

    .friend-list {
        padding: 0.5rem;
        background: #f1f1f1;
        margin-bottom: 0.5rem;
        border-radius: 5px;
        color: black;
    }

    /* Styling for search bar in My Friends */
    .card.flexible .input-style {
        width: 100%;
        padding: 0.5rem 1rem;
        border: 1px solid #ddd;
        border-radius: 6px;
        margin-bottom: 1rem;
        font-size: 1rem;
        background-color: #fff;
        color: black;
        /* We didn't have explicit styling before for the size, etc*/
        max-width: 350px;
        margin-left: auto;
        margin-right: auto;
    }

    /* Styling for button in My Friends */
    .card.flexible button {
        background: white;
        border: 1px solid #ddd;
        color: black;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        cursor: pointer;
        border-radius: 6px;
        transition: background-color 0.2s ease;
    }

    .card.flexible button:hover {
        background-color: #f1f1f1;
    }
</style>
