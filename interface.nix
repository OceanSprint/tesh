{ lib, config, flake-parts-lib, ... }: {
  options.pyDev = {

    supportedPythons = lib.mkOption {
      description = "Supported Python versions.";
      type = lib.types.listOf lib.types.str;
    };

    extraTestDependencies = lib.mkOption {
      description = "Extra dependencies for tests.";
      type = lib.types.listOf lib.types.str;
    };
  };
}
