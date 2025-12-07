"""Browser widget module.

This module contains the Browser widget class
for embedded web browsing with cookie management.
"""

from collections import defaultdict
from http.cookiejar import Cookie
from typing import Any

from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtNetwork import QNetworkCookie
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLayout,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Browser(QWebEngineView):
    """Chromium-based web browser widget with navigation controls and cookie tracking.

    A self-contained browser widget that extends QWebEngineView
    with a complete UI including
    back/forward buttons, address bar, and go button.
    Automatically tracks and stores cookies
    for each domain, with conversion between Qt and Python cookie formats.

    The browser initializes with Google
    as the home page and provides methods to retrieve
    cookies in both QNetworkCookie and http.cookiejar.Cookie formats.

    Attributes:
        cookies: Dict mapping domain strings to lists of QNetworkCookie objects.
        address_bar: QLineEdit widget showing the current URL.
        back_button: QPushButton for browser back navigation.
        forward_button: QPushButton for browser forward navigation.
        go_button: QPushButton to navigate to the URL in the address bar.
    """

    def __init__(self, parent_layout: QLayout, *args: Any, **kwargs: Any) -> None:
        """Initialize the browser widget and add it to the parent layout.

        Creates the browser UI (address bar, buttons), connects signals for navigation
        and cookie tracking, and loads the default homepage. The browser widget is
        immediately added to the provided layout.

        Args:
            parent_layout: The parent QLayout to add the complete browser widget to.
            *args: Additional positional arguments passed to parent QWebEngineView.
            **kwargs: Additional keyword arguments passed to parent QWebEngineView.
        """
        super().__init__(*args, **kwargs)
        self.parent_layout = parent_layout
        self.make_widget()
        self.connect_signals()
        self.load_first_url()

    def make_address_bar(self) -> None:
        """Create the navigation bar with back, forward, address input, and go button.

        Constructs a horizontal layout containing:
        - Back button (previous page)
        - Forward button (next page)
        - Address input field (URL entry)
        - Go button (navigate to entered URL)

        The address bar updates automatically when pages load and handles Enter key
        presses for quick navigation.
        """
        self.address_bar_layout = QHBoxLayout()

        # Add back button
        self.back_button = QPushButton()
        self.back_button.setIcon(QIcon.fromTheme("go-previous"))
        self.back_button.setToolTip("Go back")
        self.back_button.clicked.connect(self.back)
        self.address_bar_layout.addWidget(self.back_button)

        # Add forward button
        self.forward_button = QPushButton()
        self.forward_button.setIcon(QIcon.fromTheme("go-next"))
        self.forward_button.setToolTip("Go forward")
        self.forward_button.clicked.connect(self.forward)
        self.address_bar_layout.addWidget(self.forward_button)

        # Add address bar
        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("Enter URL...")
        self.address_bar.returnPressed.connect(self.navigate_to_url)
        self.address_bar_layout.addWidget(self.address_bar)

        # Add go button
        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self.navigate_to_url)
        self.address_bar_layout.addWidget(self.go_button)

        self.browser_layout.addLayout(self.address_bar_layout)

    def navigate_to_url(self) -> None:
        """Load the URL currently entered in the address bar.

        Retrieves the text from the address bar and loads it as the browser's
        current URL. Called when the user presses Enter in the address bar or
        clicks the Go button.
        """
        url = self.address_bar.text()
        self.load(QUrl(url))

    def make_widget(self) -> None:
        """Create the complete browser widget and add it to the parent layout.

        Constructs the visual hierarchy:
        - QWidget container (browser_widget)
          - QVBoxLayout
            - Address bar (horizontal layout with buttons and input)
            - QWebEngineView (actual browser)

        Sets appropriate size policies
        and adds the complete widget to the parent layout.
        """
        self.browser_widget = QWidget()
        self.browser_layout = QVBoxLayout(self.browser_widget)
        self.set_size_policy()
        self.make_address_bar()
        self.browser_layout.addWidget(self)
        self.parent_layout.addWidget(self.browser_widget)

    def set_size_policy(self) -> None:
        """Set the browser to expand and fill available space.

        Configures the size policy to expand in both horizontal and vertical directions,
        allowing the browser to grow with the parent widget.
        """
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def connect_signals(self) -> None:
        """Connect browser signals to their corresponding handler methods.

        Establishes connections for:
        - Page load completion (updates address bar with new URL)
        - Cookie addition (tracks new cookies by domain)
        """
        self.connect_load_finished_signal()
        self.connect_on_cookie_added_signal()

    def connect_load_finished_signal(self) -> None:
        """Connect the page load completion signal to the handler.

        Connects QWebEngineView's loadFinished signal to update the address bar
        when a page finishes loading.
        """
        self.loadFinished.connect(self.on_load_finished)

    def on_load_finished(self, _ok: bool) -> None:  # noqa: FBT001
        """Handle page load completion and update the address bar.

        Called when a page finishes loading (successfully or not). Updates the
        address bar to reflect the current URL of the loaded page.

        Args:
            _ok: Boolean indicating successful page
                load (unused, kept for signal compatibility).
        """
        self.update_address_bar(self.url())

    def update_address_bar(self, url: QUrl) -> None:
        """Update the address bar to display the given URL.

        Args:
            url: The QUrl to display in the address bar text field.
        """
        self.address_bar.setText(url.toString())

    def connect_on_cookie_added_signal(self) -> None:
        """Initialize cookie tracking and connect the cookie added signal.

        Creates the cookies dictionary (defaulting empty lists per domain) and
        connects the QWebEngineCookieStore's cookieAdded signal to the handler.
        Call this during initialization to enable automatic cookie tracking.
        """
        self.cookies: dict[str, list[QNetworkCookie]] = defaultdict(list)
        self.page().profile().cookieStore().cookieAdded.connect(self.on_cookie_added)

    def on_cookie_added(self, cookie: Any) -> None:
        """Handle new cookie added to the store and track it by domain.

        Called automatically when a cookie is set during web browsing. Stores the
        cookie in the cookies dictionary using the cookie's domain as the key.

        Args:
            cookie: The QNetworkCookie that was added to the cookie store.
        """
        self.cookies[cookie.domain()].append(cookie)

    def load_first_url(self) -> None:
        """Load the default homepage when the browser initializes.

        Loads Google's homepage (https://www.google.com/) as the initial page,
        providing a familiar starting point for users.
        """
        self.load(QUrl("https://www.google.com/"))

    @property
    def http_cookies(self) -> dict[str, list[Cookie]]:
        """Get all tracked cookies converted to http.cookiejar.Cookie format.

        Provides cookies in Python's standard http.cookiejar.Cookie format, suitable
        for use with the requests library, urllib, or other Python HTTP clients.
        This is useful for exporting cookies
        from the browser for external HTTP operations.

        Returns:
            Dictionary mapping domain strings to lists of http.cookiejar.Cookie objects.
        """
        return {
            domain: self.qcookies_to_httpcookies(qcookies)
            for domain, qcookies in self.cookies.items()
        }

    def qcookies_to_httpcookies(self, qcookies: list[QNetworkCookie]) -> list[Cookie]:
        """Convert a list of Qt network cookies to Python http.cookiejar cookies.

        Args:
            qcookies: List of QNetworkCookie objects to convert.

        Returns:
            List of equivalent http.cookiejar.Cookie objects preserving all attributes.
        """
        return [self.qcookie_to_httpcookie(q_cookie) for q_cookie in qcookies]

    def qcookie_to_httpcookie(self, qcookie: QNetworkCookie) -> Cookie:
        """Convert a single Qt network cookie to a Python http.cookiejar cookie.

        Translates between Qt's QNetworkCookie format and Python's http.cookiejar.Cookie
        format, preserving all attributes including name, value, domain, path, security
        flags, expiration, and HTTP-only status.

        Args:
            qcookie: The QNetworkCookie to convert.

        Returns:
            The equivalent http.cookiejar.Cookie object.
        """
        name = bytes(qcookie.name().data()).decode()
        value = bytes(qcookie.value().data()).decode()
        domain = qcookie.domain()
        path = qcookie.path() if qcookie.path() else "/"
        secure = qcookie.isSecure()
        expires = None
        if qcookie.expirationDate().isValid():
            expires = int(qcookie.expirationDate().toSecsSinceEpoch())
        rest = {"HttpOnly": str(qcookie.isHttpOnly())}

        return Cookie(
            version=0,
            name=name,
            value=value,
            port=None,
            port_specified=False,
            domain=domain,
            domain_specified=bool(domain),
            domain_initial_dot=domain.startswith("."),
            path=path,
            path_specified=bool(path),
            secure=secure,
            expires=expires or None,
            discard=False,
            comment=None,
            comment_url=None,
            rest=rest,
            rfc2109=False,
        )

    def get_domain_cookies(self, domain: str) -> list[QNetworkCookie]:
        """Get all tracked cookies for a specific domain in Qt format.

        Args:
            domain: The domain to retrieve cookies for (e.g., 'github.com').

        Returns:
            List of QNetworkCookie objects for the specified domain.
        """
        return self.cookies[domain]

    def get_domain_http_cookies(self, domain: str) -> list[Cookie]:
        """Get all tracked cookies for a specific domain in http.cookiejar format.

        Retrieves domain cookies and converts them to Python's standard http.cookiejar
        format, useful for exporting to requests, urllib, or other HTTP libraries.

        Args:
            domain: The domain to retrieve cookies for (e.g., 'github.com').

        Returns:
            List of http.cookiejar.Cookie objects for the specified domain.
        """
        cookies = self.get_domain_cookies(domain)
        return self.qcookies_to_httpcookies(cookies)
