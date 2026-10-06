import subprocess


def test_trivial() -> None:
    assert True, "Should always pass. If not, then something is really wrong!"


def test_import() -> None:
    """Test if the library is installed properly and can be imported."""
    import rshisttools as _  # noqa: F401


def test_cli() -> None:
    result = subprocess.run(["python", r".\\src\\rshisttools\\", "--help"])
    assert 1 == result.returncode, f"Module __main__ ran with return code {result.returncode}"
