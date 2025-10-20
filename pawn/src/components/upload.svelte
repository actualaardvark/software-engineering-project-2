<script lang="ts">
  import {
    Button,
    ComposedModal,
    FileUploaderDropContainer,
    FileUploaderItem,
    Form,
    FormGroup,
    FormLabel,
    ModalBody,
    ModalFooter,
    ModalHeader,
    ProgressIndicator,
    ProgressStep,
  } from "carbon-components-svelte";
  import RequiredInputWithWarn from "./required-input-with-warn.svelte";
  import { Upload } from "carbon-icons-svelte";

  let uploadFileName = $state("");
  let blockSubmit = $state(true);
  let files: ReadonlyArray<File> = $state([]);
  let modalOpen = $state(false);
  let uploadIncomplete = $state(true);
</script>

<Form on:submit>
  <FormGroup legendText="Submit File">
    <FileUploaderDropContainer
      accept={["ipynb"]}
      multiple={false}
      bind:files
      labelText="Drag and drop a Jupyter Notebook (.ipynb) file here or click to upload"
      on:add={(e) => {}}
    />
    <!-- Loops in svelte are connected to the state, so this will update to reflect the files array when it changes -->
    <!-- Theoretically this could be used to support multiple file uploads in the future -->
    {#each files as file}
      <!-- Yes this uses a self-executing javascript function. I'm not sorry. -->
      <FileUploaderItem
        name={file.name}
        status="edit"
        invalid={(() => {
          if (
            file.name.split(".")[file.name.split(".").length - 1] !== "ipynb"
          ) {
            blockSubmit = true;
            return true;
          }
          blockSubmit = false;
          return false;
        })()}
        on:delete={() => {
          files = [];
          blockSubmit = true;
        }}
      />
    {/each}
  </FormGroup>
  <FormGroup legendText="Identifying Information">
    <RequiredInputWithWarn
      labelText="Student Name"
      placeholder="Enter student name"
    />
    <RequiredInputWithWarn
      labelText="Project Name"
      placeholder="Enter project name"
    />
  </FormGroup>
  <Button
    disabled={blockSubmit}
    icon={Upload}
    type="submit"
    on:click={() => {
      modalOpen = true;
    }}>Submit</Button
  >
  <br />
  {#if blockSubmit}
    <FormLabel>You must attach a valid file to submit</FormLabel>
  {/if}
</Form>

<ComposedModal bind:open={modalOpen}>
  <ModalHeader>Create Job</ModalHeader>
  <ModalBody>
    <ProgressIndicator preventChangeOnClick currentIndex={2}>
      <ProgressStep complete label="Upload File" />
      <ProgressStep complete label="Upload Metadata" />
      <ProgressStep complete label="Add to queue" />
    </ProgressIndicator>
  </ModalBody>
  <ModalFooter
    primaryButtonText="Ok"
    secondaryButtonText="Cancel"
    bind:primaryButtonDisabled={uploadIncomplete}
  />
</ComposedModal>
