# If you're using exit codes for a session, you must specify them for all commands

```shell-session tesh-session="foo" tesh-exitcodes="1 0"
$ false

$ true

```

```shell-session tesh-session="foo"
$ echo "foo"
foo
```
