from pathlib import Path

import pytest

here = Path(__file__).parent


@pytest.fixture(scope="module")
def repo_root():
    return here.parent


@pytest.fixture(scope="module")
def mozconfigwrapper_sh(repo_root):
    return repo_root / "mozconfigwrapper.sh"


@pytest.fixture
def home(tmp_path):
    return tmp_path / "mozconfigs"


@pytest.fixture
def env(repo_root, home):
    return {
        "BUILDWITH_HOME": str(home),
        "PYTHONPATH": str(repo_root),
    }


