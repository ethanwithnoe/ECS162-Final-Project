<script>
	import Dashboard from './Dashboard.svelte';
    import { onMount } from 'svelte';
    let userEmail = null;

    onMount(async () => {
        const res = await fetch("/api/getinfo");
        const data = await res.json();
        if (!data.email) {
            window.location.href = "/"
        }
        else {
            userEmail = data.email;
        }
    })
</script>

<div class="dashboard-container">
    <h1>Dashboard</h1>

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
            <ul>
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
        background-color: #121212;
        color: white;
        font-family: sans-serif;
    }

    h1 {
        font-size: 2rem;
        margin-bottom: 1.5rem;
    }

    .top-controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        flex-wrap: wrap;
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
    }

    .main-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
    }

    .card {
        /* background: ; */
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 0 4px rgba(0,0,0,0,0.05);
    }

    .card.large {
        grid-column: span 2;
    }

    table {
        width: 100%;
        border-collapse: collapse;
    }

    th,td {
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