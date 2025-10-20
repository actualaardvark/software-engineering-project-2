<script>
  import "carbon-components-svelte/css/all.css";
  import {
    Tabs,
    Tab,
    TabContent,
    FileUploaderDropContainer,
  } from "carbon-components-svelte";
  import Settings from "../components/settings.svelte";
  import Upload from "../components/upload.svelte";
  import SystemMonitor from "../components/system-monitor.svelte";
</script>

<Tabs type="container">
  <Tab label="Upload" />
  <Tab label="Jobs" />
  <Tab label="Settings" />
  <Tab label="System Monitor" />

  <svelte:fragment slot="content">
    <TabContent>
      <Upload />
    </TabContent>
    <TabContent>Jobs</TabContent>
    <TabContent>
      <Settings />
    </TabContent>
    <TabContent>
      <SystemMonitor />
    </TabContent>
  </svelte:fragment>
</Tabs>
