<script lang="ts">
    import { onMount, afterUpdate } from 'svelte';
    import * as d3 from 'd3';

    // Working Chart Version!
    // Playing to the strengths of the bar chart chart; set  X axis for time. Shows exactly when the user ate. Shows all day.
    /*
    I had to do some ugly magic to get the style from our figma down; by default, svg can't make bars with rounded tops but straight-edged bottoms.
    Thus, I superimposed a smaller, tiny bar on top of every bar that doesn't have 0 as a value.
    */
    // D3 set up with our project, must be done in frontend
    /*
        cd frontend
        npm install d3@7

    */

    //    How to use:
    /* 
    Example call
    <BarChart {filteredData} {goalValue} {buffer} height={400} width={600} selectedNutrient={selectedNutrient} startHour={6} endHour={24} />
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
    startHour / endHour adjust the beginning and end of the X axis.
    */

    // Props passed from the parent, again, these will be edited.

    export let filteredData: { timestamp: string, nutrientValue: number }[] = [];
    export let goalValue: number = 2000;
    export let buffer: number = 10;
    export let height: number = 300;
    export let width: number = 600;
    export let selectedNutrient: string = 'calories';
    export let startHour: number = 6;
    export let endHour: number = 24;

    let svg: SVGSVGElement;

    const margin = { top: 20, right: 30, bottom: 50, left: 60 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    function drawChart() {
        if (!svg || !filteredData.length) return;

        const svgSelection = d3.select(svg);
        svgSelection.selectAll('*').remove();

        const chartGroup = svgSelection
        .append('g')
        .attr('transform', `translate(${margin.left}, ${margin.top})`);

        const hourBins = d3.range(startHour, endHour + 1);
        const binned = new Map<number, number>();

        for (let hour of hourBins) binned.set(hour, 0);

        for (let d of filteredData) {
        const hour = new Date(d.timestamp).getHours();
        if (hour >= startHour && hour <= endHour) {
            for (let h = hour; h <= endHour; h++) {
            binned.set(h, (binned.get(h) ?? 0) + d.nutrientValue);
            }
        }
        }

        const data = hourBins.map(hour => ({
        hour,
        cumulative: binned.get(hour) ?? 0
        }));

        const xScale = d3.scaleBand()
        .domain(data.map(d => d.hour.toString()))
        .range([0, innerWidth])
        .padding(0.1);

        const maxY = Math.max(
        d3.max(data, d => d.cumulative) ?? 0,
        goalValue * (1 + buffer / 100)
        );

        const yScale = d3.scaleLinear()
        .domain([0, maxY])
        .range([innerHeight, 0]);

        chartGroup.append('g')
        .attr('transform', `translate(0, ${innerHeight})`)
        .call(d3.axisBottom(xScale).tickFormat(d => `${+d % 12 || 12}${+d < 12 ? 'AM' : 'PM'}`)) // removed space here
        .call(g => g.selectAll('.tick line').remove())
        .call(g => g.select('.domain').remove())
        .selectAll('.tick text')
        .style('fill', 'black');

        chartGroup.append("g")
        .call(d3.axisLeft(yScale).tickSize(-innerWidth).tickFormat(() => ""))
        .selectAll("line")
        .attr("stroke", "#eee");

        chartGroup.append('g')
        .call(d3.axisLeft(yScale))
        .call(g => g.select('.domain').attr("stroke", "#eee"))
        .call(g => g.selectAll('.tick line').remove())
        .selectAll("text")
        .style("fill", "black");

        // MAIN bars with rounded top edges only
        chartGroup.selectAll('.bar')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', 'bar')
        .attr('x', d => xScale(d.hour.toString())!)
        .attr('y', d => yScale(d.cumulative))
        .attr('width', xScale.bandwidth())
        .attr('height', d => innerHeight - yScale(d.cumulative))
        .attr('fill', 'black')
        .attr('rx', 3) // rounds all corners
        .attr('ry', 3);

        // OVERLAY rectangles at bottom to mask rounded corners, *STYLE!*
        // ONLY for bars where cumulative > 0 to avoid overlay on empty bars
        chartGroup.selectAll('.bar-overlay')
        .data(data.filter(d => d.cumulative > 0))       // <-- filter here to skip zero bars
        .enter()
        .append('rect')
        .attr('class', 'bar-overlay')
        .attr('x', d => xScale(d.hour.toString())!)
        .attr('y', innerHeight - 6)                     // height of overlay is 6px, placed at bottom of main bars
        .attr('width', xScale.bandwidth())
        .attr('height', 6)                              // same as rx radius, covers bottom rounded corners
        .attr('fill', 'black');

        chartGroup.append('line')
        .attr('x1', 0)
        .attr('x2', innerWidth)
        .attr('y1', yScale(goalValue))
        .attr('y2', yScale(goalValue))
        .attr('stroke', selectedNutrient.toLowerCase() === 'fat' ? 'red' : '#07c')
        .attr('stroke-width', 2);

        svgSelection.append('text')
        .attr('x', width / 2)
        .attr('y', height - 10)
        .attr('text-anchor', 'middle')
        .style('fill', 'black')
        .text('Time');

        svgSelection.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('x', -height / 2)
        .attr('y', 20)
        .attr('text-anchor', 'middle')
        .style('fill', 'white')
        .text(selectedNutrient.charAt(0).toUpperCase() + selectedNutrient.slice(1));
    }

    onMount(() => drawChart());
    afterUpdate(() => drawChart());
    </script>

    <svg bind:this={svg} width={width} height={height} style="background: #fff"></svg>

    <style>
    svg {
        font-family: 'Inter', system-ui, sans-serif;
        color: black;
        background-color: white;
    }
</style>