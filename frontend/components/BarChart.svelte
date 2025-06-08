<script lang="ts">
    import { onMount, afterUpdate } from 'svelte';
    /* For my own ease;
    docker-compose -f docker-compose.dev.yml up --build
    */
    /*
    I originally tried building the radial progress charts in d3 to handle the transitions,
    but I had a ton of issues trying to get d3 with the actual project, and I had to scrap
    my work. So I'm moving to the simplest graph, to get proof of concept down

    TODO:
    Make the bar chart cumulative and not separate by hour.
    Test dynamic update as foods are drawn - will we update food on the page or in a different menu?
    Test date reset. Can't do this without db hookup
    Fix Axes and labels
    Fix aesthetics. The chart is horrific.
    */

    // Props
    export let nutrient: 'calories' | 'protein' | 'fat' | 'carbohydrates';
    export let goal: number;
    export let buffer: number; //So the goal isn't the top, configurable by frontend call, idea is roughly 10%

    export let foodLogs: {
        
        timestamp: string;
        calories: number;
        protein: number;
        fat: number;
        carbohydrates: number;
    }[];

    let canvas: HTMLCanvasElement;
    const width = 600;
    const height = 300;

    const leftPadding = 40;
    const bottomPadding = 30;
    const topPadding = 10;
    const rightPadding = 10;

    const startHour = 5;
    const endHour = 24;
    const binCount = endHour - startHour; // 19 bins: 5am–6am, ..., 11pm–12am. Currently bugs at noon. Also very ugly

    function drawChart() {
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        ctx.clearRect(0, 0, width, height);

        // Create hourly bins
        const bins = new Array(binCount).fill(0);

        for (const log of foodLogs) {

            const date = new Date(log.timestamp);
            const hour = date.getHours();

            if (hour >= startHour && hour < endHour) {
                
                const index = hour - startHour;
                bins[index] += log[nutrient];
            }
        }

        const maxY = goal + buffer;
        const chartWidth = width - leftPadding - rightPadding;
        const chartHeight = height - topPadding - bottomPadding;

        // Draw Y-axis (0 to maxY)
        ctx.strokeStyle = '#000';
        ctx.beginPath();
        ctx.moveTo(leftPadding, topPadding);
        ctx.lineTo(leftPadding, height - bottomPadding);
        ctx.stroke();

        // Draw X-axis
        ctx.beginPath();
        ctx.moveTo(leftPadding, height - bottomPadding);
        ctx.lineTo(width - rightPadding, height - bottomPadding);
        ctx.stroke();

        // Draw bars
        const barWidth = chartWidth / binCount;

        // Do we want the bars color mapped? Or static neutral colors like our figma
        const barColorMap = {       

            calories: '#067FD0',        // Navy Blue
            protein: '#128FC8',         // Pacific Blue
            fat: '#797EF6',                     // "Cornflower blue"?
            carbohydrates: '#1E80C1'    // "Pelorous"

        };

        ctx.fillStyle = barColorMap[nutrient];

        for (let i = 0; i < binCount; i++) {

            const x = leftPadding + i * barWidth;
            const barHeight = (bins[i] / maxY) * chartHeight;
            const y = height - bottomPadding - barHeight;
            ctx.fillRect(x, y, barWidth - 1, barHeight);
        }

        // Draw hour labels
        ctx.fillStyle = '#000';
        ctx.font = '10px sans-serif';
        ctx.textAlign = 'center';

        for (let i = 0; i < binCount; i++) {

            const hour = startHour + i;
            const label = hour === 24 ? 'Mid' : hour <= 11 ? `${hour} AM` : `${hour - 12} PM`;
            const x = leftPadding + i * barWidth + barWidth / 2;
            ctx.fillText(label, x, height - 5);

        }

        // Optional: goal and buffer lines
        ctx.strokeStyle = '#999';
        ctx.setLineDash([4, 2]);

        const goalY = height - bottomPadding - (goal / maxY) * chartHeight;
        ctx.beginPath();
        ctx.moveTo(leftPadding, goalY);
        ctx.lineTo(width - rightPadding, goalY);
        ctx.stroke();

        const bufferY = height - bottomPadding - (buffer / maxY) * chartHeight;
        ctx.beginPath();
        ctx.moveTo(leftPadding, bufferY);
        ctx.lineTo(width - rightPadding, bufferY);
        ctx.stroke();

        ctx.setLineDash([]);
    }

    onMount(drawChart);
    afterUpdate(drawChart);
    </script>

    <canvas bind:this={canvas} width={width} height={height}></canvas>