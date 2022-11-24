# tesh [tɛʃ] - TEstable SHell sessions in Markdown

Showing shell interactions how to run a tool is useful for teaching and explaining.

Making sure that example still works over the years is painfully hard.

Not anymore.

## Design decisions

- Supports Linux / macOS.
- Not tied to a specific markdown flavor or tooling.
- Renders reasonably well on GitHub.

## Syntax

~~~
```shell-session tesh-session="helloworld" tesh-exitcodes="0 1" tesh-setup="readme.sh" tesh-ps1="#" tesh-os="linux"
$ tesh --version
tesh, version 0.1...

$ tesh --foo
...
Error: No such option: --foo
```
~~~

The first line of the code block allows you to set a few directives:

- ``tesh-session`` marks a block testable. It's a unique identifier that allows for multiple code blocks to share the same session.
- ``tesh-exitcodes`` optional list of exit codes in the order of commands executed inside the code block.
- ``tesh-setup`` optional filename allows you to run a script to setup the environment without showing polluting the Markdown file.
- ``tesh-ps1`` sets additional PS1 prompts that are supported besides ``$``.
- ``tesh-platform`` optional parameter to specify on which platforms should this session block be tested. Examples: linux, darwin, windows
- ``...`` used in a newline is a wildcard matching 0 or more lines
- ``...`` used inside a line is a wildcard matching 0 or more chars


## Usage

```shell-session tesh="readme" tesh-exitcode="1"
$ tesh DIR(S)
Running foobar.md
  Running helloworld
Running baz.md
  Running test1
  Running test2 ... FAILED

    Expected:
      $ git foo
      git: 'bar' is not a git command

    Actual:
      $ git foo
      git: 'foo' is not a git command
```

## Developing `tesh`

You need to have [poetry](https://python-poetry.org/) and Python 3.9 through 3.11 installed on your machine.

Alternatively, if you use [nix](https://nix.dev/tutorials/declarative-and-reproducible-developer-environments), run `nix-shell` to drop into a shell that has everything prepared for development.

Then you can run `make tests` to run all tests & checks. Additional `make` commands are available:

```
# run tesh on all Markdown files
$ make tesh

# run flake8 linters on changed files only
$ make lint

# run flake8 linters on all files
$ make lint all=true

# run mypy type checker
$ make types

# run unit tests
$ make unit

# run a subset of unit tests (regex find)
$ make unit filter=foo

# re-lock Python dependencies (for example after adding or removing one from pyproject.toml)
$ make lock
```


## Comparison with other tools

| | tesh | [mdsh](https://github.com/zimbatm/mdsh) | [pandoc filters](http://www.chriswarbo.net/projects/activecode/index.html) |
|------------------------------------------|---|---|---|
| Execute shell session                    | ✔️ | ✔️ | ✔️ |
| Modify markdown file with the new output | 🚧[<sub>[1]</sub>](https://github.com/OceanSprint/tesh/issues/6) | ✔️ | ✔️ |
| Shared session between code blocks       | ✔️ | ✖️ | ✖️ |
| Custom PS1 prompts                       | ✔️ | ✖️ | ✖️ |
| Assert non-zero exit codes               | ✔️ | ✖️ | ✖️ |
| Setup the shell environment              | ✔️ | ✖️ | ✖️ |
| Wildcard matching of the command output  | ✔️ | ✖️ | ✖️ |


* ✔️: Supported
* C: Possible but you have to write some code yourself
* 🚧: Under development
* ✖️: Not supported
* ?: I don't know.
