{
  description = "TEstable SHell sessions in Markdown";

  nixConfig = {
    extra-trusted-public-keys = "oceansprint.cachix.org-1:bVOqLd1Vv4KNn7AhqfggmGwDc6GJybMz1gSL7MNEZKA=";
    extra-substituters = "https://oceansprint.cachix.org";
  };

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-23.05";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    pre-commit-hooks-nix = {
      url = "github:cachix/pre-commit-hooks.nix";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.nixpkgs-stable.follows = "nixpkgs";
    };

  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ ./flake-module.nix ];
      systems = [ "x86_64-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin" ];
      pyDev = {
        supportedPythons = [ "python39" "python310" "python311" ];
        extraTestDependencies = [ "nmap" ];
      };

    };
}
