from brew_updater import BrewUpdater, OutdatedPackage


# ##################################################################
# test parse outdated line formula
# verifies parsing of brew outdated --verbose output for formulae
def test_parse_outdated_line_formula() -> None:
    updater = BrewUpdater()
    result = updater._parse_outdated_line("wget (1.21.3) < 1.21.4", is_cask=False)
    assert result is not None
    assert result.name == "wget"
    assert result.current_version == "1.21.3"
    assert result.latest_version == "1.21.4"
    assert result.is_cask is False


# ##################################################################
# test parse outdated line cask
# verifies parsing of brew outdated --verbose output for casks
def test_parse_outdated_line_cask() -> None:
    updater = BrewUpdater()
    result = updater._parse_outdated_line("visual-studio-code (1.85.0) != 1.86.0", is_cask=True)
    assert result is not None
    assert result.name == "visual-studio-code"
    assert result.current_version == "1.85.0"
    assert result.latest_version == "1.86.0"
    assert result.is_cask is True


# ##################################################################
# test parse outdated line empty
# verifies empty lines return None
def test_parse_outdated_line_empty() -> None:
    updater = BrewUpdater()
    result = updater._parse_outdated_line("", is_cask=False)
    assert result is None


# ##################################################################
# test parse outdated line simple
# verifies parsing when only package name is provided
def test_parse_outdated_line_simple() -> None:
    updater = BrewUpdater()
    result = updater._parse_outdated_line("wget", is_cask=False)
    assert result is not None
    assert result.name == "wget"
    assert result.current_version == ""
    assert result.latest_version == ""


# ##################################################################
# test parse outdated output multiple
# verifies parsing multiple lines of output
def test_parse_outdated_output_multiple() -> None:
    updater = BrewUpdater()
    output = """wget (1.21.3) < 1.21.4
curl (8.4.0) < 8.5.0

git (2.43.0) < 2.44.0"""
    result = updater._parse_outdated_output(output, is_cask=False)
    assert len(result) == 3
    assert result[0].name == "wget"
    assert result[1].name == "curl"
    assert result[2].name == "git"


# ##################################################################
# test get outdated formulae real
# verifies we can actually call brew outdated (integration test)
def test_get_outdated_formulae_real() -> None:
    updater = BrewUpdater()
    # This should not raise - just verify we can call brew
    result = updater._get_outdated_formulae()
    assert isinstance(result, list)
    for pkg in result:
        assert isinstance(pkg, OutdatedPackage)
        assert pkg.is_cask is False


# ##################################################################
# test get outdated casks real
# verifies we can actually call brew outdated for casks (integration test)
def test_get_outdated_casks_real() -> None:
    updater = BrewUpdater()
    result = updater._get_outdated_casks()
    assert isinstance(result, list)
    for pkg in result:
        assert isinstance(pkg, OutdatedPackage)
        assert pkg.is_cask is True


# ##################################################################
# test update brew dry run
# verifies dry run mode does not actually run brew update
def test_update_brew_dry_run() -> None:
    updater = BrewUpdater(dry_run=True)
    result = updater._update_brew()
    assert result is True


# ##################################################################
# test upgrade package dry run
# verifies dry run mode does not actually upgrade packages
def test_upgrade_package_dry_run() -> None:
    updater = BrewUpdater(dry_run=True)
    pkg = OutdatedPackage(name="wget", current_version="1.21.3", latest_version="1.21.4", is_cask=False)
    result = updater._upgrade_package(pkg)
    assert result is True


# ##################################################################
# test run dry run
# verifies full run in dry run mode completes without error
def test_run_dry_run() -> None:
    updater = BrewUpdater(dry_run=True)
    result = updater.run()
    assert result == 0
