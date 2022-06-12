# vscode Opener

Provide a list of folders (using the Ulauncher settings) and this plugin will look for matches between user input and child folders. If a match, press enter and the folder will automatically be opened in vs code.

## Development.

Below some helper comments to get you started with development.

### Add Ulauncher as dev dependency

```
ULAUNCHER_PTH=$(python -c 'import site; print(site.getsitepackages()[0])')/ulauncher.pth
realpath Ulauncher > $ULAUNCHER_PTH
```

http://docs.ulauncher.io/en/latest/extensions/debugging.html

### todo:

1. add keyword for re-scan of root folders.
1. Add feedback to user when given rootfolder is incorrect.
1. Add multiple keywords for query
