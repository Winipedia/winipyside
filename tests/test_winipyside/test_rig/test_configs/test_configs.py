"""module."""

from winipyside.rig.configs.configs import (
    HealthCheckWorkflowConfigFile,
)


class TestPySideWorkflowConfigFileMixin:
    """Test class for PySide6WorkflowConfigFileMixin."""

    def test_step_run_tests(self) -> None:
        """Test method for step_run_pre_commit_hooks."""
        step = HealthCheckWorkflowConfigFile().step_run_tests()
        assert "env" in step, "Step should have env vars"
        assert step["env"]["QT_QPA_PLATFORM"] == "offscreen", (
            "QT_QPA_PLATFORM should be offscreen"
        )

    def test_steps_core_installed_setup(self) -> None:
        """Test method for steps_core_matrix_setup."""
        steps = HealthCheckWorkflowConfigFile().steps_core_installed_setup()
        assert isinstance(steps, list), "Steps should be a list"
        # assert last step is the pyside6 dependencies step
        assert (
            steps[-1]
            == HealthCheckWorkflowConfigFile().step_install_pyside_system_dependencies()
        ), "Last step should be pyside6 dependencies step"

    def test_step_install_pyside_system_dependencies(self) -> None:
        """Test method for step_install_pyside_system_dependencies."""
        step = HealthCheckWorkflowConfigFile().step_install_pyside_system_dependencies()
        assert "run" in step, "Step should have run command"


class TestHealthCheckWorkflowConfigFile:
    """Test class for HealthCheckWorkflowConfigFile."""


class TestReleaseWorkflowConfigFile:
    """Test class for ReleaseWorkflowConfigFile."""


class TestBuildWorkflowConfigFile:
    """Test class."""
