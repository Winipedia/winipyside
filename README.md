# winipyside

<!-- tooling -->
[![pyrig](https://img.shields.io/badge/built%20with-pyrig-3776AB?logo=buildkite&logoColor=black)](https://github.com/Winipedia/pyrig)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)
<!-- code-quality -->
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)[![mypy](https://img.shields.io/badge/type%20checked-mypy-039dfc.svg)](https://mypy-lang.org/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![pytest](https://img.shields.io/badge/tested%20with-pytest-46a2f1.svg?logo=pytest)](https://pytest.org/)
[![codecov](https://codecov.io/gh/Winipedia/winipyside/branch/main/graph/badge.svg)](https://codecov.io/gh/Winipedia/winipyside)
<!-- package-info -->
[![PyPI](https://img.shields.io/pypi/v/winipyside?logo=pypi&logoColor=white)](https://pypi.org/project/winipyside/)
[![Python](https://img.shields.io/badge/python-3.12|3.13-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/github/license/Winipedia/winipyside)](https://github.com/Winipedia/winipyside/blob/main/LICENSE)
<!-- ci/cd -->
[![CI](https://img.shields.io/github/actions/workflow/status/Winipedia/winipyside/health_check.yaml?label=CI&logo=github)](https://github.com/Winipedia/winipyside/actions/workflows/health_check.yaml)
[![CD](https://img.shields.io/github/actions/workflow/status/Winipedia/winipyside/release.yaml?label=CD&logo=github)](https://github.com/Winipedia/winipyside/actions/workflows/release.yaml)


---

> A utilities package for PySide6

---


## Overview

Winipyside is a production-ready PySide6 utilities package that provides reusable, well-tested components for building Qt desktop applications. It features encrypted file I/O with AES-GCM, a full-featured media player with encrypted video playback support, an embedded web browser with cookie management, toast notifications, and a modular page-based UI framework.

### Key Highlights

- 🔐 **Encrypted File I/O**: Transparent AES-GCM encryption for files and media playback
- 🎬 **Media Player**: Full-featured player with encrypted video support, speed control, and fullscreen mode
- 🌐 **Web Browser**: Embedded browser with cookie management and Qt/Python cookie conversion
- 🔔 **Notifications**: Toast notification system with auto-positioning and smart text truncation
- 🏗️ **UI Framework**: Modular page-based architecture with lifecycle hooks and navigation
- ✅ **Type Safe**: 100% type annotated with strict mypy checking
- 🧪 **Well Tested**: Comprehensive test suite with pytest and pytest-qt
- 🚀 **CI/CD Ready**: Production-ready workflows for headless environments

## Features

### 🔐 Encrypted File I/O

Transparent encryption/decryption for files and media with AES-GCM:

- **Chunked encryption** for efficient streaming (64KB chunks)
- **Random access** support with position mapping
- **Zero-copy decryption** for media playback
- **Authenticated encryption** with nonces and tags

### 🎬 Media Player

Full-featured video player with advanced controls:

- Play/pause, speed control (0.2x-5x), volume slider
- Seekable progress bar with throttled updates
- Fullscreen mode with automatic UI hiding
- **Native encrypted video playback** without temporary files
- Position resumption and smart resource management

### 🌐 Web Browser

Embedded Chromium-based browser:

- Navigation controls (back, forward, address bar)
- Automatic cookie tracking
- QNetworkCookie ↔ http.cookiejar.Cookie conversion
- Domain-based cookie retrieval

### 🏗️ UI Framework

Modular architecture for building complex applications:

- **Lifecycle hooks**: `base_setup()` → `pre_setup()` → `setup()` → `post_setup()`
- **Page-based navigation** with QStackedWidget
- **Dynamic subclass discovery**
- **SVG icon support**
- **Automatic display name generation**

## Installation

### Requirements

- Python 3.12 or 3.13
- PySide6
- System dependencies (Linux only):
  - `libegl1`
  - `libpulse0`

### Install from PyPI

```bash
pip install winipyside
```

### Install from Source

```bash
git clone https://github.com/Winipedia/winipyside.git
cd winipyside
uv sync
```

### Linux System Dependencies

```bash
sudo apt-get update
sudo apt-get install -y libegl1 libpulse0
```

## Quick Start

### Basic Application

```python
from PySide6.QtWidgets import QApplication
from winipyside.src.ui.windows.base.base import Base as BaseWindow
from winipyside.src.ui.pages.browser import Browser

class MyApp(BaseWindow):
    @classmethod
    def get_all_page_classes(cls):
        return [Browser]

    @classmethod
    def get_start_page_cls(cls):
        return Browser

    def pre_setup(self) -> None:
        pass

    def setup(self) -> None:
        self.resize(1280, 720)

    def post_setup(self) -> None:
        pass

if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec()
```

### Encrypted Video Playback

```python
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from PySide6.QtCore import QUrl, QIODevice
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from winipyside.src.core.py_qiodevice import EncryptedPyQFile

# Generate encryption key
key = AESGCM.generate_key(bit_length=256)
aes_gcm = AESGCM(key)

# Play encrypted video
video_path = Path("encrypted_video.mp4")
encrypted_file = EncryptedPyQFile(video_path, aes_gcm)
encrypted_file.open(QIODevice.OpenModeFlag.ReadOnly)

player = QMediaPlayer()
player.setAudioOutput(QAudioOutput())
player.setSourceDevice(encrypted_file, QUrl.fromLocalFile(str(video_path)))
player.play()
```

### Toast Notifications

```python
from winipyside.src.ui.widgets.notification import Notification
from pyqttoast import ToastIcon

Notification(
    title="Success",
    text="Operation completed successfully!",
    icon=ToastIcon.SUCCESS,
    duration=5000
)
```

## Documentation

Comprehensive documentation is available in the [`docs/`](docs/) directory:

- **[Core Package](docs/core.md)** - Encrypted file I/O and QIODevice wrappers
- **[UI Base](docs/ui-base.md)** - Foundation framework and lifecycle management
- **[UI Widgets](docs/ui-widgets.md)** - Reusable widgets (Browser, MediaPlayer, Notifications)
- **[UI Pages](docs/ui-pages.md)** - Page components for navigation
- **[UI Windows](docs/ui-windows.md)** - Main window framework
- **[API Reference](docs/api-reference.md)** - Complete API documentation

## Architecture

```
winipyside/
├── src/
│   ├── core/              # Encrypted file I/O
│   └── ui/
│       ├── base/          # Base classes and lifecycle
│       ├── widgets/       # Reusable widgets
│       ├── pages/         # Page components
│       └── windows/       # Window framework
├── resources/             # SVG icons and static resources
└── dev/
    ├── builders/          # Build utilities
    ├── cli/              # CLI commands
    ├── configs/          # CI/CD configuration
    └── tests/            # Test fixtures
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/Winipedia/winipyside.git
cd winipyside

# Install dependencies with uv
uv sync

# Install pre-commit hooks
uv run pre-commit install

# get familiar with pyrig
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository** and create a feature branch
2. **Write tests** for new functionality
3. **Ensure all tests pass** and code quality checks succeed
4. **Update documentation** as needed
5. **Submit a pull request** with a clear description

### Code Standards

- Follow **Google docstring convention**
- Maintain **100% type coverage**
- Write **comprehensive tests** (aim for >90% coverage)
- Use **descriptive variable names**
- Keep functions **focused and small**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Pyrig](https://github.com/Winipedia/pyrig) - Python project scaffolding framework
- Uses [PySide6](https://www.qt.io/qt-for-python) - Qt for Python
- Toast notifications powered by [pyqttoast](https://github.com/niklashenning/pyqttoast)

## Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/Winipedia/winipyside/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Winipedia/winipyside/discussions)

---
