{
  description = "A development environment for instagram-to-sqlite";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonPackages = ps: with ps; [
          sqlite-utils
          pytest
          pip
        ];
        python = pkgs.python313.withPackages pythonPackages;
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            python
            pkgs.pre-commit
          ];
        };
      });
}
