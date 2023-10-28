{
  description = "TEstable SHell sessions in Markdown";

  nixConfig = {
    extra-trusted-public-keys = "oceansprint.cachix.org-1:bVOqLd1Vv4KNn7AhqfggmGwDc6GJybMz1gSL7MNEZKA=";
    extra-substituters = "https://oceansprint.cachix.org";
  };

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-23.05";
    pydev = {
      url = "github:oceansprint/pydev";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ inputs.pydev.flakeModule ];
      systems = [
        "aarch64-darwin"
        "aarch64-linux"
        "x86_64-darwin"
        "x86_64-linux"
      ];
      pydev = {
        supportedPythons = [
          "python39"
          "python310"
          "python311"
        ];
        extraTestDependencies = [
          "nmap"
        ];
      };
    };

}
