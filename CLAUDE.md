# brew-update

Homebrew update utility following Python skill standards.

## Key Points

- **Global wrapper**: `~/bin/brew-update` calls `./run`
- **venv activation**: Built into `run` script - callers never activate manually
- **Integration tests**: Tests call real `brew` commands - requires Homebrew installed
- **Dry-run mode**: Use `--dry-run` to preview changes without upgrading

## Troubleshooting

- **"App source not there" error**: Cask is registered but app was manually deleted. Fix: `brew reinstall --cask <name>`
