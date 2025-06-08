<script lang="ts">
    import { onMount, afterUpdate } from 'svelte';
    import * as d3 from 'd3';

    // Working Chart Version!
    // Playing to the strengths of the line chart; dynamic X axis for time. Bar chart will display the entire day.
    // D3 set up with our project, must be done in frontend
    /*
        cd frontend
        npm install d3@7

    */

    //    How to use:
    /* 
    Example call
    <LineChart {filteredData} {goalValue} {buffer} height={400} width={600} selectedNutrient={selectedNutrient} />
    Pass the data in the form
    
        [
            {
                timestamp: "2025-06-08T08:00:00.000000-08:00",
                nutrientValue: 300
            },
            {
                timestamp: "2025-06-08T10:15:00.000000-08:00",
                nutrientValue: 450
            },
                //etc
        ]
    Where the data is sorted by timestamp.
    Goal Value can be modified, because the goal for different nutrients is different
    Buffer = What percent PAST the goal value do you want to show. So if the goal is 2000 and buffer is 10, graph Y axis will be 2200
    Height and Width for reusability
    SelectedNutrient so we can pass the nutrient on the page
    */

    // Props passed from the parent, again, these will be edited.
    export let filteredData: { timestamp: string, nutrientValue: number }[] = []; 
    export let goalValue: number = 2000;                    // Example goal (e.g., 2000 calories)
    export let buffer: number = 10;                         // 10% buffer above the goal
    export let height: number = 300;                        // Graph height
    export let width: number = 600;                         // Graph width
    export let selectedNutrient: string = 'calories';       // Nutrient to display (calories, protein, etc.)

    let svg: SVGSVGElement;

    // Margins and inner size of the chart
    const margin = { top: 20, right: 30, bottom: 50, left: 60 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    // Function to draw the chart
    function drawChart() {
        if (!svg || !filteredData.length) return; // If no SVG or data, don't render

        const cumulativeData = [];
        let total = 0;
        for (const d of filteredData) {
            total += d.nutrientValue;
            cumulativeData.push({ timestamp: d.timestamp, nutrientValue: total });
        }

        // Clear previous content
        const svgSelection = d3.select(svg);
        svgSelection.selectAll('*').remove();

        // Create the main group inside SVG (taking margins into account)
        const chartGroup = svgSelection
            .append('g')
            .attr('transform', `translate(${margin.left}, ${margin.top})`);

        // Create X scale (based on timestamp)
        const xScale = d3.scaleTime()
            .domain([d3.min(filteredData, d => new Date(d.timestamp))!, d3.max(cumulativeData, d => new Date(d.timestamp))!])
            .range([0, innerWidth]);

        // Create Y scale (based on nutrient value)
        const maxY = Math.max(
            d3.max(cumulativeData, d => d.nutrientValue) ?? 0, // was filteredData, now cumulative data
            goalValue * (1 + buffer / 100)
        );

        const yScale = d3.scaleLinear()
            .domain([0, maxY])
            .range([innerHeight, 0]);


        // X-Axis with tick labels
        chartGroup.append('g')
            .attr('transform', `translate(0, ${innerHeight})`)
            .call(d3.axisBottom(xScale)
                .tickFormat(d3.timeFormat('%-I %p'))        // "9 AM" not "09 AM"
            )
            .call(g => g.selectAll('.tick line').remove())
            .call(g => g.select('.domain').remove())
            .selectAll('.tick text')
            .style('fill', 'black');

        // Create Y axis
        // Y-Axis grid lines
        chartGroup.append("g")
        .attr("class", "grid")
        .call(
            d3.axisLeft(yScale)
            .tickSize(-innerWidth)
            .tickFormat(() => "")
        )
        .selectAll("line")
        .attr("stroke", "#eee");

        // Y-Axis itself
        chartGroup.append('g')
            .attr("class", "y-axis-labels")
            .call(d3.axisLeft(yScale))
            .call(g => g.select('.domain').attr("stroke", "#eee")) // Set same grey as grid
            .call(g => g.selectAll('.tick line').remove())         // Remove black ticks
            .selectAll("text")
            .style("fill", "black");

        // Line generator for the nutrient data (Smooth line with curveMonotoneX)
        const line = d3.line<{ timestamp: string; nutrientValue: number }>()
            .x(d => xScale(new Date(d.timestamp)))  // Convert timestamp to date for X axis
            .y(d => yScale(d.nutrientValue))  // Map nutrient value to Y axis
            .curve(d3.curveMonotoneX);  // Smooth the line

        // Add the line to the graph
        chartGroup.append('path')
        .data([cumulativeData])
        .attr('class', 'line')
        .attr('d', line)
        .attr('fill', 'none')
        .attr('stroke', 'black')
        .attr('stroke-width', 3)
        .attr('stroke-linejoin', 'round')
        .attr('stroke-linecap', 'round');

        const last = cumulativeData[cumulativeData.length - 1];

        // Highlight last point
        chartGroup.append('circle')
            .attr('cx', xScale(new Date(last.timestamp)))
            .attr('cy', yScale(last.nutrientValue))
            .attr('r', 6)
            .attr('fill', 'black');

        // Optional: glow effect
        chartGroup.append('circle')
            .attr('cx', xScale(new Date(last.timestamp)))
            .attr('cy', yScale(last.nutrientValue))
            .attr('r', 15)
            .attr('fill', 'lightgray')
            .attr('opacity', 0.3);

        // Add goal line (horizontal)
        chartGroup.append('line')
            .attr('x1', 0)
            .attr('x2', innerWidth)
            .attr('y1', yScale(goalValue))
            .attr('y2', yScale(goalValue))
            .attr('stroke', selectedNutrient.toLowerCase() === 'fat' ? 'red' : '#07c')  // Red if fat, blue otherwise// .attr('stroke', '#07c') // This makes the line blue if we prefer
            .attr('stroke-width', 2);


        // If you want to add a buffer line, like the goal line. Currently, it makes no sense, sense the buffer is our cap
        /*
        chartGroup.append('line')
            .attr('x1', 0)
            .attr('x2', innerWidth)
            .attr('y1', yScale(goalValue * (1 + buffer / 100)))
            .attr('y2', yScale(goalValue * (1 + buffer / 100)))
            .attr('stroke', 'orange')
            .attr('stroke-dasharray', '5,5')
            .attr('stroke-width', 2);
        */

        // X and Y axis labels (if applicable)
        svgSelection.append('text')
            .attr('x', width / 2)
            .attr('y', height - 10)
            .attr('text-anchor', 'middle')
            .style('fill', 'black') //Style black
            .text('Time');  // X Axis label ("Time" for example)

        // Y-axis label (Nutrient value)
        svgSelection.append('text')
            .attr('transform', 'rotate(-90)')
            .attr('x', -height / 2)
            .attr('y', 20)
            .attr('text-anchor', 'middle')
            .style('fill', 'white')  // Make label text white (Currently to make it invisible, as in the figma. It exists but not visible)
            .text(selectedNutrient.charAt(0).toUpperCase() + selectedNutrient.slice(1))  // Y Axis label (nutrient name, e.g., "Calories")
    }

    // Redraw chart when data or props change
    onMount(() => {
        drawChart();
    });

    afterUpdate(() => {
        drawChart();
    });

</script>

<!-- The SVG where the graph will be rendered -->

<!-- Old, ugly style-->
<!--  <svg bind:this={svg} width={width} height={height} style="background: #121212"></svg> -->
<svg bind:this={svg} width={width} height={height} style="background: #fff"></svg>


<style>
    svg {
        font-family: 'Inter', system-ui, sans-serif;
        color: black;
        background-color: white;
    }

    .domain,
    .tick line {
        stroke: #ddd; /* Lighter for grid line feel */
    }

    .tick text {
        fill: #555;
    }

    .line {
        stroke: #07c;  /* Light blue color for the line */
        stroke-width: 2;
    }
</style>