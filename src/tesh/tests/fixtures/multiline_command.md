# Multi-line command with `> ` following the prompt

Note that internally the multiline command is converted into a singleline
command by concatenating all lines and stripping the `> ` and `\` symbols.

```console tesh-session="readme-example"
$ echo "Hello from" \
>   "another" \
>   "line!"
Hello from another line!
```
