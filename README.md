<p align="center">
  <a href="https://circleci.com/gh/OceanSprint/tesh">
    <img alt="CircleCI for tesh (main branch)"
         src="https://circleci.com/gh/OceanSprint/tesh.svg?style=shield">
  </a>
  <img alt="Test coverage (main branch)"
       src="https://img.shields.io/badge/tests_coverage-100%25-brightgreen.svg">
  <img alt="Test coverage (main branch)"
       src="https://img.shields.io/badge/types_coverage-100%25-brightgreen.svg">
  <a href="https://pypi.org/project/tesh/">
    <img alt="latest version of tesh on PyPI"
         src="https://img.shields.io/pypi/v/tesh.svg">
  </a>
  <a href="https://pypi.org/project/tesh/">
    <img alt="Supported Python versions"
         src="https://img.shields.io/pypi/pyversions/tesh.svg">
  </a>
  <a href="https://github.com/OceanSprint/tesh/blob/main/LICENSE">
    <img alt="License: MIT"
         src="https://img.shields.io/badge/License-MIT-yellow.svg">
  </a>
  <a href="https://github.com/OceanSprint/tesh/graphs/contributors">
    <img alt="Built by these great folks!"
         src="https://img.shields.io/github/contributors/OceanSprint/tesh.svg">
  </a>
</p>

# tesh [[tɛʃ]](http://ipa-reader.xyz/?text=t%C9%9B%CA%83&voice=Joanna) - TEstable SHell sessions in Markdown

Showing shell interactions how to run a tool is useful for teaching and explaining.

Making sure that example still works over the years is painfully hard.

Not anymore.

```console
$ tesh demo/
📄 Checking demo/happy.md
  ✨ Running foo  ✅ Passed
  ✨ Running bar  ✅ Passed
📄 Checking demo/sad.md
  ✨ Running foo  ❌ Failed
         Command: echo "foo"

         Expected:
sad panda
         Got:
foo

Taking you into the shell ...

Enter `!!` to rerun the last command.

$
```

## Syntax

To mark a code block as testable, append `tesh-session="NAME"` to the header line.

You can use any syntax highlighting directive, such as `bash`, `shell`, `shell-session`, `console` or others.

~~~
```console tesh-session="hello"
$ echo "Hello World!"
Hello World!
```
~~~

### Linking multiple code blocks into a single shell session

Besides marking a code block as testable, `tesh-session` is a unique identifier that allows for multiple code blocks to share the same session.

~~~
```console tesh-session="multiple_blocks"
$ export NAME=Earth

```
~~~

~~~
```console tesh-session="multiple_blocks"
$ echo "Hello $NAME!"
Hello Earth!
```
~~~

### Ignoring parts of the output

Parts of the inline output can be ignored with `...`:

~~~
```console tesh-session="ignore"
$ echo "Hello from Space!"
Hello ... Space!
```
~~~

The same can be done for multiple lines of output. Note that trailing whitespace in every line is trimmed.

~~~
```console tesh-session="ignore"
$ printf "Hello \nthere \nfrom \nSpace!"
Hello
...
Space!
```
~~~

## Advanced directives

You can set a few other optional directives in the header line:

- `tesh-exitcodes`: a list of exit codes in the order of commands executed inside the code block,
- `tesh-setup`: a filename of a script to run before running the commands in the code block,
- `tesh-ps1`: allow an additional PS1 prompt besides the default `$`,
- `tesh-platform`: specify on which platforms this session block should be tested (`linux`, `darwin`, `windows`),
- `tesh-fixture`: a filename to save the current snippet,
- `tesh-timeout`: number of seconds before a command timeouts (defaults to 30s),
- `tesh-long-running`: set to `true` to showcase long-running commands such as `docker compose up`.

Let's look at all of these through examples!

### Testing exit codes

`tesh-exitcodes` accepts a list of integers, which represent the exit code for every command in the block.

~~~
```console tesh-session="exitcodes" tesh-exitcodes="1 0"
$ false

$ true

```
~~~


### Test setup

Sometimes you need to do some test setup before running the examples in your code blocks. Put those [in a file](./readme.sh) and point to it with the `tesh-setup` directive.

~~~
```console tesh-session="setup" tesh-setup="readme.sh"
$ echo "Hello $NAME!"
Hello Gaea!
```
~~~


### Custom prompts

Every so often you need to drop into a virtualenv or similar shell that changes the prompt. `tesh` supports this via `test-ps1` directive.

~~~
```console tesh-session="prompt" tesh-ps1="(foo) $"
$ PS1="(foo) $ "


(foo) $ echo "hello"
hello
```
~~~

### Only run on certain platforms

Some examples should only run on certain platforms, use `tesh-platform` to declare them as such.

~~~
```console tesh-session="platform" tesh-platform="linux"
$ uname
...Linux...
```
~~~

~~~
```console tesh-session="platform" tesh-platform="darwin"
$ uname
...Darwin...
```
~~~

### Dump file to disk

Occasionally your examples consist of first showing contents of a file, then executing a command that uses said file. This is supported, use the `tesh-fixture` directive.

~~~
```bash tesh-session="fixture" tesh-fixture="foo.sh"
echo "foo"
```
~~~

~~~
```console tesh-session="fixture"
$ chmod +x foo.sh

$ ./foo.sh
foo
```
~~~

### Custom timeout

By default, `tesh` will fail if an example command does not finish in 30 seconds. This number can be modified using the `tesh-timeout` directive.

~~~
```console tesh-session="timeout" tesh-timeout="3"
$ sleep 1

```
~~~


### Long running processes

Some processes that you want to show examples for are long-running processes, like `docker compose up`. They are supported in `tesh` blocks using the `tesh-long-running` directive. Note that they need to be the last command in the block.


~~~
```console tesh-session="long-running" tesh-timeout="1" tesh-long-running="true"
$ nmap 1.1.1.1
Starting Nmap ...
```
~~~

## Installation

The best way to install `tesh` is with your favorite Python package manager.

```bash
$ pip install tesh
```

## Design decisions

- Supports Linux / macOS.
- Not tied to a specific markdown flavor or tooling.
- Renders reasonably well on GitHub.


## Comparison with other tools

| | tesh | [mdsh](https://github.com/zimbatm/mdsh) | [pandoc filters](http://www.chriswarbo.net/projects/activecode/index.html) |
|------------------------------------------|---|---|---|
| Execute shell session                    | ✔️ | ✔️ | ✔️ |
| Modify markdown file with the new output | 🚧[<sub>[1]</sub>](https://github.com/OceanSprint/tesh/issues/6) | ✔️ | ✔️ |
| Shared session between code blocks       | ✔️ | ✖️ | ✖️ |
| Custom PS1 prompts                       | ✔️ | ✖️ | ✖️ |
| Assert non-zero exit codes               | ✔️ | ✖️ | ✖️ |
| Setup the shell environment              | ✔️ | ✖️ | ✖️ |
| Reference fixtures from other snippets   | ✔️ | ✖️ | ✖️ |
| Wildcard matching of the command output  | ✔️ | ✖️ | ✖️ |
| Starts the shell in debugging mode       | ✔️ | ✖️ | ✖️ |
| Specify timeout                          | ✔️ | ✖️ | ✖️ |
| Support long-running commands            | ✔️ | ✖️ | ✖️ |

* ✔️: Supported
* C: Possible but you have to write some code yourself
* 🚧: Under development
* ✖️: Not supported
* ?: I don't know.


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
