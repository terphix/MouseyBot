let
  pkgs = import <nixpkgs> { };

  # Podman setup script
  podmanSetupScript =
    let
      registriesConf = pkgs.writeText "registries.conf" ''
        [registries.search]
        registries = ['docker.io']
        [registries.block]
        registries = []
      '';
    in
    pkgs.writeScript "podman-setup" ''
      #!${pkgs.runtimeShell}
      # Dont overwrite customised configuration
      if ! test -f ~/.config/containers/policy.json; then
        install -Dm555 ${pkgs.skopeo.src}/default-policy.json ~/.config/containers/policy.json
      fi
      if ! test -f ~/.config/containers/registries.conf; then
        install -Dm555 ${registriesConf} ~/.config/containers/registries.conf
      fi
    '';

  # Provides a fake "docker" binary mapping to podman
  dockerCompat = pkgs.runCommandNoCC "docker-podman-compat" { } ''
    mkdir -p $out/bin
    ln -s ${pkgs.podman}/bin/podman $out/bin/docker
  '';

in
pkgs.mkShell {

  buildInputs = [
    dockerCompat
    pkgs.podman # Docker compat
    pkgs.runc # Container runtime
    pkgs.conmon # Container runtime monitor
    pkgs.skopeo # Interact with container registry
    pkgs.podman-compose # Docker-compose
    pkgs.slirp4netns # User-mode networking for unprivileged namespaces
    pkgs.fuse-overlayfs # CoW for images, much faster than default vfs
  ];

  shellHook = ''
    clear &&
    ${podmanSetupScript} &&
    echo "Welcome to MouseyBot"
  '';
}
