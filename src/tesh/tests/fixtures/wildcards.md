# Use ... to match unimportant parts of expected output

```console tesh-session="foo"
$ echo '{"a":"yes",b:[1,2,3]}'
{"a":"yes",b:[...]}
```
