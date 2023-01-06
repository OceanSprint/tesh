# flake-parts module for the tesh package
{config, lib, pkgs, ...}: {
  packages.tesh = pkgs.poetry2nix.mkPoetryApplication {
    projectDir = ../.;
    # disabling checks because building mypy from source is expensive.
    doCheck = false;
    # currently not needed because doCheck = false
    overrides = [
      pkgs.poetry2nix.defaultPoetryOverrides
      (import ./poetry2nix-overrides.nix)
    ];
  };
}
