<script lang="ts">
	// import Dashboard from './Dashboard.svelte';
    import { onMount } from 'svelte';
    import LineChart from '../components/LineChart.svelte';
    import BarChart from '../components/BarChart.svelte';
    import ProgressChart from '../components/RadialProgress.svelte';

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
            "timestamp": "2025-05-08T08:00:00.000000-08:00", // 8:00 AM > falls into the 8 AM bin
            "userid": "admin@hw3.com",
            "_id": "119"
        },
        {
            "calories": 450,
            "carbohydrates": 60,
            "fat": 15,
            "protein": 25,
            "description": "Chicken Salad",
            "name": "Grilled Chicken Salad",
            "timestamp": "2025-06-08T10:15:00.000000-08:00",
            "userid": "admin@hw3.com",
            "_id": "11"
        },
        {
            "calories": 150,
            "carbohydrates": 20,
            "fat": 5,
            "protein": 10,
            "description": "Apple and Peanut Butter",
            "name": "Snack",
            "timestamp": "2025-06-08T12:30:00.000000-08:00",
            "userid": "admin@hw3.com",
            "_id": "11"
        },
        {
            "calories": 600,
            "carbohydrates": 75,
            "fat": 20,
            "protein": 40,
            "description": "Dinner - Steak and Potatoes",
            "name": "Steak Dinner",
            "timestamp": "2025-06-08T17:00:00.000000-08:00",
            "userid": "admin@hw3.com",
            "_id": "11"
        },
        {
            "calories": 200,
            "carbohydrates": 30,
            "fat": 10,
            "protein": 15,
            "description": "Evening Smoothie",
            "name": "Smoothie",
            "timestamp": "2025-06-08T20:00:00.000000-08:00",
            "userid": "admin@hw3.com",
            "_id": "11"
        }
    ];

    // MOCK DATA FOR THE PROGRESS CHART

    let progressData = [
        {
            "_id": { "$oid": "6845294727d84e4d2024ddc1" },
            "calories": true,
            "protein": true,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-10"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddc2" },
            "calories": true,
            "protein": true,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-11"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddc3" },
            "calories": true,
            "protein": false,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-12"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddc4" },
            "calories": true,
            "protein": true,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-13"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddc5" },
            "calories": true,
            "protein": true,
            "fat": false,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-14"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddc6" },
            "calories": true,
            "protein": true,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-15"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddc7" },
            "calories": false,
            "protein": true,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-16"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddc8" },
            "calories": true,
            "protein": true,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-17"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddc9" },
            "calories": true,
            "protein": true,
            "fat": false,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-18"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddca" },
            "calories": true,
            "protein": true,
            "fat": true,
            "carbohydrates": false,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-19"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddcb" },
            "calories": true,
            "protein": true,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-20"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddcc" },
            "calories": true,
            "protein": true,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-21"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddcd" },
            "calories": false,
            "protein": true,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-22"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddce" },
            "calories": true,
            "protein": true,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-23"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddcf" },
            "calories": true,
            "protein": false,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-24"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddd0" },
            "calories": true,
            "protein": true,
            "fat": true,
            "carbohydrates": false,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-25"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddd1" },
            "calories": true,
            "protein": true,
            "fat": false,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-26"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddd2" },
            "calories": true,
            "protein": true,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-27"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddd3" },
            "calories": true,
            "protein": true,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-28"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddd4" },
            "calories": true,
            "protein": true,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-29"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddd5" },
            "calories": false,
            "protein": false,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-30"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddd6" },
            "calories": true,
            "protein": true,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-05-31"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddd7" },
            "calories": true,
            "protein": true,
            "fat": false,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-06-01"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddd8" },
            "calories": true,
            "protein": true,
            "fat": true,
            "carbohydrates": false,
            "userid": "user@hw3.com",
            "timestamp": "2025-06-02"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddd9" },
            "calories": true,
            "protein": true,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-06-03"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024ddda" },
            "calories": true,
            "protein": true,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-06-04"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024dddb" },
            "calories": true,
            "protein": false,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-06-05"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024dddc" },
            "calories": true,
            "protein": true,
            "fat": true,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-06-06"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024dddd" },
            "calories": true,
            "protein": true,
            "fat": false,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-06-07"
        },
        {
            "_id": { "$oid": "6845294727d84e4d2024dee4" },
            "calories": true,
            "protein": true,
            "fat": false,
            "carbohydrates": true,
            "userid": "user@hw3.com",
            "timestamp": "2025-06-08"
        }
    ]
    

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

    // let filteredData:any = null;

    let filteredData = foodData
        .sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()) // Sort by timestamp
        .map(meal => ({
            timestamp: meal.timestamp,
            nutrientValue: meal[selectedNutrient as keyof Meal] as number,  // Assert nutrientValue is a number
        }));
    //END MOCK SECTION
    async function getFoodLogs() {
        selectedNutrient = "calories";  // Define the default selected nutrient

        try {
            const res = await fetch(`/api/getuserfoods?range=${encodeURIComponent("")}`);
            const data = await res.json();
            const foodData = data.foodList;

            console.log(foodData);

            filteredData = foodData
            .sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()) // Sort by timestamp
            .map(meal => ({
                timestamp: meal.timestamp,
                nutrientValue: meal[selectedNutrient as keyof Meal] as number,  // Assert nutrientValue is a number
            }));
            
        } catch (error) {
            console.error("Failed fetch food data:", error);
        }

        
    }
    let goalValue = 2000;
    let buffer = 10;
    //END MOCK SECTION FOR LINE/BAR

    // MOCK SECTION FOR PROGRESS FILTERING
    let view: "today" | "lastWeek" | "lastMonth" = "today";

    function filterProgressData(view: string) {
        const today = new Date();
        today.setHours(0, 0, 0, 0); // normalize to start of day

        if (view === "lastWeek") {
            // last 7 days including today
            const sevenDaysAgo = new Date(today);
            sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 6); // 6 because inclusive of today

            return progressData.filter(item => {
                const itemDate = new Date(item.timestamp);
                return itemDate >= sevenDaysAgo && itemDate <= today;
            });
        } else if (view === "lastMonth") {
            // previous calendar month
            const firstDayThisMonth = new Date(today.getFullYear(), today.getMonth(), 1);
            const lastMonthEnd = new Date(firstDayThisMonth);
            lastMonthEnd.setDate(0); // last day of previous month
            const lastMonthStart = new Date(lastMonthEnd.getFullYear(), lastMonthEnd.getMonth(), 1);

            return progressData.filter(item => {
                const itemDate = new Date(item.timestamp);
                return itemDate >= lastMonthStart && itemDate <= lastMonthEnd;
            });
        } else {
            // Default to show all data or today
            return progressData;
        }
    }

    $: filteredProgress = filterProgressData(view);

    // END MOCK SECTION FOR PROGRESS FILTERING

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
        getFoodLogs();
        fetchInfo();
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
    <!-- <div class="logout">
            <button onclick={redirectToLogout}> Logout </button>
    </div> -->
    <!-- <div class="goals-page">
        <button onclick={redirectToGoals}> My Goals </button>
    </div> -->


    <button class="toggle" onclick={toggleSidebar}>≡ Pages</button>

    <div class="layout">
        {#if showSidebar}
            <aside class="sidebar">
                <ul>
                    <li>Dashboard</li>
                    <li onclick={redirectToMeals}>My Meals</li>
                    <li onclick={redirectToGoals}>My Goals</li>
                    <!-- <li onclick ={redirectToAddFood}></li> -->
                    <li onclick={redirectToLogout}>Logout</li>
                </ul>
            </aside>
        {/if}

        <main class="content">
            <header>
                <h1>My Dashboard</h1>
                <div class="tabs">
                    <button>Today</button>
                    <button>This Week</button>
                    <button>Last Month</button>
                </div>
            </header>

        <div class="summary-cards">
            <div class="card">
                <h3>Calories</h3>
                <ProgressChart
                    filteredData={filteredProgress}
                    {selectedNutrient}
                    width={300}
                    height={300}
                />
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
                <BarChart
                    {filteredData}
                    {goalValue}
                    {buffer}
                    height={400}
                    width={600}
                    selectedNutrient={selectedNutrient}
                    startHour={6}
                    endHour={23}
                />
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

                <div class="card">
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
        </main>
    </div>
</div>

        


        <!-- <div class="top-controls">
            
        </div>
        <input type="text" placeholder="Search...">
        

        <div class="main-grid">
            <div class="card large">
                <h3>Today's Calories</h3>
                <div class="graph-placeholder">[Bar Graph]</div>
            </div>

            <div class="card-meals">
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
                <LineChart 
                    {filteredData} 
                    {goalValue} 
                    {buffer} 
                    height={400} 
                    width={600} 
                    selectedNutrient={selectedNutrient}
                />
            </div>
        </div>
    </div>
</div> -->

<style>
    /* .dashboard-container {
        padding: 2rem;
        /* background-color: #fafafa;
        /* background-color: #121212;
        color: white;
        font-family: sans-serif;
    } */
    .dashboard-container {
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
        /* width: 100%; */
        padding: 0.75rem;
        cursor: pointer;
        border-radius: 6px;
    }

    .sidebar li:hover, .sidebar li:active {
        background-color: #2a2a2a;
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

    .card {
        background-color: #121212; /*diff*/
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 0 5px rgba(0, 0, 0, 0, 0.4);
    }

    .card h2, .card h3 {
        margin-top: 0;
    }

    .card p {
        font-size: 1.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }

    .card small {
        color: #bbb;
    }

    /* .card.large {
        grid-column: span 2;
    } */

    main {
        width: 100%;
    }

    .main-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        color: white;
    }

    th, td {
        text-align: left;
        padding: 0.4rem;
        border-bottom: 1px solid #333;
    }

    th {
        background-color: #2a2a2a;
        color: #ccc;
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

</style>
