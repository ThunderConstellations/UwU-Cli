# 🤝 Contributing to UwU-CLI

Thank you for your interest in contributing to UwU-CLI! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic knowledge of Python development

### Development Setup
```bash
# Clone the repository
git clone https://github.com/UwU-CLI/UwU-Cli.git
cd UwU-Cli

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

## 🔧 Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes
- Write clean, well-documented code
- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes
```bash
# Run all tests
python -m pytest tests/

# Run specific test files
python test_specific_feature.py

# Run linting
python -m flake8 .
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "feat: add new feature description"
```

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```

## 📝 Code Style Guidelines

### Python Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for all public functions
- Keep functions small and focused
- Use type hints where appropriate

### Example
```python
def process_user_input(user_input: str) -> str:
    """
    Process user input and return formatted response.
    
    Args:
        user_input: The raw user input string
        
    Returns:
        Formatted response string
        
    Raises:
        ValueError: If input is empty or invalid
    """
    if not user_input.strip():
        raise ValueError("Input cannot be empty")
    
    # Process the input
    processed = user_input.strip().lower()
    return f"Processed: {processed}"
```

### Commit Message Format
Use conventional commit format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Test additions/changes
- `chore:` - Maintenance tasks

## 🧪 Testing Guidelines

### Writing Tests
- Write tests for all new functionality
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies
- Aim for high test coverage

### Example Test
```python
import pytest
from utils.example import process_user_input

def test_process_user_input_valid():
    """Test processing valid user input."""
    result = process_user_input("Hello World")
    assert result == "Processed: hello world"

def test_process_user_input_empty():
    """Test processing empty input raises error."""
    with pytest.raises(ValueError, match="Input cannot be empty"):
        process_user_input("")

def test_process_user_input_whitespace():
    """Test processing whitespace-only input raises error."""
    with pytest.raises(ValueError, match="Input cannot be empty"):
        process_user_input("   ")
```

## 🔒 Security Guidelines

### Never Commit Sensitive Information
- API keys
- Passwords
- Tokens
- Database credentials
- User-specific information

### Configuration Files
- Use templates for configuration
- Store actual credentials in environment variables
- Add sensitive files to `.gitignore`
- Use `.env` files for local development

## 📚 Documentation

### Code Documentation
- Add docstrings to all public functions
- Include examples in docstrings
- Document complex algorithms
- Explain business logic

### User Documentation
- Update README.md for new features
- Add usage examples
- Document configuration options
- Include troubleshooting guides

## 🐛 Bug Reports

### Before Reporting
1. Check existing issues
2. Search the documentation
3. Try to reproduce the issue
4. Check if it's a configuration issue

### Bug Report Template
```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 11, macOS 12, Ubuntu 20.04]
- Python Version: [e.g., 3.9.7]
- UwU-CLI Version: [e.g., 2.0.0]

**Additional Information**
Any other relevant information
```

## 💡 Feature Requests

### Before Requesting
1. Check if the feature already exists
2. Search existing issues
3. Consider if it fits the project scope
4. Think about implementation complexity

### Feature Request Template
```markdown
**Feature Description**
Clear description of the requested feature

**Use Case**
Why this feature is needed

**Proposed Implementation**
How you think it could be implemented

**Alternatives Considered**
Other approaches you've considered

**Additional Information**
Any other relevant information
```

## 🔄 Pull Request Process

### Before Submitting
1. Ensure all tests pass
2. Update documentation
3. Follow code style guidelines
4. Add appropriate labels

### Pull Request Template
```markdown
**Description**
Brief description of changes

**Type of Change**
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

**Testing**
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

**Documentation**
- [ ] README updated
- [ ] Code comments added
- [ ] API documentation updated

**Breaking Changes**
- [ ] No breaking changes
- [ ] Breaking changes documented
```

## 🏷️ Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements or additions to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `priority: high` - High priority issue
- `priority: low` - Low priority issue
- `status: blocked` - Blocked by other issues
- `status: in progress` - Currently being worked on

## 📞 Getting Help

### Questions and Discussion
- Use GitHub Discussions for questions
- Join our community chat
- Check existing documentation

### Development Help
- Ask questions in issues
- Request code reviews
- Seek guidance on complex changes

## 🎯 Contribution Ideas

### Good First Issues
- Documentation improvements
- Test coverage improvements
- Code style fixes
- Simple bug fixes

### Advanced Contributions
- New features
- Performance improvements
- Architecture changes
- Plugin development

## 🏆 Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- Project documentation
- Community acknowledgments

## 📋 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers learn
- Follow community guidelines

---

**Thank you for contributing to UwU-CLI! Your contributions help make this project better for everyone.** 🎉 