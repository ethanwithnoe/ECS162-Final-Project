<script lang="ts">
    import { onMount, afterUpdate } from 'svelte';
    import * as d3 from 'd3';

    /*

    Draft version, all this does is display the number of days out of the total days in the time period.
    Parent page using this component needs to filter the data by time period.
    I already included a sample function to filter the data, as well as our hideous block of mock data.
    The mock data in Dashboard is REALLY long and ugly, but it's pulling the filtered data correctly.

    TODO FOR ALL CHARTS: Fill our actual database with user data, remove the mock data and hook them up by user.

        Sample call

<ProgressChart
    filteredData={filteredProgress}
    {selectedNutrient}
    width={300}
    height={300}
/>
    */

    // Props section
    export let filteredData: {
        timestamp: string;
        calories: boolean;
        protein: boolean;
        fat: boolean;
        carbohydrates: boolean;
    }[] = [];

    export let selectedNutrient: 'calories' | 'protein' | 'fat' | 'carbohydrates' = 'calories';
    export let width: number = 300;
    export let height: number = 300;

    const margin = { top: 20, right: 20, bottom: 40, left: 20 };

    let svg: SVGSVGElement;

    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const radius = Math.min(innerWidth, innerHeight) / 2;
    const thickness = radius * 0.3;

    function drawChart() {
        if (!svg) return;

        const svgSelection = d3.select(svg);
        svgSelection.selectAll('*').remove();

        const chartGroup = svgSelection
        .append('g')
        .attr('transform', `translate(${margin.left + innerWidth / 2}, ${margin.top + innerHeight / 2})`);

        const totalDays = filteredData.length;
        const achievedDays = filteredData.filter(d => d[selectedNutrient]).length;

        if (totalDays === 0) {
            // No data: show a message or empty chart
            chartGroup.append('text')
                .attr('text-anchor', 'middle')
                .style('font-size', '1.5rem')
                .style('fill', '#666')
                .text('No data');
            return;
        }

        // Calculate the completion percentage
        const completionPercentage = (achievedDays / totalDays) * 100;

        // Scale from 0 to totalDays mapped to 0 to 2π radians
        const angleScale = d3.scaleLinear()
        .domain([0, totalDays])
        .range([0, 2 * Math.PI])
        .clamp(true);

        // Background full circle arc (light gray)
        const arcBackground = d3.arc()
        .innerRadius(radius - thickness)
        .outerRadius(radius)
        .startAngle(0)
        .endAngle(2 * Math.PI);

        // Foreground arc for achieved days
        const arcForeground = d3.arc()
        .innerRadius(radius - thickness)
        .outerRadius(radius)
        .startAngle(0)
        .endAngle(angleScale(achievedDays));

        // Draw background arc
        chartGroup.append('path')
            .attr('d', arcBackground({
                innerRadius: radius - thickness,
                outerRadius: radius,
                startAngle: 0,
                endAngle: 2 * Math.PI,
            })!)
            .attr('fill', '#eee');

        // Draw foreground arc
        chartGroup.append('path')
            .attr('d', arcForeground({
                innerRadius: radius - thickness,
                outerRadius: radius,
                startAngle: 0,
                endAngle: angleScale(achievedDays),
            })!)
            .attr('fill', 'black'); // 'black' if you want it to be black instead, for frontend devs

        // Center text: completion percentage
        chartGroup.append('text')
            .attr('text-anchor', 'middle')
            .attr('dy', '-0.2em')
            .style('font-size', `${radius * .2}px`)  // Scale the text size relative to the radius
            .style('fill', 'black')
            .text(`${completionPercentage.toFixed(1)}%`);  // Display percentage with 1 decimal place

        // Center text: total days label
        chartGroup.append('text')
            .attr('text-anchor', 'middle')
            .attr('dy', '1.2em')
            .style('font-size', `${radius * 0.2}px`)  // Scale the text size relative to the radius
            .style('fill', 'black')
            .text(`completion`);
    }

    onMount(() => drawChart());
    afterUpdate(() => drawChart());
</script>

<svg bind:this={svg} {width} {height} style="background: #fff;"></svg>

<style>
    svg {
        font-family: 'Inter', system-ui, sans-serif;
        color: black;
        background-color: white;
    }
</style>
