<script lang="ts">
  import { browser } from "$app/environment";
  import { Chart, type ChartConfiguration } from "chart.js/auto";
  import { onMount } from "svelte";

  let { ramData } = $props();

  let chartConfig: ChartConfiguration = {
    data: {
      labels: [...Array(60).keys()],
      datasets: [
        {
          label: "Memory Usage",
          data: $state.snapshot(ramData),
          fill: true,
          tension: 0.0,
          backgroundColor: "#FFB1C1",
        },
      ],
    },
    type: "line",
    options: {
      animation: {
        duration: 0,
      },
      scales: {
        x: {
          min: 0,
          max: 60,
          beginAtZero: true,
        },
        y: {
          beginAtZero: true,
          min: 0,
          max: 100,
        },
      },
    },
  };

  // TODO: Fix this type error
  let canvasElement: HTMLCanvasElement;
  let chart: Chart;
  onMount(() => {
    if (browser) {
      // TODO: Make this more svelte-y
      canvasElement = document.getElementById("ram-usage-graph");
      chart = new Chart(canvasElement, chartConfig);
    }
  });

  $effect(() => {
    chart.data.datasets.forEach((dataset) => {
      dataset.data = $state.snapshot(ramData);
    });
    chart.update();
  });
</script>

<canvas id="ram-usage-graph"></canvas>
