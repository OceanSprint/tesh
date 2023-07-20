# `nix-shell` example

```console tesh-session="nix-shell" tesh-ps1="[nix-shell:~]$"
$ echo $IN_NIX_SHELL
$ export NIX_PATH=nixpkgs=https://github.com/nixos/nixpkgs/archive/c7a18f89ef1dc423f57f3de9bd5d9355550a5d15.tar.gz
$ nix-shell -p hello
...
[nix-shell:~]$ echo $IN_NIX_SHELL
impure
[nix-shell:~]$ which hello
/nix/store/...-hello-.../bin/hello
[nix-shell:~]$ exit
exit
$
```
