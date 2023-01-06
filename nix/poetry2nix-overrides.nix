curr: prev: let
  add-setuptools = curr: old: {
    buildInputs = old.buildInputs ++ [curr.setuptools];
  };
in {
  # missing setuptools
  typecov = prev.typecov.overrideAttrs (add-setuptools curr);
  wmctrl = prev.wmctrl.overrideAttrs (add-setuptools curr);
  pyrepl = prev.pyrepl.overrideAttrs (add-setuptools curr);
  fancycompleter = prev.fancycompleter.overrideAttrs (add-setuptools curr);
  flake8-assertive = prev.flake8-assertive.overrideAttrs (add-setuptools curr);
  flake8-builtins = prev.flake8-builtins.overrideAttrs (add-setuptools curr);
  flake8-deprecated = prev.flake8-deprecated.overrideAttrs (add-setuptools curr);
  flake8-ensure-ascii = prev.flake8-ensure-ascii.overrideAttrs (add-setuptools curr);
  flake8-plone-hasattr = prev.flake8-plone-hasattr.overrideAttrs (add-setuptools curr);
  flake8-tuple = prev.flake8-tuple.overrideAttrs (add-setuptools curr);
  flake8-comprehensions = prev.flake8-comprehensions.overrideAttrs (add-setuptools curr);
  flake8-super-call = prev.flake8-super-call.overrideAttrs (add-setuptools curr);

  # missing setuptools and setuptools-scm
  pdbpp = prev.pdbpp.overrideAttrs (old: {
    buildInputs = old.buildInputs ++ [curr.setuptools curr.setuptools-scm];
  });
}
