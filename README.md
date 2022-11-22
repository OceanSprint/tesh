# tesh - TEstable SHell sessions in README.md files

## Syntax

~~~
 ```shell-session tesh="helloworld" tesh-exitcodes="0 1 0"
$ git --version
git version 2...

$ git foo
git: 'foo' is not a git command

$ git status
On branch master
...
nothing to commit, working tree clean
```
~~~


## Usage

```shell-session tesh="readme" test-exitcode="1"
$ tesh FILE(S)
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


## Prior art

- http://www.chriswarbo.net/projects/activecode/index.html
- https://github.com/zimbatm/mdsh

