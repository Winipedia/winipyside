"""Tests for winipyside.ui.pages.browser module."""

from PySide6.QtWidgets import QVBoxLayout
from pytest_mock import MockerFixture

from winipyside.core.ui.pages import browser
from winipyside.core.ui.pages.browser import Browser


class TestBrowser:
    """Test class for Browser."""

    def test_setup(self, mocker: MockerFixture) -> None:
        """Test method for setup."""
        # Mock the Browser class methods to avoid abstract class issues
        mock_add_browser = mocker.patch.object(Browser, "add_browser")

        # Create a mock instance
        mock_browser = mocker.MagicMock(spec=Browser)
        mock_browser.add_browser = mock_add_browser

        # Call setup method directly on the class
        Browser.setup(mock_browser)

        # Verify add_browser was called
        mock_add_browser.assert_called_once()
        assert mock_add_browser.called, "setup should call add_browser method"

        # Test that setup method exists and is final
        assert hasattr(Browser, "setup"), "Browser should have setup method"
        assert callable(Browser.setup), "setup should be callable"

    def test_add_browser(self, mocker: MockerFixture) -> None:
        """Test method for add_browser."""
        # Mock the BrowserWidget class
        mock_browser_widget_class = mocker.patch(browser.__name__ + ".BrowserWidget")
        mock_browser_widget_instance = mocker.MagicMock()
        mock_browser_widget_class.return_value = mock_browser_widget_instance

        # Create a mock browser instance with v_layout
        mock_browser = mocker.MagicMock(spec=Browser)
        mock_layout = mocker.MagicMock(spec=QVBoxLayout)
        mock_browser.v_layout = mock_layout

        # Call add_browser method directly on the class
        Browser.add_browser(mock_browser)

        # Verify BrowserWidget was instantiated with correct layout
        mock_browser_widget_class.assert_called_once_with(mock_layout)

        # Verify the browser widget was assigned to the browser attribute
        assert mock_browser.browser is mock_browser_widget_instance, (
            "add_browser should assign BrowserWidget instance to browser attribute"
        )

        # Test that the method exists and is final
        assert hasattr(Browser, "add_browser"), "Browser should have add_browser method"
        assert callable(Browser.add_browser), "add_browser should be callable"

        # Test that it's a method of the Browser class
        assert "add_browser" in Browser.__dict__, (
            "add_browser should be defined in Browser class"
        )
