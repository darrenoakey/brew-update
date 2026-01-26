import subprocess
import sys
from dataclasses import dataclass

from colorama import Fore, Style


# ##################################################################
# outdated package
# represents a homebrew package that has a newer version available
@dataclass
class OutdatedPackage:
    name: str
    current_version: str
    latest_version: str
    is_cask: bool


# ##################################################################
# brew updater
# handles updating homebrew itself and all installed packages
class BrewUpdater:

    # ##################################################################
    # init
    # initialize the updater with optional dry run mode
    def __init__(self, dry_run: bool = False) -> None:
        self.dry_run = dry_run

    # ##################################################################
    # run
    # main entry point - updates brew then all outdated packages
    def run(self) -> int:
        self._print_header("Updating Homebrew")
        if not self._update_brew():
            return 1

        self._print_header("Checking for outdated formulae")
        formulae = self._get_outdated_formulae()
        self._print_outdated(formulae, "formulae")

        self._print_header("Checking for outdated casks")
        casks = self._get_outdated_casks()
        self._print_outdated(casks, "casks")

        all_outdated = formulae + casks
        if not all_outdated:
            self._print_success("Everything is up to date!")
            return 0

        self._print_header(f"Upgrading {len(all_outdated)} package(s)")
        failed = self._upgrade_packages(all_outdated)

        if failed:
            self._print_error(f"Failed to upgrade: {', '.join(failed)}")
            return 1

        self._print_success("All packages upgraded successfully!")
        return 0

    # ##################################################################
    # update brew
    # runs brew update to fetch latest package definitions
    def _update_brew(self) -> bool:
        if self.dry_run:
            self._print_info("[DRY RUN] Would run: brew update")
            return True
        result = subprocess.run(["brew", "update"], capture_output=True, text=True)
        if result.returncode != 0:
            self._print_error(f"brew update failed: {result.stderr}")
            return False
        print(result.stdout)
        return True

    # ##################################################################
    # get outdated formulae
    # returns list of outdated homebrew formulae
    def _get_outdated_formulae(self) -> list[OutdatedPackage]:
        result = subprocess.run(
            ["brew", "outdated", "--formula", "--verbose"],
            capture_output=True,
            text=True
        )
        return self._parse_outdated_output(result.stdout, is_cask=False)

    # ##################################################################
    # get outdated casks
    # returns list of outdated homebrew casks
    def _get_outdated_casks(self) -> list[OutdatedPackage]:
        result = subprocess.run(
            ["brew", "outdated", "--cask", "--verbose"],
            capture_output=True,
            text=True
        )
        return self._parse_outdated_output(result.stdout, is_cask=True)

    # ##################################################################
    # parse outdated output
    # parses brew outdated --verbose output into structured data
    def _parse_outdated_output(self, output: str, is_cask: bool) -> list[OutdatedPackage]:
        packages = []
        for line in output.strip().split("\n"):
            if not line.strip():
                continue
            parsed = self._parse_outdated_line(line, is_cask)
            if parsed:
                packages.append(parsed)
        return packages

    # ##################################################################
    # parse outdated line
    # parses a single line from brew outdated --verbose output
    # format: "name (current_version) < latest_version" or "name (current_version) != latest_version"
    def _parse_outdated_line(self, line: str, is_cask: bool) -> OutdatedPackage | None:
        line = line.strip()
        if not line:
            return None

        # Handle format: "name (current) < latest" or "name (current) != latest"
        if " < " in line:
            parts = line.split(" < ")
        elif " != " in line:
            parts = line.split(" != ")
        else:
            # Simple format: just package name
            return OutdatedPackage(name=line, current_version="", latest_version="", is_cask=is_cask)

        if len(parts) != 2:
            return None

        name_and_current = parts[0]
        latest_version = parts[1].strip()

        # Extract name and current version from "name (version)"
        if "(" in name_and_current and ")" in name_and_current:
            paren_start = name_and_current.rfind("(")
            name = name_and_current[:paren_start].strip()
            current_version = name_and_current[paren_start + 1:name_and_current.rfind(")")].strip()
        else:
            name = name_and_current.strip()
            current_version = ""

        return OutdatedPackage(
            name=name,
            current_version=current_version,
            latest_version=latest_version,
            is_cask=is_cask
        )

    # ##################################################################
    # upgrade packages
    # upgrades all packages in the list, returns names of failed packages
    def _upgrade_packages(self, packages: list[OutdatedPackage]) -> list[str]:
        failed = []
        for pkg in packages:
            success = self._upgrade_package(pkg)
            if not success:
                failed.append(pkg.name)
        return failed

    # ##################################################################
    # upgrade package
    # upgrades a single package
    def _upgrade_package(self, pkg: OutdatedPackage) -> bool:
        cmd = ["brew", "upgrade"]
        if pkg.is_cask:
            cmd.append("--cask")
        cmd.append(pkg.name)

        version_info = ""
        if pkg.current_version and pkg.latest_version:
            version_info = f" ({pkg.current_version} -> {pkg.latest_version})"

        if self.dry_run:
            self._print_info(f"[DRY RUN] Would upgrade: {pkg.name}{version_info}")
            return True

        self._print_info(f"Upgrading {pkg.name}{version_info}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            self._print_error(f"Failed to upgrade {pkg.name}: {result.stderr}")
            return False
        return True

    # ##################################################################
    # print outdated
    # prints list of outdated packages
    def _print_outdated(self, packages: list[OutdatedPackage], package_type: str) -> None:
        if not packages:
            print(f"  No outdated {package_type}")
            return
        print(f"  Found {len(packages)} outdated {package_type}:")
        for pkg in packages:
            version_info = ""
            if pkg.current_version and pkg.latest_version:
                version_info = f" ({pkg.current_version} -> {pkg.latest_version})"
            print(f"    - {pkg.name}{version_info}")

    # ##################################################################
    # print header
    # prints a cyan header
    def _print_header(self, text: str) -> None:
        print(f"\n{Fore.CYAN}==> {text}{Style.RESET_ALL}")

    # ##################################################################
    # print success
    # prints a green success message
    def _print_success(self, text: str) -> None:
        print(f"{Fore.GREEN}{text}{Style.RESET_ALL}")

    # ##################################################################
    # print error
    # prints a red error message
    def _print_error(self, text: str) -> None:
        print(f"{Fore.RED}{text}{Style.RESET_ALL}", file=sys.stderr)

    # ##################################################################
    # print info
    # prints an info message
    def _print_info(self, text: str) -> None:
        print(f"  {text}")
