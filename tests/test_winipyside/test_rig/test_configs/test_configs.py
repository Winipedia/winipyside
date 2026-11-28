"""module."""

from winipyside.rig.configs.configs import (
    HealthCheckWorkflowConfigFile,
)


class TestBuildWorkflowConfigFile:
    """Test class."""


class TestHealthCheckWorkflowConfigFile:
    """Test class for HealthCheckWorkflowConfigFile."""

    def test_step_run_tests(self) -> None:
        """Test method."""
        step = HealthCheckWorkflowConfigFile().step_run_tests()
        assert "env" in step, "Step should have env vars"
        assert step["env"]["QT_QPA_PLATFORM"] == "offscreen", (
            "QT_QPA_PLATFORM should be offscreen"
        )


class TestPySideWorkflowConfigFileMixin:
    """Test class for PySide6WorkflowConfigFileMixin."""

    def test_step_install_pyside_system_dependencies(self) -> None:
        """Test method for step_install_pyside_system_dependencies."""
        step = HealthCheckWorkflowConfigFile().step_install_pyside_system_dependencies()
        assert "run" in step, "Step should have run command"

    def test_steps_core_installed_setup(self) -> None:
        """Test method for steps_core_installed_setup."""
        workflow = HealthCheckWorkflowConfigFile()
        steps = workflow.steps_core_installed_setup()
        assert isinstance(steps, tuple), "Steps should be a tuple"
        assert steps[-1] == workflow.step_install_pyside_system_dependencies, (
            "Last step should be pyside6 dependencies step"
        )


class TestReleaseWorkflowConfigFile:
    """Test class for ReleaseWorkflowConfigFile."""
