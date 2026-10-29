"""Override pyrig's ProjectTester to add custom dev dependencies."""

from typing import override

from pyrig.rig.tools.testing.project import ProjectTester as BaseProjectTester


class ProjectTester(BaseProjectTester):
    """Override pyrig's ProjectTester to add custom dev dependencies."""

    @override
    def dev_dependencies(self) -> tuple[str, ...]:
        """Add custom dev dependencies to pyrig's ProjectTester default list."""
        return (*super().dev_dependencies(), "pytest-qt")
