<script lang="ts">
    export let onFoodAdded: (data: any) => void;
    let manualMode = false;
    let searchQuery = "";
    let searchResults: any[] = [];
    let chosenFood: any = null;
    let visibleCount = 10;
    let userMacros = {
        name: "",
        calories: 0,
        protein: 0,
        fat: 0,
        carbohydrates: 0
    };
    $: if (manualMode && !chosenFood) {
        chosenFood = { description: "Enter Manually" };
    }
    async function foodSearch() {
        if(!searchQuery) return;
        try{
            const url = `/api/search?query=${encodeURIComponent(searchQuery)}`; //get from backend now
            const options = {
            method: "GET",
            headers: {
                "Accept": "application/json",
            },
        };
        const res = await fetch(url, options); 
        if(!res.ok) {
            const text = await res.text();
            console.error("Fetch failed:", res.status, text);
            return;
        }
            const data = await res.json();
            console.log("search results:", data)
            searchResults = data.foods.slice(0, 100); 
        } catch (e) {
            console.error("Network Error:", e);
            searchResults = [];
        }
    }
    function selectFood(item: any) {
        chosenFood = item;
        userMacros = {
            name : item.description ?? 0,
            calories: nutrientByName(item, "Energy") ?? 0,
            protein: nutrientByName(item, "Protein") ?? 0,
            fat: nutrientByName(item, "Total lipid (fat)") ?? 0,
            carbohydrates: nutrientByName(item, "Carbohydrate, by difference") ?? 0
        };
        //COMMENTED OUT TO SEE FOOD BETTER PUT BACK IN ON LATER DATE
        //searchResults = [];
    }
    
    async function submitFood() {
        const res = await fetch("/api/addfood", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ...chosenFood, ...userMacros})
        });
        const result = await res.json();
        console.log("Saved:", result);
        visibleCount = 5;
        if(onFoodAdded) onFoodAdded(result);
    }

    function nutrientByName(item: any, nutrientName: string) { 
        return item.foodNutrients.find((n: any) => n.nutrientName === nutrientName)?.value || "?";
    }
    function viewMore() {
        visibleCount = visibleCount + 10;
    }
</script>

    
<div class="table-wrap">

    <button class="exit" on:click={() => onFoodAdded(null)}>X</button>
    <h2> Add Food of Choice! </h2>
    
    <div class="search">
        <input type="text" bind:value={searchQuery} placeholder="Search food..." />
        <button on:click={foodSearch}>Search</button>
        <button on:click = {() => {
            chosenFood = { description: "Enter Manually" };
            manualMode = true;
        }}>+ Add Food Manually</button>
    </div>
    
    {#if searchResults.length > 0} 
        <ul>
            {#each searchResults.slice(0, visibleCount) as item}
                <li on:click={() => selectFood(item)}>
                    <strong>{item.brandName ? item.brandName + ":" : ""}</strong> {item.description}<br /> 
                    Calories:       {nutrientByName(item, "Energy" )} kcal |
                    Protein:        {nutrientByName(item, "Protein")} g |
                    Fat:            {nutrientByName(item, "Total lipid (fat)")} g |
                    Carbohydrates   {nutrientByName(item, "Carbohydrate, by difference")} g
                </li>
            {/each}
        </ul>
        {#if visibleCount < searchResults.length}
                    <button on:click={viewMore}>View More</button>
        {/if}
    {:else} 
        <p>No results</p>
    {/if}
    {#if chosenFood || manualMode} 
        <h3> Macros for {chosenFood.description}</h3>
        <table>
            <tbody>
                <tr><td>Name</td><td><input type="string" bind:value={userMacros.name} /></td></tr>
                <tr><td>Calories</td><td><input type="number" bind:value={userMacros.calories} /></td></tr>
                <tr><td>Protein (g)</td><td><input type="number" bind:value={userMacros.protein} /></td></tr>
                <tr><td>Fat (g)</td><td><input type="number" bind:value={userMacros.fat} /></td></tr>
                <tr><td>Carbohydrates (g)</td><td><input type="number" bind:value={userMacros.carbohydrates} /></td></tr>
            </tbody>
        </table>
        <button on:click={submitFood}>Submit</button>
    {/if} 
</div>
<style>
    ul {list-style: none; 
        padding: 0; 
        max-height: 300px;
        overflow-y: auto; 
    }
    li { 
        margin: 10px 0;
        background: grey;
        padding: 10px;
        cursor: pointer;
    }
    li:hover {
        background: rgb(109, 109, 109);
    }
    input[type="text"], input[type="number"] { 
        margin: 5px;
    }
    table {
        max-height: 200px;
        margin-top: 10px;
    }
    td {
        padding: 5px;
    }
    .table-wrap {
        position: relative;
        padding: 20px;
        border: 1px solid black;
        border-radius: 8px;
        background-color: rgba(0, 0, 0, 0.219);
        border: 1px solid rgb(26, 72, 109);
        border-radius: 8px;
        width: 50%;
        margin: 20px auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 10px;
    }
    .search {
        display: flex;
        flex-direction: row;
        gap: 10px; 
        margin-bottom: 15px;
        justify-content: center;
    }
    .exit {
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgb(109, 109, 109);
        color: white;
        font-size: 1.2rem;
        border: 1px solid black;
        cursor: pointer;
    }
    .exit:hover {
        color: red;
    }
</style>