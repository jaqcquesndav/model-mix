# Model-Mix Test Setup

This document describes how to set up and run tests for the model-mix Streamlit application.

## Prerequisites

- Python 3.11+ (Python 3.12.3 is being used in this environment)
- pip package manager
- sudo access for installing system dependencies (on Linux)

## System Dependencies

The application requires several system libraries for proper functioning of dependencies like `lxml` and `weasyprint`. These are listed in `packages.txt`:

- **libxml2-dev**: XML processing library development files (required by lxml)
- **libxslt1-dev**: XSLT processing library development files (required by lxml)
- **libpango-1.0-0**: Text layout and rendering library (required by weasyprint)
- **libpangocairo-1.0-0**: Cairo rendering support for Pango (required by weasyprint)
- **libgdk-pixbuf2.0-0**: Image loading library (required by weasyprint)
- **libffi-dev**: Foreign Function Interface library development files
- **libcairo2**: 2D graphics library (required by weasyprint)
- **libcairo2-dev**: Cairo development files (required by weasyprint)
- **pkg-config**: Helper tool for compiling applications
- **python3-cffi**: C Foreign Function Interface for Python
- **shared-mime-info**: MIME database (required by weasyprint)

## Quick Setup

### Using the Setup Script (Recommended)

Run the automated setup script:

```bash
./setupTests.sh
```

This script will:
1. Install system dependencies from `packages.txt`
2. Install Python dependencies from `requirements.txt`
3. Install test dependencies (pytest, pytest-cov, pytest-mock)
4. Verify the installation

### Manual Setup

If you prefer to set up manually:

1. **Install system dependencies** (Linux/Ubuntu):
   ```bash
   sudo apt-get update
   sudo apt-get install -y libxml2-dev libxslt1-dev libpango-1.0-0 \
     libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev libcairo2 \
     libcairo2-dev pkg-config python3-cffi shared-mime-info
   ```

2. **Install Python dependencies**:
   ```bash
   pip install --user -r requirements.txt
   ```

3. **Install test dependencies**:
   ```bash
   pip install --user pytest pytest-cov pytest-mock
   ```

## Running Tests

### Run all tests
```bash
pytest
```

### Run with verbose output
```bash
pytest -v
```

### Run only unit tests
```bash
pytest -m unit
```

### Run with coverage report
```bash
pytest --cov=. --cov-report=html
```

The coverage report will be generated in the `htmlcov/` directory.

### Run specific test file
```bash
pytest tests/test_utils.py
```

### Run specific test function
```bash
pytest tests/test_utils.py::TestCalculerPretInteretFixe::test_calculer_pret_interet_fixe_basic
```

## Test Structure

```
model-mix/
├── tests/
│   ├── __init__.py
│   ├── test_dependencies.py    # Tests for dependency imports
│   └── test_utils.py           # Tests for utility functions
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
├── packages.txt                # System dependencies
├── setupTests.sh              # Automated setup script
└── mixbpm.py                  # Main application file
```

## Test Markers

Tests are marked with pytest markers for better organization:

- `@pytest.mark.unit`: Unit tests (fast, isolated tests)
- `@pytest.mark.integration`: Integration tests (slower, test component interactions)
- `@pytest.mark.slow`: Slow-running tests

## Troubleshooting

### lxml installation fails

If you see errors about missing `libxml2` or `libxslt`:
```bash
sudo apt-get install -y libxml2-dev libxslt1-dev
pip install --user lxml
```

### weasyprint installation fails

If you see errors related to Cairo or Pango:
```bash
sudo apt-get install -y libcairo2-dev libpango-1.0-0 libpangocairo-1.0-0 \
  libgdk-pixbuf2.0-0 pkg-config
pip install --user weasyprint
```

### ImportError in tests

Ensure all dependencies are installed:
```bash
pip install --user -r requirements.txt
pytest tests/test_dependencies.py -v
```

## Development Container

The repository includes a `.devcontainer/devcontainer.json` configuration that automatically:
- Sets up Python 3.11 environment
- Installs system dependencies from `packages.txt`
- Installs Python dependencies from `requirements.txt`
- Starts the Streamlit application

The devcontainer's `updateContentCommand` handles the installation process automatically when the container starts.

## CI/CD Considerations

When setting up CI/CD pipelines, ensure:

1. System dependencies from `packages.txt` are installed first
2. Python dependencies from `requirements.txt` are installed second
3. Test dependencies (pytest, etc.) are installed
4. Tests are run with appropriate markers if needed

Example GitHub Actions snippet:
```yaml
- name: Install system dependencies
  run: |
    sudo apt-get update
    sudo apt-get install -y $(cat packages.txt | tr '\n' ' ')

- name: Install Python dependencies
  run: |
    pip install -r requirements.txt
    pip install pytest pytest-cov

- name: Run tests
  run: pytest -v
```

## Contributing

When adding new tests:

1. Place test files in the `tests/` directory
2. Name test files with the `test_` prefix
3. Use appropriate markers (`@pytest.mark.unit`, etc.)
4. Follow existing test patterns for consistency
5. Ensure tests are isolated and don't depend on external resources

## Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [Streamlit documentation](https://docs.streamlit.io/)
- [lxml documentation](https://lxml.de/)
- [WeasyPrint documentation](https://doc.courtbouillon.org/weasyprint/)
