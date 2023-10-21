{
  description = "TEstable SHell sessions in Markdown";

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
      imports = [
        inputs.pre-commit-hooks-nix.flakeModule
      ];
      systems = [ "x86_64-linux" "aarch64-darwin" ];
      perSystem = { config, self', inputs', pkgs, system, lib, ... }:

        let
          autoflake = pkgs.python3Packages.autoflake.overrideAttrs (old: {
            propagatedBuildInputs = old.propagatedBuildInputs ++ [ pkgs.python3Packages.tomli ];
          });

          supportedPythons = [ "python39" "python310" "python311" ];
          forAllPythons = name: f:
            let
              attrNames = (map (py: "${name}-${py}") supportedPythons);
              outputs = lib.genAttrs supportedPythons
                (python: f python);
            in
            lib.mapAttrs' (py: value: { name = "${name}-${py}"; inherit value; }) outputs;
        in
        {
          # Per-system attributes can be defined here. The self' and inputs'
          # module parameters provide easy access to attributes of the same
          # system.

          formatter = pkgs.nixpkgs-fmt;

          pre-commit.settings.hooks.black.enable = true;
          pre-commit.settings.hooks.isort.enable = true;
          pre-commit.settings.hooks.yamllint.enable = true;
          pre-commit.settings.hooks.autoflake.enable = true;
          pre-commit.settings.hooks.flake8.enable = true;

          pre-commit.settings.settings.autoflake.binPath = "${autoflake}/bin/autoflake";
          pre-commit.settings.hooks.check-merge-conflict = {
            enable = true;

            name = "check-merge-conflict";
            description = "Check for files that contain merge conflict strings.";
            entry = "${pkgs.python3Packages.pre-commit-hooks}/bin/check-merge-conflict";
            types = [ "text" ];
          };

          pre-commit.settings.hooks.end-of-file-fixer = {
            enable = true;

            name = "end-of-file-fixer";
            description = "Ensures that a file is either empty, or ends with one newline.";
            entry = "${pkgs.python3Packages.pre-commit-hooks}/bin/end-of-file-fixer";
            types = [ "text" ];
          };

          pre-commit.settings.hooks.trailing-whitespace = {
            enable = true;

            name = "trailing-whitespace";
            description = "This hook trims trailing whitespace.";
            entry = "${pkgs.python3Packages.pre-commit-hooks}/bin/trailing-whitespace-fixer";
            types = [ "text" ];
          };

          pre-commit.settings.hooks.codespell = {
            enable = true;

            name = "codespell";
            description = "Checks for common misspellings in text files.";
            entry = "${pkgs.codespell}/bin/codespell --ignore-words .aspell.en.pws";
            types = [ "text" ];
          };

          packages =
            (forAllPythons "default" (python:
              inputs.poetry2nix.legacyPackages.${system}.mkPoetryApplication {
                projectDir = ./.;
                preferWheels = true;
                python = pkgs.${python};
              }))

            //

            (forAllPythons "testEnv" (python:
              inputs.poetry2nix.legacyPackages.${system}.mkPoetryEnv {
                projectDir = ./.;
                preferWheels = true;
                python = pkgs.${python};
              }))

            //

            (forAllPythons "impure-check" (python:
              pkgs.writeScriptBin "impure-check" ''
                # run the impure-check in a temp dir that gets nuked
                # if this script fails in any way
                export TMPDIR=$(${pkgs.coreutils}/bin/mktemp -d)
                trap "${pkgs.coreutils}/bin/chmod -R +w '$TMPDIR'; ${pkgs.coreutils}/bin/rm -rf '$TMPDIR'" EXIT

                export PATH="${lib.makeBinPath [
                  pkgs.coreutils
                  pkgs.gnumake
                  pkgs.bash
                  pkgs.nix
                  pkgs.which
                  self'.packages."default-${python}"
                ]}"

                cd $TMPDIR
                cp -r ${./.}/* ./
                make examples
              ''
            ));

          # 'make lint' not needed since pre-commit is run by pre-commit flake-part
          # 'make examples' is an impure test so it's done in `impure-check`
          checks =
            (forAllPythons "tests" (python:
              pkgs.runCommand "tests"
                {
                  buildInputs = self'.devShells."default-${python}".buildInputs;
                } ''
                cp -r ${./.} ./source
                chmod +w -R ./source
                cd ./source
                export PYTHONPATH="$(realpath ./src)"
                make types
                make unit
                make tesh
                cp -r htmlcov $out/
              ''));

          devShells =
            {default=self'.devShells.default-python311;}

            //

            (forAllPythons "default" (python:
              let
                testEnv = self'.packages."testEnv-${python}";
              in

              pkgs.mkShell
              {
                name = "dev-shell";

                buildInputs = with pkgs; [
                  poetry
                  self'.packages."testEnv-${python}"

                  # test dependency
                  nmap
                ];

                inputsFrom = [ config.pre-commit.devShell ];

                shellHook = ''
                  tmp_path=$(realpath ./.direnv)

                  source=$(realpath .)
                  mkdir -p "$tmp_path/python/${testEnv.sitePackages}"

                  # Install the package in editable mode
                  # This allows executing `clan` from within the dev-shell using the current
                  # version of the code and its dependencies.
                  PYTHONPATH=${pkgs."python${lib.replaceStrings ["python"] [""] python}Packages".poetry-core}/${testEnv.sitePackages}:${testEnv}/${testEnv.sitePackages} ${pkgs."python${lib.replaceStrings ["python"] [""] python}Packages".pip}/bin/pip install \
                    --no-deps \
                    --disable-pip-version-check \
                    --no-index \
                    --no-build-isolation \
                    --prefix "$tmp_path/python" \
                    --editable $source

                  export PATH="$tmp_path/python/bin:$PATH"
                  export PYTHONPATH="$source/src:$tmp_path/python/${testEnv.sitePackages}:${testEnv}/${testEnv.sitePackages}"
                '';

            }));
        };
    };
}
