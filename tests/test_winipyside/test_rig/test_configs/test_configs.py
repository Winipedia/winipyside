"""module."""

from winipyside.rig.configs.configs import HealthCheckWorkflow


class TestPySideWorkflowMixin:
    """Test class for PySide6WorkflowMixin."""

    def test_step_run_tests(self) -> None:
        """Test method for step_run_pre_commit_hooks."""
        step = HealthCheckWorkflow.step_run_tests()
        assert "env" in step, "Step should have env vars"
        assert step["env"]["QT_QPA_PLATFORM"] == "offscreen", (
            "QT_QPA_PLATFORM should be offscreen"
        )

    def test_steps_core_installed_setup(self) -> None:
        """Test method for steps_core_matrix_setup."""
        steps = HealthCheckWorkflow.steps_core_installed_setup()
        assert isinstance(steps, list), "Steps should be a list"
        # assert last step is the pyside6 dependencies step
        assert (
            steps[-1] == HealthCheckWorkflow.step_install_pyside_system_dependencies()
        ), "Last step should be pyside6 dependencies step"

    def test_step_install_pyside_system_dependencies(self) -> None:
        """Test method for step_install_pyside_system_dependencies."""
        step = HealthCheckWorkflow.step_install_pyside_system_dependencies()
        assert "run" in step, "Step should have run command"


class TestHealthCheckWorkflow:
    """Test class for HealthCheckWorkflow."""


class TestReleaseWorkflow:
    """Test class for ReleaseWorkflow."""


class TestBuildWorkflow:
    """Test class."""
