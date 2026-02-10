"""module."""

from winipyside.rig.tools.project_tester import ProjectTester


class TestProjectTester:
    """Test class."""

    def test_get_dev_dependencies(self) -> None:
        """Test method."""
        result = ProjectTester.get_dev_dependencies()
        assert isinstance(result, list), "Dev dependencies should be a list"
        assert "pytest-qt" in result, "Dev dependencies should include pytest-qt"
