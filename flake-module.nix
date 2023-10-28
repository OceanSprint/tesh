{ inputs, lib, config, self, ... }@top: {
  imports = [
    inputs.pre-commit-hooks-nix.flakeModule
    ./interface.nix
  ];
  perSystem = { config, self', inputs', pkgs, system, lib, ... }:

    let
      autoflake = pkgs.python3Packages.autoflake.overrideAttrs (old: {
        propagatedBuildInputs = old.propagatedBuildInputs ++ [ pkgs.python3Packages.tomli ];
      });

      supportedPythons = top.config.pyDev.supportedPythons;
      forAllPythons = name: f:
        let
          attrNames = (map (py: "${name}${py}") supportedPythons);
          outputs = lib.genAttrs supportedPythons
            (python: f python);
        in
        lib.mapAttrs' (py: value: { name = "${name}${py}"; inherit value; }) outputs;

      poetryArgs = python: {
        projectDir = self;
        preferWheels = true;
        python = pkgs.${python};
      };

      pyproject = lib.importTOML ./pyproject.toml;
      name = pyproject.tool.poetry.name;

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
        (forAllPythons "${name}-" (python:
          inputs.poetry2nix.legacyPackages.${system}.mkPoetryApplication (poetryArgs python)))

        //

        (forAllPythons "testEnv-" (python:
          inputs.poetry2nix.legacyPackages.${system}.mkPoetryEnv (poetryArgs python)));

      checks =
        (forAllPythons "tests-" (python:
          pkgs.runCommand "tests"
            {
              nativeBuildInputs = self'.devShells."${python}".nativeBuildInputs;
            } ''
            cp -r ${self} ./source
            chmod +w -R ./source
            cd ./source
            export PYTHONPATH="$(realpath ./src)"
            make tests skip_lint=true
            cp -r htmlcov $out/
          ''))
          //

        (forAllPythons "ci-" (python:
          pkgs.runCommand "ci" {
            jobs = [
              self'.packages."${name}-${python}"
              self'.packages."testEnv-${python}"
              self'.devShells."${python}"
              self'.checks."tests-${python}"
              self'.checks."pre-commit"
            ];
          } ''touch $out''
        ));

      devShells =
        { default = self'.devShells.python311; }

        //

        (forAllPythons "" (python:
          let
            testEnv = self'.packages."testEnv-${python}";
          in

          pkgs.mkShell
            {
              name = "dev-shell";

              nativeBuildInputs = with pkgs; [
                poetry
                testEnv

                # remove when https://github.com/cachix/pre-commit-hooks.nix/issues/356 is merged
                autoflake
                black
                codespell
                pkgs.python3Packages.flake8
                isort
                yamllint

              ]
              # extra test dependencies
              ++ (map (name: pkgs.${name}) top.config.pyDev.extraTestDependencies);

              inputsFrom = [ config.pre-commit.devShell ];

              shellHook = ''
                tmp_path="$(realpath ./.direnv)"
                mkdir -p "$tmp_path"

                source="$(realpath .)"
                mkdir -p "$tmp_path/python/${testEnv.sitePackages}"

                # Install the package in editable mode
                # This allows executing the project scripts from within the dev-shell using the current
                # version of the code and its dependencies.
                PYTHONPATH="${pkgs."${python}".pkgs.poetry-core}/${testEnv.sitePackages}:${testEnv}/${testEnv.sitePackages}" \
                  ${pkgs."${python}".pkgs.pip}/bin/pip install \
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
}
