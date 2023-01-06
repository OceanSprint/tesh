{
  description = "TEstable SHell sessions in Markdown";

  inputs = {
    nixpkgs.url = "nixpkgs";
    poetry2nix.url = "poetry2nix";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      flake = {
        # Put your original flake attributes here.
      };
      systems = [
        "x86_64-linux"
      ];
      perSystem = { config, pkgs, ... }: {
        imports = [
          ./nix/tesh.nix
        ];
        packages.default = config.packages.tesh;
      };
    };
}
