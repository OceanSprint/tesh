# tesh [[tɛʃ]](http://ipa-reader.xyz/?text=t%C9%9B%CA%83&voice=Joanna) - TEstable SHell sessions in Markdown

Showing shell interactions how to run a tool is useful for teaching and explaining.

Making sure that example still works over the years is painfully hard.

Not anymore.

## Design decisions

- Supports Linux / macOS.
- Not tied to a specific markdown flavor or tooling.
- Renders reasonably well on GitHub.

## Syntax

To mark a `shell-session` as testable, append `tesh-session="NAME"` to the header line.

~~~
```shell-session tesh-session="hello"
$ echo "Hello World!"
Hello World!
```
~~~

### Linking multiple code blocks into a single shell session

Besides marking a code block as testable, `tesh-session` is a unique identifier that allows for multiple code blocks to share the same session.

~~~
```shell-session tesh-session="multiple_blocks"
$ export NAME=Earth

```
~~~

~~~
```shell-session tesh-session="multiple_blocks"
$ echo "Hello $NAME!"
Hello Earth!
```
~~~

### Ignoring parts of the output

Parts of the inline output can be ignored with `...`:

~~~
```shell-session tesh-session="ignore"
$ echo "Hello from Space!"
Hello ... Space!
```
~~~

The same can be done for multiple lines of output. Note that trailing whitespace in every line is trimmed.

~~~
```shell-session tesh-session="ignore"
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
- `tesh-platform`: specify on which platforms this session block should be tested (`linux`, `darwin`, `windows`).

Let's look at all of these through examples

### Testing exit codes

`tesh-exitcodes` accepts a list of integers, which represent the exit code for every command in the block.

~~~
```shell-session tesh-session="exitcodes" tesh-exitcodes="1 0"
$ false

$ true

```
~~~


### Test setup

Sometimes you need to do some test setup before running the examples in your code blocks. Put those [in a file](./readme.sh) and point to it with the `tesh-setup` directive.

~~~
```shell-session tesh-session="setup" tesh-setup="readme.sh"
$ echo "Hello $NAME!"
Hello Gaea!
```
~~~


### Custom prompts

TODO

~~~
```shell-session tesh-session="prompt" tesh-ps1="foo"
$ echo "foo"
foo
```
~~~

### Only run on certain platforms

TODO

~~~
```shell-session tesh-session="platform" tesh-platform="darwin"
$ echo "foo"
foo
```
~~~


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
