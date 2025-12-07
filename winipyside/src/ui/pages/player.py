"""Player page module.

This module contains the player page class for the VideoVault application.
"""

from abc import abstractmethod
from collections.abc import Callable
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from winipyside.src.ui.pages.base.base import Base as BasePage
from winipyside.src.ui.widgets.media_player import MediaPlayer


class Player(BasePage):
    """Media player page for video playback with encryption support.

    A page dedicated to video playback with full media controls
    (play/pause, speed control, volume, progress slider, fullscreen).
    Supports both regular and AES-GCM encrypted video
    files with seamless playback from encrypted sources
    without temporary file extraction.

    The page manages a MediaPlayer widget and provides convenient methods for starting
    playback with optional position resumption.
    """

    @abstractmethod
    def start_playback(self, path: Path, position: int = 0) -> None:
        """Start video playback (to be implemented by subclasses).

        Args:
            path: The file path to start playback for.
            position: The position to start playback from in milliseconds.
        """

    def setup(self) -> None:
        """Initialize the player page with a media player widget.

        Creates a MediaPlayer widget and adds it to the page's layout,
        enabling video playback with full controls.
        """
        self.media_player = MediaPlayer(self.v_layout)

    def play_file_from_func(
        self,
        play_func: Callable[..., Any],
        path: Path,
        position: int = 0,
        **kwargs: Any,
    ) -> None:
        """Play a file using a provided playback function with page navigation.

        A helper method that switches to the player page and invokes the specified
        play function. This pattern allows reusing the same playback logic for
        different file types (regular, encrypted, etc.) via different play functions.

        Args:
            play_func: The playback function to call
                (e.g., play_file or play_encrypted_file).
            path: The file path to play.
            position: The position to start playback from in milliseconds (default 0).
            **kwargs: Additional keyword arguments passed to play_func
                (e.g., aes_gcm for encryption).
        """
        # set current page to player
        self.set_current_page(self.__class__)
        # Stop current playback and clean up resources
        play_func(path=path, position=position, **kwargs)

    def play_file(self, path: Path, position: int = 0) -> None:
        """Play a regular (unencrypted) video file.

        Switches to the player page and starts playback of the specified file.
        Delegates to play_file_from_func with the MediaPlayer's play_file method.

        Args:
            path: The file path to the video file to play.
            position: The position to start playback from in milliseconds (default 0).
        """
        self.play_file_from_func(
            self.media_player.play_file, path=path, position=position
        )

    def play_encrypted_file(
        self, path: Path, aes_gcm: AESGCM, position: int = 0
    ) -> None:
        """Play an AES-GCM encrypted video file with transparent decryption.

        Switches to the player page and starts playback of the encrypted file.
        The file is decrypted on-the-fly during playback without extracting
        temporary files, providing secure playback of protected content.

        Args:
            path: The file path to the encrypted video file to play.
            aes_gcm: The AES-GCM cipher instance initialized with the decryption key.
            position: The position to start playback from in milliseconds (default 0).
        """
        self.play_file_from_func(
            self.media_player.play_encrypted_file,
            path=path,
            position=position,
            aes_gcm=aes_gcm,
        )
