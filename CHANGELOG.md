## Changelog

0.3.0 (2023-XX-XX)
------------------

* ANSI escape code is filtered out to not have to write code blocks with ANSI
  escape sequences, since they are not displayed properly by most of the
  Markdown highligthers, refs #45.
  [garbas]

* Allowing `...` to be used in `PS1` (`tesh-ps1`), refs #45.
  [garbas]

* Running examples in CI, refs #45.
  [garbas]


0.2.0 (2022-12-30)
------------------

* Show the command that failed the assert, refs #29.
  [domenkozar]

* Tell users to use `!!` to rerun the last command.
  [zupo]

* Added `--no-debug` commandline option flag.
  [domenkozar]

* Added `tesh-timeout` and `tesh-timeout-expected` directives, refs #30.
  [domenkozar]


0.1.1 (2022-11-25)
------------------

* Add README to PyPI page.
  [zupo]


0.1.0 (2022-11-25)
------------------

* Initial release.
  [domenkozar, zupo]
