require "system/user"
require "http/client"
require "socket"

lib LibC
  fun getuid : UidT
end

module Knight
  VERSION = "0.1.0"

  private PODMAN_NOT_INSTALLED_EXCEPTION_TEXT = "Podman is not installed."

  class UnresolvedRuntimeDependencyException < Exception
  end

  def self.podman_client : HTTP::Client
    current_user = System::User.find_by(id: LibC.getuid.to_s)
    begin
      HTTP::Client.new(UNIXSocket.new "/run/user/#{current_user.id}/podman/podman.sock")
    rescue Socket::ConnectError
      raise UnresolvedRuntimeDependencyException.new(PODMAN_NOT_INSTALLED_EXCEPTION_TEXT)
    end
  end

  def self.container_ids
    podman_client.get("/libpod/containers/list").body
  end
end
