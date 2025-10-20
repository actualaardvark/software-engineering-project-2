<script>
  import { Button } from "carbon-components-svelte";
  import { Reset } from "carbon-icons-svelte";
</script>

<Button
  kind="danger"
  on:click={() => {
    localStorage.clear();
    window.location.reload();
  }}
>
  <Reset /> Reset localstorage
</Button>
