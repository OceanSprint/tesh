let
  nixpkgs = builtins.fetchTarball {
    # https://github.com/NixOS/nixpkgs/tree/nixos-23.05 on 2023-07-05
    url = "https://github.com/nixos/nixpkgs/archive/c7a18f89ef1dc423f57f3de9bd5d9355550a5d15.tar.gz";
    sha256 =  "1ggpzw4q52sh4sxmvdvz7q34n7nmdk2nc3ciaipw8zm05mh78dzp";
  };

  pkgs = import nixpkgs { };

in

pkgs.mkShell {
  name = "dev-shell";

  buildInputs = with pkgs; [
      poetry
      python311
      python310
      python39
      gitAndTools.pre-commit

      # test dependency
      nmap
    ];
}
