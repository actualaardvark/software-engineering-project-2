<script lang="ts">
  import { browser } from "$app/environment";
  import { Chart, type ChartConfiguration } from "chart.js/auto";
  import { onMount } from "svelte";

  let { cpuData } = $props();

  let chartConfig: ChartConfiguration = {
    data: {
      labels: [...Array(60).keys()],
      datasets: [
        {
          label: "CPU Usage",
          data: $state.snapshot(cpuData),
          fill: true,
          tension: 0.0,
          backgroundColor: "#9BD0F5",
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
      canvasElement = document.getElementById("cpu-usage-graph");
      chart = new Chart(canvasElement, chartConfig);
    }
  });

  $effect(() => {
    chart.data.datasets.forEach((dataset) => {
      dataset.data = $state.snapshot(cpuData);
    });
    chart.update();
  });
</script>

<canvas id="cpu-usage-graph"></canvas>
