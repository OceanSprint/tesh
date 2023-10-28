## Changelog

0.3.1 (2023-10-28)
------------------

* Fix multiline commands on macOS and NixOS, refs #48, #52.
  [zupo]


0.3.0 (2023-07-28)
------------------

* ANSI escape code is filtered out to not have to write code blocks with ANSI
  escape sequences, since they are not displayed properly by most of the
  Markdown highlighters, refs #45.
  [garbas]

* Allowing `...` to be used in `PS1` (`tesh-ps1`), refs #45.
  [garbas]

* Handle unicode in examples, refs #39.
  [h4l]

* Widen the TTY to avoid truncating commands, refs #42.
  [h4l]

* Allow commands to continue across lines, refs #41.
  [h4l]

* Escape square brackets in fnmatch patterns, refs #38.
  [h4l]

* Respect leading whitespace in example output, refs #43.
  [h4l]


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
