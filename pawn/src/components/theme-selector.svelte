<script lang="ts">
  import { Dropdown, Theme } from "carbon-components-svelte";
  // Somewhat cursed import. Unlikely to break, but necessary to avoid a type error on the theme binding.
  import type { CarbonTheme } from "carbon-components-svelte/src/Theme/Theme.svelte";

  let theme: CarbonTheme = "white";
</script>

<Dropdown
  titleText="Theme"
  bind:selectedId={theme}
  type="inline"
  items={[
    { id: "white", text: "Light" },
    { id: "g100", text: "Dark" },
  ]}
/>

<Theme bind:theme persist persistKey="__carbon-theme" />
