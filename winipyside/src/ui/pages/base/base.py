"""Base page module.

This module contains the base page class for the VideoVault application.
"""

from functools import partial
from typing import TYPE_CHECKING, Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLayout,
    QMenu,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from winipyside.src.ui.base.base import Base as BaseUI

if TYPE_CHECKING:
    from winipyside.src.ui.windows.base.base import Base as BaseWindow


class Base(BaseUI, QWidget):
    """Abstract base class for all pages in the stacked widget navigation system.

    A page is a full-screen view that can be displayed within a QStackedWidget.
    Each page inherits from BaseUI to get the standard lifecycle hooks and provides
    a top navigation bar with a menu dropdown. Pages are responsible for their own
    content layout and child widgets.

    Attributes:
        v_layout: Main vertical layout for the page content.
        h_layout: Horizontal layout for top navigation bar.
        menu_button: Menu button that provides navigation to other pages.
        base_window: Reference to the containing BaseWindow.
    """

    def __init__(self, base_window: "BaseWindow", *args: Any, **kwargs: Any) -> None:
        """Initialize the page with a reference to the base window.

        Args:
            base_window: The parent BaseWindow containing this page's stack.
            *args: Additional positional arguments passed to parent QWidget.
            **kwargs: Additional keyword arguments passed to parent QWidget.
        """
        self.base_window = base_window
        super().__init__(*args, **kwargs)

    def base_setup(self) -> None:
        """Initialize the page structure with vertical and horizontal layouts.

        Creates the main vertical layout for page content, a horizontal layout
        for the top navigation bar, and registers this page with the base window.
        This is the first lifecycle hook and must run before other setup methods.

        The layout structure is:
        - v_layout (QVBoxLayout) - Main page layout
          - h_layout (QHBoxLayout) - Top navigation/menu bar
          - [page content added here by subclasses]
        """
        self.v_layout = QVBoxLayout()
        self.setLayout(self.v_layout)

        # add a horizontal layout for the top row
        self.h_layout = QHBoxLayout()
        self.v_layout.addLayout(self.h_layout)

        self.add_menu_dropdown_button()
        self.base_window.add_page(self)

    def add_menu_dropdown_button(self) -> None:
        """Create and configure the page navigation menu button.

        Creates a dropdown menu button in the top-left corner that lists all available
        pages as menu actions. Clicking an action switches to that page. The menu
        auto-populates with all page subclasses from the window.

        The menu uses SVG icons for a modern appearance and is aligned to the top-left
        of the navigation bar.
        """
        self.menu_button = QPushButton("Menu")
        self.menu_button.setIcon(self.get_svg_icon("menu_icon"))
        self.menu_button.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        self.h_layout.addWidget(
            self.menu_button,
            alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft,
        )
        self.menu_dropdown = QMenu(self.menu_button)
        self.menu_button.setMenu(self.menu_dropdown)

        for page_cls in self.base_window.get_all_page_classes():
            action = self.menu_dropdown.addAction(page_cls.get_display_name())
            action.triggered.connect(partial(self.set_current_page, page_cls))

    def add_to_page_button(
        self, to_page_cls: type["Base"], layout: QLayout
    ) -> QPushButton:
        """Create a navigation button that switches to the specified page.

        Creates a styled button with the target page's display name and connects it
        to automatically navigate to that page when clicked. The button is added to
        the provided layout.

        Args:
            to_page_cls: The page class to navigate to when the button is clicked.
            layout: The layout to add the button to
                (typically h_layout or a child layout).

        Returns:
            The created QPushButton widget (if you need to store or modify it).
        """
        button = QPushButton(to_page_cls.get_display_name())

        # connect to open page on click
        button.clicked.connect(lambda: self.set_current_page(to_page_cls))

        # add to layout
        layout.addWidget(button)

        return button
