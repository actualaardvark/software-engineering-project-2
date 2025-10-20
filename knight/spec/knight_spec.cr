require "./spec_helper"

describe Knight do
  describe "podman_client" do
    it "can create an http client for the active podman socket" do
      Knight.podman_client
    end
  end
  describe "container_ids" do
    it "can get a list of container ids" do
      puts Knight.container_ids
    end
  end
end
