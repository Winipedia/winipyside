"""Configs for pyrig.

All subclasses of ConfigFile in the configs package are automatically called.
"""

from typing import Any

from pyrig.rig.configs.base.workflow import (
    WorkflowConfigFile as PyrigWorkflowConfigFile,
)
from pyrig.rig.configs.remote_version_control.workflows.build import (
    BuildWorkflowConfigFile as PyrigBuildWorkflowConfigFile,
)
from pyrig.rig.configs.remote_version_control.workflows.health_check import (
    HealthCheckWorkflowConfigFile as PyrigHealthCheckWorkflowConfigFile,
)
from pyrig.rig.configs.remote_version_control.workflows.release import (
    ReleaseWorkflowConfigFile as PyrigReleaseWorkflowConfigFile,
)


class PySideWorkflowConfigFileMixin(PyrigWorkflowConfigFile):
    """Mixin to add PySide6-specific workflow steps.

    This mixin provides common overrides for PySide6 workflows to work on
    GitHub Actions headless Linux environments.
    """

    def step_run_tests(
        self,
        *,
        step: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Get the pre-commit step.

        We need to add some env vars
        so QtWebEngine doesn't try to use GPU acceleration etc.
        """
        step = super().step_run_tests(step=step)
        step.setdefault("env", {}).update(
            {
                "QT_QPA_PLATFORM": "offscreen",
                "QTWEBENGINE_DISABLE_SANDBOX": "1",
                "QTWEBENGINE_CHROMIUM_FLAGS": "--no-sandbox --disable-gpu --disable-software-rasterizer --disable-dev-shm-usage",  # noqa: E501
            }
        )
        return step

    def steps_core_installed_setup(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Get the core installed setup steps.

        We need to install additional system dependencies for pyside6.
        """
        steps = super().steps_core_installed_setup(
            *args,
            **kwargs,
        )

        steps.append(
            self.step_install_pyside_system_dependencies(),
        )
        return steps

    def step_install_pyside_system_dependencies(self) -> dict[str, Any]:
        """Get the step to install PySide6 dependencies."""
        return self.step(
            step_func=self.step_install_pyside_system_dependencies,
            run="sudo apt-get update && sudo apt-get install -y libegl1 libpulse0",
            if_condition="runner.os == 'Linux'",
        )


class HealthCheckWorkflowConfigFile(
    PySideWorkflowConfigFileMixin, PyrigHealthCheckWorkflowConfigFile
):
    """Health check workflow.

    Extends winiutils health check workflow to add additional steps.
    This is necessary to make pyside6 work on github actions which is a headless linux
    environment.
    """


class BuildWorkflowConfigFile(
    PySideWorkflowConfigFileMixin, PyrigBuildWorkflowConfigFile
):
    """Build workflow.

    Extends winiutils build workflow to add additional steps.
    This is necessary to make pyside6 work on github actions which is a headless linux
    environment.
    """


class ReleaseWorkflowConfigFile(
    PySideWorkflowConfigFileMixin, PyrigReleaseWorkflowConfigFile
):
    """Release workflow.

    Extends winiutils release workflow to add additional steps.
    This is necessary to make pyside6 work on github actions which is a headless linux
    environment.
    """
