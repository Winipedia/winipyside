"""Class-level test fixtures and utilities.

These fixtures in this module are automatically applied to all test classes
through pytest's autouse mechanism. Pyrig automatically adds this module to
pytest_plugins in conftest.py. However you still have decorate the fixture
with @autouse_class_fixture from pyrig.src.testing.fixtures or with pytest's
autouse mechanism @pytest.fixture(scope="class", autouse=True).
"""
