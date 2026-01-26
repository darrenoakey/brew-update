# brew-update

Updates Homebrew and all outdated packages.

## Usage

```bash
# Update everything
brew-update update

# Dry run (show what would be updated without updating)
brew-update update --dry-run
```

## What it does

1. Runs `brew update` to fetch latest package definitions
2. Checks for outdated formulae (`brew outdated --formula --verbose`)
3. Checks for outdated casks (`brew outdated --cask --verbose`)
4. Upgrades each outdated package

## Development

```bash
# Run tests
./run test src/brew_updater_test.py

# Run linter
./run lint

# Run full checks
./run check
```
