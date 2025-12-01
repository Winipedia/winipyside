"""module."""

from pyrig.src.testing.assertions import assert_with_msg

from winipyside.dev.configs.configs import HealthCheckWorkflow, PyprojectConfigFile


class TestPySideWorkflowMixin:
    """Test class for PySide6WorkflowMixin."""

    def test_step_run_tests(self) -> None:
        """Test method for step_run_pre_commit_hooks."""
        step = HealthCheckWorkflow.step_run_tests()
        assert_with_msg("env" in step, "Step should have env vars")
        assert_with_msg(
            step["env"]["QT_QPA_PLATFORM"] == "offscreen",
            "QT_QPA_PLATFORM should be offscreen",
        )

    def test_steps_core_installed_setup(self) -> None:
        """Test method for steps_core_matrix_setup."""
        steps = HealthCheckWorkflow.steps_core_installed_setup()
        assert_with_msg(isinstance(steps, list), "Steps should be a list")
        # assert last step is the pyside6 dependencies step
        assert (
            steps[-1] == HealthCheckWorkflow.step_install_pyside_system_dependencies()
        ), "Last step should be pyside6 dependencies step"

    def test_step_install_pyside_system_dependencies(self) -> None:
        """Test method for step_install_pyside_system_dependencies."""
        step = HealthCheckWorkflow.step_install_pyside_system_dependencies()
        assert_with_msg("run" in step, "Step should have run command")


class TestHealthCheckWorkflow:
    """Test class for HealthCheckWorkflow."""


class TestReleaseWorkflow:
    """Test class for ReleaseWorkflow."""


class TestPyprojectConfigFile:
    """Test class."""

    def test_get_standard_dev_dependencies(self) -> None:
        """Test method."""
        dev_dependencies = PyprojectConfigFile.get_standard_dev_dependencies()

        assert isinstance(dev_dependencies, list), "Dev dependencies should be a dict"

        assert "pytest-qt" in dev_dependencies, (
            "Dev dependencies should include pytest-qt"
        )
