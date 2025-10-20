{pkgs ? (import ./nixpkgs.nix) {}}: {
  default = pkgs.mkShell {
    NIX_CONFIG = "experimental-features = nix-command flakes"; # Enable nix command and flake support.
    nativeBuildInputs = with pkgs; [
      crystalline # Crystal LSP
      shards # Crystal build system and package manager
      crystal_1_15 # Crystal language (v1.15.1)
      sqlite # SQLite database (dependency of SQLite Crystal library)
      bun # Bun Javascript runtime (npm has not been tested)
    ];
  };
}
