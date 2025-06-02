<script lang="ts">
    export let onFoodAdded: (data: any) => void;
    let manualMode = false;
    let searchQuery = "";
    let searchResults: any[] = [];
    let chosenFood: any = null;
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
            searchResults = data.foods.slice(0, 50); 
        } catch (e) {
            console.error("Network Error:", e);
            searchResults = [];
        }
    }
    function selectFood(item) {
        chosenFood = item;
        userMacros = {
            name : item.name ?? 0,
            calories: item.calories ?? 0,
            protein: item.protein ?? 0,
            fat: item.fat ?? 0,
            carbohydrates: item.carbohydrates ?? 0
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
        if(onFoodAdded) onFoodAdded(result);
    }

    function nutrientByName(item: any, nutrientName: string) { 
        return item.foodNutrients.find((n: any) => n.nutrientName === nutrientName)?.value || "?";
    }

</script>

<div> 
    <h2> Add Food of Choice! </h2>
    <input type="text" bind:value={searchQuery} placeholder="Search food..." />
    <button on:click={foodSearch}>Search</button>
    <button on:click = {() => {
        chosenFood = { description: "Enter Manually" };
        manualMode = true;
    }}>+ Add Food Manually</button>

    {#if searchResults.length > 0} 
        <ul>
            {#each searchResults as item}
                <li on:click={() => selectFood(item)}>
                    <strong>{item.brandName ? item.brandName + ":" : ""}</strong> {item.description}<br /> 
                    Calories:       {nutrientByName(item, "Energy" )} kcal |
                    Protein:        {nutrientByName(item, "Protein")} g |
                    Fat:            {nutrientByName(item, "Total lipid (fat)")} g |
                    Carbohydrates   {nutrientByName(item, "Carbohydrate, by difference")} g
                </li>
            {/each}
        </ul>
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
        margin-top: 10px;
    }
    td {
        padding: 5px;
    }
</style>