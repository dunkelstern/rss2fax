with import <nixpkgs> { };

  mkShell {
    nativeBuildInputs = with pkgs.buildPackages; [
      chromedriver
      poppler_utils
    ];
    shellHook = ''
  	  if [ ! -e .venv ] ; then
	      python -m venv .venv
	      . .venv/bin/activate
        pip install poetry
        poetry install --no-root
        
        deactivate
      fi
	    . .venv/bin/activate
    '';
}
