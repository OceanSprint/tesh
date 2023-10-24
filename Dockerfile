FROM ubuntu:23.10
RUN apt-get update \
    && apt-get install nano git nix -y \
    && echo "experimental-features = nix-command flakes" >> /etc/nix/nix.conf \
    && echo "max-jobs = 4" >> /etc/nix/nix.conf
COPY ./. /tesh
RUN nix develop /tesh -c true
WORKDIR /tesh
CMD nix develop
