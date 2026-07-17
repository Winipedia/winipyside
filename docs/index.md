# Home

<!-- project-status -->
[![CI](https://img.shields.io/github/actions/workflow/status/Winipedia/winipyside/health_check.yml?label=CI&logo=github)](https://github.com/Winipedia/winipyside/actions/workflows/health_check.yml)
[![CD](https://img.shields.io/github/actions/workflow/status/Winipedia/winipyside/deploy.yml?label=CD&logo=github)](https://github.com/Winipedia/winipyside/actions/workflows/deploy.yml)
[![ProjectTester](https://img.shields.io/badge/coverage->=90%25-hsl(108,80%25,45%25)?logo=codecov&logoColor=white)](https://pytest.org)
<!-- code-quality -->
[![ByteOrderMarkerFormatter](https://img.shields.io/badge/BOM-fix--byte--order--marker-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![CaseConflictChecker](https://img.shields.io/badge/case--conflict-check--case--conflict-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![DependencyAuditor](https://img.shields.io/badge/security-pip--audit-blue?logo=python)](https://github.com/pypa/pip-audit)
[![DependencyChecker](https://img.shields.io/badge/dependencies-deptry-blue)](https://github.com/osprey-oss/deptry)
[![EndOfFileFormatter](https://img.shields.io/badge/EOF-end--of--file--fixer-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![EndOfLineFormatter](https://img.shields.io/badge/EOL-mixed--line--ending-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![JSONFormatter](https://img.shields.io/badge/JSON-pretty--format--json-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![JSONLinter](https://img.shields.io/badge/JSON-check--json-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![LargeFileChecker](https://img.shields.io/badge/large--files-check--added--large--files-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![MarkdownLinter](https://img.shields.io/badge/Markdown-rumdl-darkgreen)](https://github.com/rvben/rumdl)
[![MergeConflictChecker](https://img.shields.io/badge/merge--conflict-check--merge--conflict-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![ModuleTestNamingChecker](https://img.shields.io/badge/test--naming-name--tests--test-blue)](https://github.com/pre-commit/pre-commit-hooks)
[![PythonLinter](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![SecretsChecker](https://img.shields.io/badge/secrets-detect--secrets-blue)](https://github.com/Yelp/detect-secrets)
[![SecurityChecker](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![ShellFormatter](https://img.shields.io/badge/shell-shfmt-orange)](https://github.com/mvdan/sh)
[![ShellLinter](https://img.shields.io/badge/shell-shellcheck-blue)](https://github.com/koalaman/shellcheck)
[![SpellChecker](https://img.shields.io/badge/spell--check-typos-blue)](https://github.com/crate-ci/typos)
[![TOMLLinter](https://img.shields.io/badge/TOML-tombi-blueviolet)](https://github.com/tombi-toml/tombi)
[![TrailingWhitespaceFormatter](https://img.shields.io/badge/whitespace-trailing--whitespace--fixer-orange)](https://github.com/pre-commit/pre-commit-hooks)
[![TypeChecker](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
[![YAMLLinter](https://img.shields.io/badge/YAML-ryl-red)](https://github.com/owenlamont/ryl)
<!-- tooling -->
[![PackageManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Pyrigger](https://img.shields.io/badge/built%20with-pyrig-3776AB?logo=buildkite&logoColor=black)](https://github.com/Winipedia/pyrig)
[![RemoteVersionController](https://img.shields.io/github/stars/Winipedia/winipyside?style=social)](https://github.com/Winipedia/winipyside)
[![VersionControlHookManager](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/j178/prek/master/docs/assets/badge-v0.json)](https://github.com/j178/prek)
[![VersionController](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white)](https://git-scm.com)
<!-- project-info -->
[![DocsBuilder](https://img.shields.io/badge/MkDocs-Documentation-326CE5?logo=mkdocs&logoColor=white)](https://Winipedia.github.io/winipyside)
[![PackageIndex](https://img.shields.io/pypi/v/winipyside?logo=pypi&logoColor=white)](https://pypi.org/project/winipyside)
[![ProgrammingLanguage](https://img.shields.io/pypi/pyversions/winipyside)](https://www.python.org)
[![License](https://img.shields.io/github/license/Winipedia/winipyside)](https://github.com/Winipedia/winipyside/blob/main/LICENSE)

---

> A utilities package for PySide6

---

Welcome to the comprehensive documentation for **Winipyside**,
a PySide6 utilities package for building modern Qt desktop applications.

## Table of Contents

### Core Documentation

- **[Core Package](core.md)** - Encrypted file I/O and QIODevice wrappers
  - PyQIODevice - Python-friendly QIODevice wrapper
  - PyQFile - File operations with Path support
  - EncryptedPyQFile - Transparent AES-GCM encryption

### UI Framework Documentation

- **[UI Base](ui-base.md)** - Foundation framework and lifecycle management
  - Base class with lifecycle hooks
  - QABCLoggingMeta metaclass
  - Navigation and utility methods

- **[UI Widgets](ui-widgets.md)** - Reusable widgets
  - Notification - Toast notifications
  - Browser - Embedded web browser with cookie management
  - MediaPlayer - Full-featured media player
  - ClickableWidget - Click-enabled widgets

- **[UI Pages](ui-pages.md)** - Page components for navigation
  - Base page class
  - Player page
  - Browser page

- **[UI Windows](ui-windows.md)** - Main window framework
  - Base window class
  - Page management
  - Navigation system

### Additional Resources

- **[API Reference](api-reference.md)** - Complete API documentation
- **[Examples](examples.md)** - Code examples and tutorials
- **[Best Practices](best-practices.md)** - Design patterns and recommendations

## Quick Links

### Getting Started

1. [Installation](https://github.com/Winipedia/winipyside/blob/main/README.md#installation)
2. [Quick Start](https://github.com/Winipedia/winipyside/blob/main/README.md#quick-start)
3. [Basic Application Example](examples.md#basic-application)

### Common Use Cases

- [Playing Encrypted Videos](core.md#encrypted-video-playback)
- [Building Multi-Page Applications](ui-windows.md#multi-page-application)
- [Cookie Management in Browser](ui-widgets.md#browser-cookie-management)
- [Custom Lifecycle Hooks](ui-base.md#lifecycle-hooks)

## Architecture Overview

Winipyside is organized into several key packages:

```text
winipyside/src/
├── core/              # Low-level I/O and encryption
│   └── py_qiodevice.py
└── ui/                # UI framework and components
    ├── base/          # Foundation classes
    ├── widgets/       # Reusable widgets
    ├── pages/         # Page components
    └── windows/       # Window framework
```

### Design Philosophy

1. **Type Safety**: 100% type annotated with strict mypy checking
2. **Modularity**: Reusable components with clear interfaces
3. **Lifecycle Management**: Consistent initialization patterns
4. **Testability**: Designed for easy testing with pytest-qt
5. **Production Ready**: CI/CD workflows for headless environments

## Key Concepts

### Lifecycle Hooks

All UI components follow a 4-phase initialization pattern:

1. **`base_setup()`** - Initialize Qt components
2. **`pre_setup()`** - Setup before main initialization
3. **`setup()`** - Main setup logic
4. **`post_setup()`** - Finalization after setup

### Page-Based Navigation

Applications use a QStackedWidget-based navigation system:

- **Windows** contain multiple **Pages**
- **Pages** can navigate to other pages
- Automatic menu generation for page switching

### Encrypted I/O

Transparent encryption/decryption using AES-GCM:

- Chunked encryption for efficient streaming
- Position mapping for random access
- Zero-copy decryption for media playback

## Contributing

See the [Contributing Guide](https://github.com/Winipedia/winipyside/blob/main/README.md#contributing) for information on:

- Setting up the development environment
- Running tests
- Code quality standards
- Submitting pull requests

## Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/Winipedia/winipyside/issues)
- **GitHub Discussions**: [Ask questions or share ideas](https://github.com/Winipedia/winipyside/discussions)
