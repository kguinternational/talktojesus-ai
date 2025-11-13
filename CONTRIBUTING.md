# Contributing to Talk to Jesus AI

Thank you for your interest in contributing to Talk to Jesus AI! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Respect the spiritual nature of this project

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Use the bug report template
3. Include detailed steps to reproduce
4. Add relevant logs and error messages

### Suggesting Features

1. Check if the feature has been suggested
2. Describe the feature and use case
3. Explain how it aligns with the project goals

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Add/update tests
5. Ensure all tests pass: `pytest`
6. Format code: `black .`
7. Run linter: `pylint *.py`
8. Commit with clear messages
9. Push to your fork
10. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/talktojesus-ai.git
cd talktojesus-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Run tests
pytest
```

## Code Style

- Follow PEP 8 guidelines
- Use Black for formatting (line length: 120)
- Add docstrings to functions and classes
- Keep functions focused and small
- Write descriptive variable names

## Testing

- Write tests for new features
- Maintain test coverage
- Test edge cases
- Include integration tests where appropriate

## Commit Messages

Use clear, descriptive commit messages:

```
Add feature: Zoom meeting recording support
Fix: Handle empty SMS messages correctly
Update: Improve AI response generation
Docs: Add API usage examples
```

## Questions?

Open an issue with the "question" label or reach out to maintainers.

Thank you for contributing!
