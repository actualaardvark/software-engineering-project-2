<!-- There's a memory leak in here somewhere -->
<script lang="ts">
  import { onMount } from "svelte";
  import CpuGraph from "./cpu-graph.svelte";
  import { browser } from "$app/environment";
  import RamGraph from "./ram-graph.svelte";
  import { Grid, Row, Column } from "carbon-components-svelte";

  let cpuData: Array<number> = $state(Array(60).fill(0));
  let ramData: Array<number> = $state(Array(60).fill(0));
  onMount(() => {
    if (browser) {
      function connect() {
        const socket = new WebSocket(
          "ws://localhost:3000/api/v1/socket/monitor/global",
        );

        socket.onmessage = async (event) => {
          const utilizationData = JSON.parse(event.data);
          cpuData.push(utilizationData.cpu_usage);
          ramData.push(utilizationData.memory_usage);
          cpuData.shift();
          ramData.shift();
        };
        socket.onclose = () => {
          console.log("Utilization socket reconnecting...");
          setTimeout(() => {
            connect();
          }, 1000);
        };
      }
      connect();
    }
  });
</script>

<CpuGraph {cpuData} />

<RamGraph {ramData} />
