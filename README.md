# vscode Opener

## Add Ulauncher as dev dependency

```
ULAUNCHER_PTH=$(python -c 'import site; print(site.getsitepackages()[0])')/ulauncher.pth
realpath Ulauncher > $ULAUNCHER_PTH
```

http://docs.ulauncher.io/en/latest/extensions/debugging.html

# todo:

1. add keyword for re-scan of root folders.
1. Add feedback to user when given rootfolder is incorrect.
1. Add multiple keywords for query
