# Whitespace handling in tesh code blocks

Leading whitespace in command output is matched

## Code block flush with left margin

```console tesh-session="non-indented-block"
$ # No blank lines after these commands:
$ printf '0 space\n  2 space\n    4 space\n'
0 space
  2 space
    4 space
$ printf '  2 space\n    4 space\n0 space\n'
  2 space
    4 space
0 space
```

## Code block with indent

Leading whitespace is trimmed to the same level as the first line in the block.

(The same example as above, but indented.)

  ```console tesh-session="indented-block"
    $ # No blank lines after these commands:
    $ printf '0 space\n  2 space\n    4 space\n'
    0 space
      2 space
        4 space
    $ printf '  2 space\n    4 space\n0 space\n'
      2 space
        4 space
    0 space
  ```

## Examples can have extra trailing whitespace for readability

```console tesh-session="extra-trailing-whitespace"
$ echo this is the first thing
this is the first thing

$ # This is some commentary on the next thing
$ echo another thing
another thing


$ # More than one blank line is OK too.
```
