"""Notification widget module.

This module provides a notification toast widget for displaying temporary messages.
"""

from pyqttoast import Toast, ToastIcon, ToastPosition  # type: ignore[import-untyped]
from PySide6.QtWidgets import QApplication
from winiutils.src.data.structures.text.string import value_to_truncated_string

Toast.setPosition(ToastPosition.TOP_MIDDLE)


class Notification(Toast):  # type: ignore[misc]
    """Toast notification widget with automatic text truncation.

    A configurable toast notification that appears in the top-middle of the screen
    and automatically disappears after a set duration. Truncates long title and text
    to fit within half the window width, ensuring notifications don't expand the window
    or look excessively large.

    Signals inherit from the underlying Toast class and fire when the notification
    is shown/hidden.

    Attributes:
        duration: How long the notification stays visible in milliseconds
            (default 10000).
        icon: The icon to display with the notification.
    """

    def __init__(
        self,
        title: str,
        text: str,
        icon: ToastIcon = ToastIcon.INFORMATION,
        duration: int = 10000,
    ) -> None:
        """Initialize and display the notification.

        Creates a toast notification with the given title, text, and icon.
        The notification automatically appears in the top-middle of the active window
        and disappears after the specified duration.

        Args:
            title: The notification title (will be truncated to window width).
            text: The notification body text (will be truncated to window width).
            icon: The ToastIcon to display. Defaults to INFORMATION.
            duration: How long the notification stays visible in milliseconds.
                Defaults to 10000 (10 seconds).
        """
        super().__init__(QApplication.activeWindow())
        self.setDuration(duration)
        self.setIcon(icon)
        self.set_title(title)
        self.set_text(text)

    def set_title(self, title: str) -> None:
        """Set the notification title and truncate if necessary.

        Truncates the title to fit within half the active window width
        before displaying.
        This prevents excessively long titles from making the notification too wide.

        Args:
            title: The title text to set (may be longer than the window).
        """
        title = self.str_to_half_window_width(title)
        self.setTitle(title)

    def set_text(self, text: str) -> None:
        """Set the notification body text and truncate if necessary.

        Truncates the text to fit within half the active window width before displaying.
        This prevents excessively long messages from making the notification too wide.

        Args:
            text: The notification text to set (may be longer than the window).
        """
        text = self.str_to_half_window_width(text)
        self.setText(text)

    def str_to_half_window_width(self, string: str) -> str:
        """Truncate a string to fit within half the active window width.

        Calculates half the width of the currently active window and truncates the
        string to fit within that width. Uses a fallback of 500 pixels if no window
        is active, ensuring the function always returns a reasonable result.

        This prevents notifications from becoming too wide and potentially expanding
        their parent window or becoming unreadable.

        Args:
            string: The string to potentially truncate.

        Returns:
            The string, truncated if necessary to fit within half the window width.
        """
        main_window = QApplication.activeWindow()
        width = main_window.width() / 2 if main_window is not None else 500
        width = int(width)
        return value_to_truncated_string(string, width)
