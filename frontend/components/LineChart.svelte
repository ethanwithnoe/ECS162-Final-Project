<script lang="ts">
    import { onMount, afterUpdate } from 'svelte';
    import * as d3 from 'd3';

    // Props passed from the parent
    export let filteredData: { timestamp: string, nutrientValue: number }[] = []; 
    export let goalValue: number = 2000;  // Example goal (e.g., 2000 calories)
    export let buffer: number = 10;  // 10% buffer above the goal
    export let height: number = 300;  // Graph height
    export let width: number = 600;   // Graph width
    export let selectedNutrient: string = 'calories';  // Nutrient to display (calories, protein, etc.)

    let svg: SVGSVGElement;

    // Margins and inner size of the chart
    const margin = { top: 20, right: 30, bottom: 50, left: 60 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    // Function to draw the chart
    function drawChart() {
        if (!svg || !filteredData.length) return; // If no SVG or data, don't render

        // Clear previous content
        const svgSelection = d3.select(svg);
        svgSelection.selectAll('*').remove();

        // Create the main group inside SVG (taking margins into account)
        const chartGroup = svgSelection
            .append('g')
            .attr('transform', `translate(${margin.left}, ${margin.top})`);

        // Create X scale (based on timestamp)
        const xScale = d3.scaleTime()
            .domain([d3.min(filteredData, d => new Date(d.timestamp))!, d3.max(filteredData, d => new Date(d.timestamp))!])
            .range([0, innerWidth]);

        // Create Y scale (based on nutrient value)
        const yScale = d3.scaleLinear()
            .domain([0, d3.max(filteredData, d => d.nutrientValue)!])
            .range([innerHeight, 0]);

        // Create X axis
        chartGroup.append('g')
            .attr('transform', `translate(0, ${innerHeight})`)
            .call(d3.axisBottom(xScale))
            .selectAll('.tick text')
            .style('fill', 'white');  // Make tick labels white

        // Create Y axis
        chartGroup.append('g')
            .call(d3.axisLeft(yScale))
            .selectAll('.tick text')
            .style('fill', 'white');  // Make tick labels white

        // Line generator for the nutrient data (Smooth line with curveMonotoneX)
        const line = d3.line()
            .x(d => xScale(new Date(d.timestamp)))  // Convert timestamp to date for X axis
            .y(d => yScale(d.nutrientValue))  // Map nutrient value to Y axis
            .curve(d3.curveMonotoneX);  // Smooth the line

        // Add the line to the graph
        chartGroup.append('path')
            .data([filteredData])
            .attr('class', 'line')
            .attr('d', line)
            .attr('fill', 'none')
            .attr('stroke', '#07c')  // Blue line color
            .attr('stroke-width', 2);

        // Add goal line (horizontal)
        chartGroup.append('line')
            .attr('x1', 0)
            .attr('x2', innerWidth)
            .attr('y1', yScale(goalValue))
            .attr('y2', yScale(goalValue))
            .attr('stroke', 'red')
            .attr('stroke-dasharray', '5,5')
            .attr('stroke-width', 2);

        // Add buffer line (above the goal)
        chartGroup.append('line')
            .attr('x1', 0)
            .attr('x2', innerWidth)
            .attr('y1', yScale(goalValue * (1 + buffer / 100)))
            .attr('y2', yScale(goalValue * (1 + buffer / 100)))
            .attr('stroke', 'orange')
            .attr('stroke-dasharray', '5,5')
            .attr('stroke-width', 2);

        // Add labels if provided
        if (selectedNutrient) {
            svgSelection.append('text')
                .attr('x', width / 2)
                .attr('y', height - 10)
                .attr('text-anchor', 'middle')
                .style('fill', 'white')  // Make label text white
                .text(selectedNutrient);  // Nutrient name label
        }

        // X and Y axis labels (if applicable)
        svgSelection.append('text')
            .attr('x', width / 2)
            .attr('y', height - 10)
            .attr('text-anchor', 'middle')
            .style('fill', 'white')  // Make label text white
            .text('Time');  // X Axis label ("Time" for example)

        // Y-axis label (Nutrient value)
        svgSelection.append('text')
            .attr('transform', 'rotate(-90)')
            .attr('x', -height / 2)
            .attr('y', 20)
            .attr('text-anchor', 'middle')
            .style('fill', 'white')  // Make label text white
            .text(selectedNutrient);  // Y Axis label (nutrient name, e.g., "Calories")
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

<svg bind:this={svg} width={width} height={height} style="background: #121212"></svg>

<style>
    svg {
        font-family: sans-serif;  /* Modern sans-serif font */
        color: white;
    }

    .domain,
    .tick line {
        stroke: white;  /* White for axis lines */
    }

    .tick text {
        fill: white;  /* White for axis tick text */
    }

    .line {
        stroke: #07c;  /* Light blue color for the line */
        stroke-width: 2;
    }
</style>