"""Override pyrig's ProjectTester to add custom dev dependencies."""

from pyrig.rig.tools.project_tester import ProjectTester as BaseProjectTester


class ProjectTester(BaseProjectTester):
    """Override pyrig's ProjectTester to add custom dev dependencies."""

    def dev_dependencies(self) -> list[str]:
        """Add custom dev dependencies to pyrig's ProjectTester default list."""
        return [*super().dev_dependencies(), "pytest-qt"]
