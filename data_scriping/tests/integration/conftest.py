from pathlib import Path

import pytest


@pytest.fixture
def artefact_base_path():
    return Path("tests/integration/data")
