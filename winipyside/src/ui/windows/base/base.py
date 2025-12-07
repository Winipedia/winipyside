"""Base window module.

This module contains the base window class for the VideoVault application.
"""

from abc import abstractmethod

from PySide6.QtWidgets import QMainWindow, QStackedWidget

from winipyside.src.ui.base.base import Base as BaseUI
from winipyside.src.ui.pages.base.base import Base as BasePage


class Base(BaseUI, QMainWindow):
    """Abstract base class for the main application window.

    A QMainWindow-based window that implements the stacked widget navigation pattern.
    Subclasses define which pages are available
    and which page should be shown at startup.
    The window manages a QStackedWidget containing all pages and handles page switching.

    Attributes:
        stack: The QStackedWidget managing all pages.
    """

    @classmethod
    @abstractmethod
    def get_all_page_classes(cls) -> list[type[BasePage]]:
        """Get all page classes to be added to this window.

        Subclasses must return a list of all page classes that should be available
        in the window's stack. These pages will be instantiated during window setup.

        Returns:
            A list of BasePage subclass types to include in the window.
        """

    @classmethod
    @abstractmethod
    def get_start_page_cls(cls) -> type[BasePage]:
        """Get the page class to display when the window first opens.

        Subclasses must return the page class that should be shown initially.
        This page must be one of the classes returned by get_all_page_classes().

        Returns:
            The BasePage subclass type to display at startup.
        """

    def base_setup(self) -> None:
        """Initialize the main window structure with title and stacked pages.

        Sets the window title to the window's display name, creates the stacked widget,
        instantiates all pages, and sets the starting page. This is the first lifecycle
        hook and establishes the complete window structure.
        """
        self.setWindowTitle(self.get_display_name())

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.make_pages()

        self.set_start_page()

    def make_pages(self) -> None:
        """Instantiate all page classes and add them to the stack.

        Iterates through all page classes returned by get_all_page_classes()
        and instantiates each one, which triggers their base_setup() hooks
        and adds them to the stack. Must be called during window initialization.
        """
        for page_cls in self.get_all_page_classes():
            page_cls(base_window=self)

    def set_start_page(self) -> None:
        """Switch to the startup page as returned by get_start_page_cls()."""
        self.set_current_page(self.get_start_page_cls())

    def add_page(self, page: BasePage) -> None:
        """Add a page to the stacked widget.

        Called by page instances during their setup to register themselves with
        the window. Each page is added to the stack widget.

        Args:
            page: The BasePage instance to add to the stack.
        """
        self.stack.addWidget(page)
