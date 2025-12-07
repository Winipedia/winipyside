"""Clickable widget module.

This module provides custom Qt widgets
that emit clicked signals for interactive UI elements.
"""

from typing import Any

from PySide6.QtCore import Qt, Signal
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QWidget


class ClickableWidget(QWidget):
    """Regular QWidget that emits a clicked signal on left mouse button press.

    A simple extension of QWidget that makes it interactive by emitting a custom
    clicked signal when the user clicks on it. Useful for creating custom button-like
    areas or interactive widget regions that don't inherit from QPushButton.

    Signals:
        clicked: Emitted when the left mouse button is pressed on the widget.
    """

    clicked = Signal()

    def mousePressEvent(self, event: Any) -> None:  # noqa: N802
        """Handle left mouse button press and emit clicked signal.

        Emits the clicked signal when the left mouse button is pressed on the widget,
        then passes the event to the parent class for standard processing.

        Args:
            event: The QMouseEvent containing button type and position information.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class ClickableVideoWidget(QVideoWidget):
    """Video display widget that emits a clicked signal on left mouse button press.

    Extends QVideoWidget to make video playback areas interactive by emitting a custom
    clicked signal when clicked. Commonly used for play/pause toggling or fullscreen
    mode switching in media player UIs.

    Signals:
        clicked: Emitted when the left mouse button is pressed on the video widget.
    """

    clicked = Signal()

    def mousePressEvent(self, event: Any) -> None:  # noqa: N802
        """Handle left mouse button press on video and emit clicked signal.

        Emits the clicked signal
        when the left mouse button is pressed on the video widget,
        then passes the event to the parent class for standard processing.

        Args:
            event: The QMouseEvent containing button type and position information.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
