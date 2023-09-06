{
  description = "TEstable SHell sessions in Markdown";

  inputs = {
    nixpkgs.url = "nixpkgs";
    flake-parts.url = "github:hercules-ci/flake-parts";
    dream2nix.url = "github:nix-community/dream2nix";
    dream2nix.inputs.nixpkgs.follows = "nixpkgs";
    dream2nix.inputs.flake-parts.follows = "flake-parts";
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

        packages.default = config.packages.tesh;

        packages.tesh = inputs.dream2nix.lib.evalModules {
          modules = [
            ./dream2nix
            {
              paths.projectRoot = ./.;
              paths.projectRootFile = "flake.nix";
              paths.package = ./dream2nix;
            }
          ];
          packageSets.nixpkgs = pkgs;
        };
      };
    };
}
