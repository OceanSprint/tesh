{
  config,
  dream2nix,
  lib,
  ...
}: let
  pyproject = lib.importTOML ../pyproject.toml;
  poetryDeps = lib.attrNames
    (builtins.removeAttrs pyproject.tool.poetry.dependencies ["python"]);

in {
  imports = [
    dream2nix.modules.dream2nix.pip
  ];

  inherit (pyproject.tool.poetry) name version;

  pip = {
    pypiSnapshotDate = "2023-09-05";
    flattenDependencies = true;
    requirementsList = poetryDeps ++ pyproject.build-system.requires;
  };

  paths.lockFile = "${config.deps.stdenv.system}.json";

  mkDerivation = {
    src = ../.;
    buildInputs = [
      config.pip.drvs.poetry-core.public
    ];
  };

  buildPythonPackage = {
    format = "pyproject";
  };
}
