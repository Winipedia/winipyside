"""Base UI module.

This module contains the base UI class for the VideoVault application.
"""

from abc import abstractmethod
from types import ModuleType
from typing import TYPE_CHECKING, Any, Self, cast

from pyrig.src.modules.class_ import (
    get_all_nonabstract_subclasses,
)
from pyrig.src.modules.package import get_main_package, walk_package
from pyrig.src.resource import get_resource_path
from pyrig.src.string import split_on_uppercase
from PySide6.QtCore import QObject
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QStackedWidget
from winiutils.src.oop.mixins.meta import ABCLoggingMeta

from winipyside import resources

# Avoid circular import
if TYPE_CHECKING:
    from winipyside.src.ui.pages.base.base import Base as BasePage
    from winipyside.src.ui.windows.base.base import Base as BaseWindow


class QABCLoggingMeta(
    ABCLoggingMeta,
    type(QObject),  # type: ignore[misc]
):
    """Metaclass combining ABC enforcement with Qt and logging integration.

    This metaclass merges ABCLoggingMeta (which enforces abstract methods and logs
    implementation status) with QObject's metaclass. This enables Qt-based UI classes
    to use abstract methods while maintaining proper Qt initialization.
    """


class Base(metaclass=QABCLoggingMeta):
    """Abstract base class for all UI components with lifecycle hooks.

    Defines a common initialization pattern for UI elements with four ordered setup
    phases, enabling predictable initialization flow. All UI components (pages, widgets,
    windows) inherit from this base to ensure consistent lifecycle management.

    Subclasses must implement all abstract methods in the prescribed order:
    base_setup() → pre_setup() → setup() → post_setup()
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the UI component and execute all setup lifecycle hooks.

        Calls setup methods in a fixed order: base_setup(), pre_setup(), setup(),
        and post_setup(). This ensures all UI initialization happens in the correct
        sequence, with dependencies resolved before dependent setup runs.
        """
        super().__init__(*args, **kwargs)
        self.base_setup()
        self.pre_setup()
        self.setup()
        self.post_setup()

    @abstractmethod
    def base_setup(self) -> None:
        """Initialize core Qt objects required by the UI component.

        This is the first lifecycle hook, called before any other setup. Must create
        and configure fundamental Qt widgets/layouts that other setup phases depend on.

        Examples:
            - Creating QWidget or QMainWindow
            - Setting up top-level layouts
            - Initializing core visual structure
        """

    @abstractmethod
    def pre_setup(self) -> None:
        """Execute setup operations before main setup.

        This is the second lifecycle hook. Use this for operations that should run
        after base_setup() but before setup(), such as signal connections that rely
        on base_setup() completing.
        """

    @abstractmethod
    def setup(self) -> None:
        """Execute main UI initialization.

        This is the third lifecycle hook. Contains the primary UI initialization logic,
        such as creating widgets, connecting signals, and populating components.
        """

    @abstractmethod
    def post_setup(self) -> None:
        """Execute finalization operations after main setup.

        This is the fourth and final lifecycle hook. Use this for cleanup, final
        configuration, or operations that should run after setup() is complete,
        such as layout adjustments or state initialization.
        """

    @classmethod
    def get_display_name(cls) -> str:
        """Generate human-readable display name from class name.

        Converts the class name from CamelCase to space-separated words.
        For example: 'BrowserPage' becomes 'Browser Page'.

        Returns:
            The human-readable display name derived from the class name.
        """
        return " ".join(split_on_uppercase(cls.__name__))

    @classmethod
    def get_subclasses(cls, package: ModuleType | None = None) -> list[type[Self]]:
        """Get all non-abstract subclasses of this UI class.

        Dynamically discovers all concrete (non-abstract)
        subclasses within the specified package. Forces module imports to
        ensure all subclasses are loaded and discoverable.
        Returns results sorted by class name for consistent ordering.

        Args:
            package: The package to search for subclasses in. If None, searches
                the main package. Common use is winipyside root package.

        Returns:
            A sorted list of all non-abstract subclass types.
        """
        if package is None:
            # find the main package
            package = get_main_package()

        _ = list(walk_package(package))

        children = get_all_nonabstract_subclasses(cls)
        return sorted(children, key=lambda cls: cls.__name__)

    def set_current_page(self, page_cls: type["BasePage"]) -> None:
        """Switch the currently displayed page in the stacked widget.

        Finds the page instance of the specified type and brings it to the front
        of the stacked widget, making it the visible page.

        Args:
            page_cls: The page class type to display. The corresponding instance
                must already exist in the stack.

        Raises:
            StopIteration: If no page of the specified class exists in the stack.
        """
        self.get_stack().setCurrentWidget(self.get_page(page_cls))

    def get_stack(self) -> QStackedWidget:
        """Get the stacked widget containing all pages.

        Assumes the window object has a 'stack' attribute (QStackedWidget)
        that holds all pages.

        Returns:
            The QStackedWidget managing page navigation.

        Raises:
            AttributeError: If the window doesn't have a 'stack' attribute.
        """
        window = cast("BaseWindow", (getattr(self, "window", lambda: None)()))

        return window.stack

    def get_stack_pages(self) -> list["BasePage"]:
        """Get all page instances from the stacked widget.

        Retrieves all currently instantiated pages in the stacked widget,
        maintaining their widget index order.

        Returns:
            A list of all BasePage instances in the stack.
        """
        # Import here to avoid circular import

        stack = self.get_stack()
        # get all the pages
        return [cast("BasePage", stack.widget(i)) for i in range(stack.count())]

    def get_page[T: "BasePage"](self, page_cls: type[T]) -> T:
        """Get a specific page instance from the stack by class type.

        Finds the single instance of the specified page class in the stack.
        Uses type equality check to handle inheritance correctly.

        Args:
            page_cls: The page class type to retrieve. Uses PEP 695 generic syntax.

        Returns:
            The page instance of the specified class, cast to correct type.

        Raises:
            StopIteration: If no page of the specified class is in the stack.
        """
        page = next(
            page for page in self.get_stack_pages() if page.__class__ is page_cls
        )
        return cast("T", page)

    @classmethod
    def get_svg_icon(cls, svg_name: str, package: ModuleType | None = None) -> QIcon:
        """Load an SVG file and return it as a QIcon.

        Locates SVG files in the resources package and creates Qt icons from them.
        Automatically appends .svg extension if not provided. The SVG is loaded
        from the assets, enabling dynamic icon theming and scaling.

        Args:
            svg_name: The SVG filename (with or without .svg extension).
            package: The package to search for SVG files. If None, uses the default
                resources package. Override for custom resource locations.

        Returns:
            A QIcon created from the SVG file, ready for use in UI widgets.

        Raises:
            FileNotFoundError: If the SVG file is not found in the resources.
        """
        if package is None:
            package = resources
        if not svg_name.endswith(".svg"):
            svg_name = f"{svg_name}.svg"

        return QIcon(str(get_resource_path(svg_name, package=package)))

    @classmethod
    def get_page_static[T: "BasePage"](cls, page_cls: type[T]) -> T:
        """Get a page instance directly from the main application window.

        This static method provides a global way to access any page without needing
        a reference to the window. Searches through top-level widgets to find the
        BaseWindow instance, then retrieves the desired page from it.

        Useful for accessing pages from deep within nested widget hierarchies where
        passing window references would be impractical.

        Args:
            page_cls: The page class type to retrieve. Uses PEP 695 generic syntax.

        Returns:
            The page instance of the specified class from the main window.

        Raises:
            StopIteration: If no BaseWindow is found or if the page doesn't exist.
        """
        from winipyside.src.ui.windows.base.base import (  # noqa: PLC0415  bc of circular import
            Base as BaseWindow,
        )

        top_level_widgets = QApplication.topLevelWidgets()
        main_window = next(
            widget for widget in top_level_widgets if isinstance(widget, BaseWindow)
        )
        return main_window.get_page(page_cls)
