{
  description = "TEstable SHell sessions in Markdown";
  inputs.nixpkgs.url = "nixpkgs/nixos-23.05";
  inputs.poetry2nix = {
    url = "github:nix-community/poetry2nix";
    inputs.nixpkgs.follows = "nixpkgs";
  };
  outputs = { self, nixpkgs, poetry2nix }:

    let

      lib = nixpkgs.lib;
      supportedSystems = [ "x86_64-linux" "aarch64-darwin" ];
      forAllSystems = f: lib.genAttrs supportedSystems
        (system: f system (import nixpkgs { inherit system; }));

    in
    {
      formatter = forAllSystems (system: pkgs: pkgs.nixpkgs-fmt);

      packages = forAllSystems (system: pkgs: {
        default = poetry2nix.legacyPackages.${system}.mkPoetryApplication {
          projectDir = self;
          preferWheels = true;
        };

        testEnv = poetry2nix.legacyPackages.${system}.mkPoetryEnv {
          projectDir = self;
          preferWheels = true;
        };
      });

      devShells = forAllSystems (system: pkgs:
        {
          default = pkgs.mkShell {
            name = "dev-shell";

            buildInputs = with pkgs; [
              # poetry
              self.packages.${system}.testEnv
              # python311
              # python310
              # python39
              # gitAndTools.pre-commit

              # test dependency
              # nmap
            ];
          };

        });


      checks = forAllSystems (system: pkgs: {
        lint = pkgs.runCommand "lint"
          {
            buildInputs = self.devShells.${system}.default.buildInputs ++ [ pkgs.git ];
          } ''
          mkdir ./home
          export HOME=$(realpath ./home)
          cp -r ${self} ./source
          chmod +w -R ./source
          cd ./source
          pre-commit run --all-files || cat ../home/.cache/pre-commit/pre-commit.log
        '';
      });

    };
}
