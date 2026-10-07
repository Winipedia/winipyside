"""Explicit references for reviewed dead code false positives."""

from PySide6.QtCore import QIODevice

from winipyside.core.core.py_qiodevice import EncryptedPyQFile
from winipyside.core.ui.base.base import Base as UIBase
from winipyside.core.ui.pages.base.base import Base as BasePage
from winipyside.core.ui.pages.browser import Browser as BrowserPage
from winipyside.core.ui.pages.player import Player
from winipyside.core.ui.widgets.browser import Browser
from winipyside.core.ui.widgets.clickable_widget import ClickableWidget
from winipyside.core.ui.widgets.notification import Notification

_BROWSER_OVERRIDES = (
    Browser.get_domain_http_cookies,
    Browser.http_cookies,
)
_QT_OVERRIDES = (
    EncryptedPyQFile.CHUNK_OVERHEAD,
    QIODevice.readLineData,
    QIODevice.skipData,
)
_UI_ATTRIBUTES = (BrowserPage.browser,)  # ty: ignore[unresolved-attribute]
_UI_CLASSES = (
    BrowserPage,
    ClickableWidget,
    Notification,
    Player,
)
_UI_OVERRIDES = (
    BasePage.add_to_page_button,
    Player.start_playback,
    UIBase.get_page_static,
    UIBase.get_subclasses,
)
