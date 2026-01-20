# Contributing to Consciousness

Thank you for your interest in contributing to Consciousness, the AI consciousness proxy via regret pruning!

## Code of Conduct

This project follows a [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming environment for all contributors.

## How to Contribute

1. **Fork and Clone**: Fork the repository and clone your fork locally.
2. **Create a Branch**: Create a feature branch from `main` (e.g., `git checkout -b feature/add-new-endpoint`).
3. **Make Changes**: Implement your feature or fix, ensuring tests pass.
4. **Test**: Run `pytest` and check for linting issues with `flake8`.
5. **Commit**: Use clear, concise commit messages (e.g., "Add rate limiting to /prompt endpoint").
6. **Pull Request**: Open a PR with a detailed description, linking any related issues.

## Development Setup

- Python 3.9+
- Install dependencies: `pip install -r requirements.txt`
- Run tests: `pytest`
- Run locally: `python api/api_server.py`
- Docker: `docker-compose up --build`

## Code Style and Guidelines

- **Python**: Use type hints, docstrings, and follow PEP 8.
- **Modularity**: Keep logic in separate modules; avoid monolithic code.
- **Security**: Never expose secrets; use environment variables.
- **Testing**: Add unit tests for new features; aim for 80%+ coverage.
- **Documentation**: Update README/API docs for changes.

## Reporting Issues

- Use [GitHub Issues](https://github.com/fersiguenza/ai-consciusness/issues) for bugs or features.
- Provide steps to reproduce, expected vs. actual behavior, and environment details.

## Community

Join discussions in Issues or PRs. For questions, email maintainers or open an issue.

Thank you for helping make Remorse better!
- Be respectful and constructive.
- All contributions are welcome!
