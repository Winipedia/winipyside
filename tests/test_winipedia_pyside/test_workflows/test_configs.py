"""module."""

from winipedia_utils.testing.assertions import assert_with_msg

from winipedia_pyside.workflows.configs import HealthCheckWorkflow


class TestPySide6WorkflowMixin:
    """Test class for PySide6WorkflowMixin."""

    def test_get_pre_commit_step(self) -> None:
        """Test method for get_pre_commit_step."""
        step = HealthCheckWorkflow.get_pre_commit_step()
        assert_with_msg("env" in step, "Step should have env vars")
        assert_with_msg(
            step["env"]["QT_QPA_PLATFORM"] == "offscreen",
            "QT_QPA_PLATFORM should be offscreen",
        )
        assert_with_msg(
            step["env"]["QTWEBENGINE_DISABLE_SANDBOX"] == "1",
            "QTWEBENGINE_DISABLE_SANDBOX should be 1",
        )

    def test_get_poetry_setup_steps(self) -> None:
        """Test method for get_poetry_setup_steps."""
        steps = HealthCheckWorkflow.get_poetry_setup_steps()
        assert_with_msg(isinstance(steps, list), "Steps should be a list")
        assert_with_msg(
            any(
                "PySide6 System Dependencies" in step.get("name", "") for step in steps
            ),
            "Steps should include PySide6 System Dependencies",
        )


class TestHealthCheckWorkflow:
    """Test class for HealthCheckWorkflow."""


class TestReleaseWorkflow:
    """Test class for ReleaseWorkflow."""
