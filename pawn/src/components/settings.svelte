<script>
  import { Column, Grid, Row } from "carbon-components-svelte";
  import ResetLocalstorage from "./reset-localstorage.svelte";
  import ThemeSelector from "./theme-selector.svelte";
</script>

<Grid>
  <Row>
    <Column>
      <h2>Customization</h2>
      <ThemeSelector />
    </Column>
  </Row>
  <Row>
    <Column>
      <h2>Developer</h2>
      <ResetLocalstorage />
    </Column>
  </Row>
</Grid>
