"""Browser page module.

This module contains the Browser page class
for displaying web content within the application.
"""

from winipyside.src.ui.pages.base.base import Base as BasePage
from winipyside.src.ui.widgets.browser import Browser as BrowserWidget


class Browser(BasePage):
    """Web browser page for embedded internet browsing.

    A page that provides full web browsing capabilities
    through an embedded Chromium-based browser.
    Includes navigation controls (back/forward/address bar) and automatic cookie
    tracking for web interactions.
    """

    def setup(self) -> None:
        """Initialize the browser page with a web browser widget.

        Creates and configures the BrowserWidget for web browsing and adds it to
        the page's layout. The browser provides full navigation capabilities.
        """
        self.add_brwoser()

    def add_brwoser(self) -> None:
        """Create and add a web browser widget to the page.

        Creates a BrowserWidget instance and adds it to the vertical layout,
        making the embedded browser available for web navigation. The browser
        automatically handles cookies and provides standard navigation controls.

        Note: Method name has a typo (brwoser) but kept for backward compatibility.
        """
        self.browser = BrowserWidget(self.v_layout)
