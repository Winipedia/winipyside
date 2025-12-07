"""Media player widget module.

This module contains the MediaPlayer widget class with full playback controls.
"""

import time
from functools import partial
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PySide6.QtCore import Qt, QTimer, QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLayout,
    QMenu,
    QPushButton,
    QSizePolicy,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from winipyside.src.core.py_qiodevice import (
    EncryptedPyQFile,
    PyQFile,
    PyQIODevice,
)
from winipyside.src.ui.base.base import Base as BaseUI
from winipyside.src.ui.widgets.clickable_widget import ClickableVideoWidget


class MediaPlayer(QMediaPlayer):
    """Full-featured video player widget.

    A complete media player implementation
    with UI controls for play/pause, speed selection,
    volume control, progress seeking, and fullscreen mode. Supports both regular and
    AES-GCM encrypted video files with transparent decryption during playback.

    The player automatically manages IO device lifecycle and provides throttled slider
    updates to prevent excessive position changes during scrubbing.

    Attributes:
        video_widget: ClickableVideoWidget displaying the video.
        audio_output: QAudioOutput for volume control.
        progress_slider: QSlider for playback position control.
        volume_slider: QSlider for volume adjustment (0-100).
        playback_button: Play/pause toggle button.
        speed_button: Playback speed selector button.
        fullscreen_button: Fullscreen mode toggle button.
    """

    def __init__(self, parent_layout: QLayout, *args: Any, **kwargs: Any) -> None:
        """Initialize the media player and create its UI.

        Creates the complete player widget with video display and control bars
        (above and below the video) and adds it to the parent layout.

        Args:
            parent_layout: The parent layout to add the complete player widget to.
            *args: Additional positional arguments passed to parent QMediaPlayer.
            **kwargs: Additional keyword arguments passed to parent QMediaPlayer.
        """
        super().__init__(*args, **kwargs)
        self.parent_layout = parent_layout
        self.io_device: PyQIODevice | None = None
        self.make_widget()

    def make_widget(self) -> None:
        """Create the complete media player widget structure.

        Builds the visual hierarchy:
        - QWidget container (media_player_widget)
          - QVBoxLayout
            - Control bar (above) with play, speed, volume, fullscreen buttons
            - ClickableVideoWidget (video display)
            - Control bar (below) with progress slider

        The structure allows for hiding/showing control bars independently.
        """
        self.media_player_widget = QWidget()
        self.media_player_layout = QVBoxLayout(self.media_player_widget)
        self.parent_layout.addWidget(self.media_player_widget)
        self.add_media_controls_above()
        self.make_video_widget()
        self.add_media_controls_below()

    def make_video_widget(self) -> None:
        """Create the video display widget with audio output configuration.

        Creates a ClickableVideoWidget,
            connects its click signal for fullscreen toggling,
        sets it to expand and fill available space, and configures audio output.
        """
        self.video_widget = ClickableVideoWidget()
        self.video_widget.clicked.connect(self.on_video_clicked)
        self.video_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.setVideoOutput(self.video_widget)

        self.audio_output = QAudioOutput()
        self.setAudioOutput(self.audio_output)

        self.media_player_layout.addWidget(self.video_widget)

    def on_video_clicked(self) -> None:
        """Toggle visibility of all media control bars when video is clicked.

        Provides a common media player pattern where clicking the video hides
        controls for a cleaner viewing experience, and clicking again shows them.
        """
        if self.media_controls_widget_above.isVisible():
            self.hide_media_controls()
            return
        self.show_media_controls()

    def show_media_controls(self) -> None:
        """Make both top and bottom control bars visible."""
        self.media_controls_widget_above.show()
        self.media_controls_widget_below.show()

    def hide_media_controls(self) -> None:
        """Make both top and bottom control bars invisible."""
        self.media_controls_widget_above.hide()
        self.media_controls_widget_below.hide()

    def add_media_controls_above(self) -> None:
        """Create the top control bar with organized button sections.

        Creates a horizontal layout divided into left, center, and right sections,
        then populates each with appropriate controls:
        - Left: Speed control
        - Center: Play/pause button
        - Right: Volume control and fullscreen button

        This layout pattern allows flexible positioning of controls.
        """
        # main above widget
        self.media_controls_widget_above = QWidget()
        self.media_controls_layout_above = QHBoxLayout(self.media_controls_widget_above)
        self.media_player_layout.addWidget(self.media_controls_widget_above)
        # left contorls
        self.left_controls_widget = QWidget()
        self.left_controls_layout = QHBoxLayout(self.left_controls_widget)
        self.media_controls_layout_above.addWidget(
            self.left_controls_widget, alignment=Qt.AlignmentFlag.AlignLeft
        )
        # center contorls
        self.center_controls_widget = QWidget()
        self.center_controls_layout = QHBoxLayout(self.center_controls_widget)
        self.media_controls_layout_above.addWidget(
            self.center_controls_widget, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.right_controls_widget = QWidget()
        self.right_controls_layout = QHBoxLayout(self.right_controls_widget)
        self.media_controls_layout_above.addWidget(
            self.right_controls_widget, alignment=Qt.AlignmentFlag.AlignRight
        )

        self.add_speed_control()
        self.add_volume_control()
        self.add_playback_control()
        self.add_fullscreen_control()

    def add_media_controls_below(self) -> None:
        """Create the bottom control bar with the progress slider.

        Creates a horizontal layout for the bottom controls and adds the
        seekable progress slider for playback position control.
        """
        self.media_controls_widget_below = QWidget()
        self.media_controls_layout_below = QHBoxLayout(self.media_controls_widget_below)
        self.media_player_layout.addWidget(self.media_controls_widget_below)
        self.add_progress_control()

    def add_playback_control(self) -> None:
        """Create a play/pause toggle button in the center control area.

        Creates a button with play/pause icons that toggles between playing and
        paused states. The button is placed in the center control section.
        """
        self.play_icon = BaseUI.get_svg_icon("play_icon")
        self.pause_icon = BaseUI.get_svg_icon("pause_icon")
        # Pause symbol: ⏸ (U+23F8)
        self.playback_button = QPushButton()
        self.playback_button.setIcon(self.pause_icon)
        self.playback_button.clicked.connect(self.toggle_playback)

        self.center_controls_layout.addWidget(self.playback_button)

    def toggle_playback(self) -> None:
        """Toggle between play and pause states and update the button icon.

        If currently playing, pauses and shows the play icon. If paused or stopped,
        starts playback and shows the pause icon.
        """
        if self.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.pause()
            self.playback_button.setIcon(self.play_icon)
        else:
            self.play()
            self.playback_button.setIcon(self.pause_icon)

    def add_speed_control(self) -> None:
        """Create a speed selector button with dropdown menu.

        Creates a button showing the current playback speed (default 1.0x) with a
        dropdown menu listing predefined speed options (0.2x to 5x). Placed in the
        left control section.
        """
        self.default_speed = 1
        self.speed_options = [0.2, 0.5, self.default_speed, 1.5, 2, 3, 4, 5]
        self.speed_button = QPushButton(f"{self.default_speed}x")
        self.speed_menu = QMenu(self.speed_button)
        for speed in self.speed_options:
            action = self.speed_menu.addAction(f"{speed}x")
            action.triggered.connect(partial(self.change_speed, speed))

        self.speed_button.setMenu(self.speed_menu)
        self.left_controls_layout.addWidget(self.speed_button)

    def change_speed(self, speed: float) -> None:
        """Set the playback speed multiplier and update the speed button label.

        Args:
            speed: The new playback speed multiplier (e.g., 1.0 for normal, 2.0 for 2x).
        """
        self.setPlaybackRate(speed)
        self.speed_button.setText(f"{speed}x")

    def add_volume_control(self) -> None:
        """Create a horizontal volume slider with 0-100 range.

        Creates a slider for user volume adjustment and connects it to the
        volume change handler. Placed in the left control section.
        """
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.valueChanged.connect(self.on_volume_changed)
        self.left_controls_layout.addWidget(self.volume_slider)

    def on_volume_changed(self, value: int) -> None:
        """Update audio output volume based on slider value.

        Converts the slider value (0-100) to audio volume range (0.0-1.0) and
        applies it to the audio output.

        Args:
            value: The slider value from 0-100.
        """
        volume = value / 100.0  # Convert to 0.0-1.0 range
        self.audio_output.setVolume(volume)

    def add_fullscreen_control(self) -> None:
        """Create a fullscreen toggle button and discover sibling widgets to hide.

        Creates a button with fullscreen/exit-fullscreen icons and discovers which
        other widgets in the window should be hidden when entering fullscreen mode.
        Placed in the right control section.
        """
        self.fullscreen_icon = BaseUI.get_svg_icon("fullscreen_icon")
        self.exit_fullscreen_icon = BaseUI.get_svg_icon("exit_fullscreen_icon")
        self.fullscreen_button = QPushButton()
        self.fullscreen_button.setIcon(self.fullscreen_icon)

        self.parent_widget = self.parent_layout.parentWidget()
        self.other_visible_widgets = [
            w
            for w in set(self.parent_widget.findChildren(QWidget))
            - {
                self.media_player_widget,
                *self.media_player_widget.findChildren(QWidget),
            }
            if w.isVisible() or not (w.isHidden() or w.isVisible())
        ]
        self.fullscreen_button.clicked.connect(self.toggle_fullscreen)

        self.right_controls_layout.addWidget(self.fullscreen_button)

    def toggle_fullscreen(self) -> None:
        """Toggle between fullscreen and windowed mode.

        Switches the window to fullscreen (hiding sibling widgets and controls) or back
        to windowed mode (showing everything). Updates the button icon accordingly.
        """
        # Get the main window
        main_window = self.media_player_widget.window()
        if main_window.isFullScreen():
            for widget in self.other_visible_widgets:
                widget.show()
            # show the window in the previous size
            main_window.showMaximized()
            self.fullscreen_button.setIcon(self.fullscreen_icon)
        else:
            for widget in self.other_visible_widgets:
                widget.hide()
            main_window.showFullScreen()
            self.fullscreen_button.setIcon(self.exit_fullscreen_icon)

    def add_progress_control(self) -> None:
        """Create the seekable progress slider and connect position signals.

        Creates a horizontal slider for playback position and establishes connections
        between the media player's position/duration signals and the slider, with
        throttled updates to prevent excessive updates during scrubbing.
        """
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.media_controls_layout_below.addWidget(self.progress_slider)

        # Connect media player signals to update the progress slider
        self.positionChanged.connect(self.update_slider_position)
        self.durationChanged.connect(self.set_slider_range)

        # Connect slider signals to update video position
        self.last_slider_moved_update = time.time()
        self.slider_moved_update_interval = 0.1
        self.progress_slider.sliderMoved.connect(self.on_slider_moved)
        self.progress_slider.sliderReleased.connect(self.on_slider_released)

    def update_slider_position(self, position: int) -> None:
        """Update the progress slider to reflect current playback position.

        Only updates the slider if the user is not currently dragging it,
        preventing jumpy behavior during manual seeking.

        Args:
            position: The current media position in milliseconds.
        """
        # Only update if not being dragged to prevent jumps during manual sliding
        if not self.progress_slider.isSliderDown():
            self.progress_slider.setValue(position)

    def set_slider_range(self, duration: int) -> None:
        """Set the progress slider range to match media duration.

        Args:
            duration: The total media duration in milliseconds.
        """
        self.progress_slider.setRange(0, duration)

    def on_slider_moved(self, position: int) -> None:
        """Handle slider movement with throttled position updates.

        Implements throttling (minimum 100ms between updates) to prevent excessive
        seeking during fast slider drags, improving performance and reducing
        audio stuttering.

        Args:
            position: The new position from the slider in milliseconds.
        """
        current_time = time.time()
        if (
            current_time - self.last_slider_moved_update
            > self.slider_moved_update_interval
        ):
            self.setPosition(position)
            self.last_slider_moved_update = current_time

    def on_slider_released(self) -> None:
        """Seek to the slider position when the user releases it.

        Ensures the final position is set even if the last move event was throttled.
        """
        self.setPosition(self.progress_slider.value())

    def play_video(
        self,
        io_device: PyQIODevice,
        source_url: QUrl,
        position: int = 0,
    ) -> None:
        """Start playback of a video from the specified IO device.

        Stops any current playback, sets up the new source, and starts playing.
        Uses a timer to delay playback start, preventing freezing when switching
        between videos. Automatically resumes to the specified position once media
        is buffered.

        Args:
            io_device: The PyQIODevice to use as the media source.
            source_url: The QUrl representing the source location for error reporting.
            position: The position to resume playback from in milliseconds (default 0).
        """
        self.stop_and_close_io_device()

        self.resume_func = partial(self.resume_to_position, position=position)
        self.mediaStatusChanged.connect(self.resume_func)

        # SingleShot prevents freezing when starting new video while another is playing
        QTimer.singleShot(
            100,
            partial(
                self.set_source_and_play, io_device=io_device, source_url=source_url
            ),
        )

    def stop_and_close_io_device(self) -> None:
        """Stop playback and close the current IO device.

        Safely closes any previously opened IO device to release resources
        and prevent memory leaks.
        """
        self.stop()
        if self.io_device is not None:
            self.io_device.close()

    def resume_to_position(
        self, status: QMediaPlayer.MediaStatus, position: int
    ) -> None:
        """Seek to the target position once media is buffered and ready.

        Called when media status changes. Once the media reaches BufferedMedia status
        (fully buffered and ready to play), seeks to the specified position and
        disconnects this handler to avoid repeated seeking.

        Args:
            status: The current media status.
            position: The target position to seek to in milliseconds.
        """
        if status == QMediaPlayer.MediaStatus.BufferedMedia:
            self.setPosition(position)
            self.mediaStatusChanged.disconnect(self.resume_func)

    def set_source_and_play(
        self,
        io_device: PyQIODevice,
        source_url: QUrl,
    ) -> None:
        """Set the media source and start playback.

        Called via timer to delay playback start and prevent freezing.
        Configures the IO device as the source and begins playback.

        Args:
            io_device: The PyQIODevice to use as the media source.
            source_url: The QUrl representing the source location.
        """
        self.set_source_device(io_device, source_url)
        self.play()

    def set_source_device(self, io_device: PyQIODevice, source_url: QUrl) -> None:
        """Configure the media source from an IO device.

        Args:
            io_device: The PyQIODevice to use as the media source.
            source_url: The QUrl representing the source location for error reporting.
        """
        self.source_url = source_url
        self.io_device = io_device
        self.setSourceDevice(self.io_device, self.source_url)

    def play_file(self, path: Path, position: int = 0) -> None:
        """Play a regular (unencrypted) video file.

        Opens the file at the given path and starts playback. The file must be
        in a format supported by the system's media engine (MP4, WebM, MKV, etc.).

        Args:
            path: The file path to the video file to play.
            position: The position to start playback from in milliseconds (default 0).
        """
        self.play_video(
            position=position,
            io_device=PyQFile(path),
            source_url=QUrl.fromLocalFile(path),
        )

    def play_encrypted_file(
        self, path: Path, aes_gcm: AESGCM, position: int = 0
    ) -> None:
        """Play an AES-GCM encrypted video file with transparent decryption.

        Opens an encrypted video file and decrypts it on-the-fly during playback.
        No temporary files are created; decryption happens in memory as needed.
        Supports seeking without decrypting the entire file first.

        Args:
            path: The file path to the encrypted video file to play.
            aes_gcm: The AES-GCM cipher instance initialized with the correct key.
            position: The position to start playback from in milliseconds (default 0).
        """
        self.play_video(
            position=position,
            io_device=EncryptedPyQFile(path, aes_gcm),
            source_url=QUrl.fromLocalFile(path),
        )
