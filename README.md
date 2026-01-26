![](banner.jpg)

# brew-update

A command-line tool for updating Homebrew and all installed packages.

## Purpose

brew-update automates the process of keeping your Homebrew installation current by updating Homebrew itself and then upgrading all outdated formulae and casks.

## Installation

1. Clone or download this repository
2. Create a virtual environment and install dependencies:

```bash
cd brew-update
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Optionally, add the `run` script to your PATH or create an alias:

```bash
alias brew-update='/path/to/brew-update/run'
```

## Usage

### Update all packages

```bash
./run update
```

This will:
1. Run `brew update` to fetch the latest package definitions
2. Check for outdated formulae and casks
3. Upgrade each outdated package

### Dry run

Preview what would be updated without making any changes:

```bash
./run update --dry-run
```

## Examples

### Perform a full update

```bash
$ ./run update
Updating Homebrew...
Checking for outdated formulae...
Checking for outdated casks...
Upgrading node (20.10.0 -> 21.5.0)...
Upgrading visual-studio-code (1.85.0 -> 1.85.1)...
Done!
```

### Check what needs updating

```bash
$ ./run update --dry-run
Updating Homebrew...
Checking for outdated formulae...
Checking for outdated casks...
Would upgrade: node (20.10.0 -> 21.5.0)
Would upgrade: visual-studio-code (1.85.0 -> 1.85.1)
Dry run complete. No packages were updated.
```

## Development

Run tests:

```bash
./run test src/brew_updater_test.py
```

Run linter:

```bash
./run lint
```

Run full checks:

```bash
./run check
```