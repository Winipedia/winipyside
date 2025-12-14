"""Configs for pyrig.

All subclasses of ConfigFile in the configs package are automatically called.
"""

from typing import Any

from pyrig.dev.configs.pyproject import (
    PyprojectConfigFile as PyrigPyprojectConfigFile,
)
from pyrig.dev.configs.workflows.base.base import (
    Workflow as PyrigWorkflow,
)
from pyrig.dev.configs.workflows.build import (
    BuildWorkflow as PyrigBuildWorkflow,
)
from pyrig.dev.configs.workflows.health_check import (
    HealthCheckWorkflow as PyrigHealthCheckWorkflow,
)
from pyrig.dev.configs.workflows.release import (
    ReleaseWorkflow as PyrigReleaseWorkflow,
)


class PyprojectConfigFile(PyrigPyprojectConfigFile):
    """Pyproject config file.

    Extends winiutils pyproject config file to add additional config.
    """

    @classmethod
    def get_standard_dev_dependencies(cls) -> list[str]:
        """Get the standard dev dependencies."""
        standard_dev_dependencies = super().get_standard_dev_dependencies()
        standard_dev_dependencies.extend(
            [
                "pytest-qt",
            ]
        )
        return standard_dev_dependencies


class PySideWorkflowMixin(PyrigWorkflow):
    """Mixin to add PySide6-specific workflow steps.

    This mixin provides common overrides for PySide6 workflows to work on
    GitHub Actions headless Linux environments.
    """

    @classmethod
    def step_run_tests(
        cls,
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

    @classmethod
    def steps_core_installed_setup(
        cls,
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
            cls.step_install_pyside_system_dependencies(),
        )
        return steps

    @classmethod
    def step_install_pyside_system_dependencies(cls) -> dict[str, Any]:
        """Get the step to install PySide6 dependencies."""
        return cls.get_step(
            step_func=cls.step_install_pyside_system_dependencies,
            run="sudo apt-get update && sudo apt-get install -y libegl1 libpulse0",
            if_condition="runner.os == 'Linux'",
        )


class HealthCheckWorkflow(PySideWorkflowMixin, PyrigHealthCheckWorkflow):
    """Health check workflow.

    Extends winiutils health check workflow to add additional steps.
    This is necessary to make pyside6 work on github actions which is a headless linux
    environment.
    """


class BuildWorkflow(PySideWorkflowMixin, PyrigBuildWorkflow):
    """Build workflow.

    Extends winiutils build workflow to add additional steps.
    This is necessary to make pyside6 work on github actions which is a headless linux
    environment.
    """


class ReleaseWorkflow(PySideWorkflowMixin, PyrigReleaseWorkflow):
    """Release workflow.

    Extends winiutils release workflow to add additional steps.
    This is necessary to make pyside6 work on github actions which is a headless linux
    environment.
    """
