<script lang="ts">
  import { TextInput } from "carbon-components-svelte";
  // TODO: Make the other props do something.
  let { labelText, placeholder, ...props } = $props();
  let blankWarn = $state(true);
</script>

<TextInput
  required
  bind:labelText
  inline
  bind:placeholder
  bind:warn={blankWarn}
  on:input={(e) => {
    // TODO: Fix this type error.
    // It's not even true, ClipboardEvent absolutely has a detail property.
    // Nevermind, it vanished. If it comes back it's a liar and should be treated as such.
    if (e.detail === "") {
      blankWarn = true;
    } else {
      blankWarn = false;
    }
  }}
  warnText="This field is required"
/>
