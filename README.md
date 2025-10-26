# Model-Mix: Business Model Generation Application

A Streamlit-based application for generating business models, financial planning, and business analysis.

## 📋 Overview

Model-Mix is a comprehensive Streamlit application that helps entrepreneurs and businesses create detailed business models, including:
- Business Model Canvas generation
- Financial planning and projections
- Market analysis
- Persona development (B2C, B2B)
- Investment and financing calculations

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ (tested with Python 3.12.3)
- pip package manager
- sudo access (for installing system dependencies on Linux)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/jaqcquesndav/model-mix.git
   cd model-mix
   ```

2. **Install system dependencies** (Linux/Ubuntu):
   ```bash
   sudo apt-get update
   sudo apt-get install -y $(cat packages.txt | tr '\n' ' ')
   ```

3. **Install Python dependencies**:
   ```bash
   pip install --user -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   export API_KEY="your-openai-api-key"
   ```

5. **Run the application**:
   ```bash
   streamlit run mixbpm.py
   ```

The application will be available at `http://localhost:8501`

## 🧪 Testing

### Quick Test Setup

Run the automated setup script:
```bash
./setupTests.sh
```

### Manual Test Setup

1. **Install system dependencies** (see Installation step 2 above)

2. **Install test dependencies**:
   ```bash
   pip install --user -r requirements-test.txt
   ```

3. **Run tests**:
   ```bash
   pytest                          # Run all tests
   pytest -v                       # Verbose output
   pytest -m unit                  # Run only unit tests
   pytest --cov=. --cov-report=html  # With coverage report
   ```

For detailed testing instructions, see [TEST_SETUP.md](TEST_SETUP.md)

## 📦 System Dependencies

The application requires several system libraries for its dependencies (lxml, weasyprint, etc.). These are automatically installed in the DevContainer or can be manually installed from `packages.txt`:

- libxml2-dev, libxslt1-dev (for lxml)
- libpango-1.0-0, libpangocairo-1.0-0 (for weasyprint)
- libcairo2, libcairo2-dev (for weasyprint)
- libgdk-pixbuf2.0-0, libffi-dev
- pkg-config, python3-cffi, shared-mime-info

## 🐳 DevContainer / Codespaces

This repository includes a DevContainer configuration for easy development:

1. Open in GitHub Codespaces or VS Code with DevContainers extension
2. The container will automatically:
   - Install system dependencies from `packages.txt`
   - Install Python dependencies from `requirements.txt`
   - Start the Streamlit application on port 8501

## 📁 Project Structure

```
model-mix/
├── mixbpm.py                      # Main application file
├── requirements.txt               # Python dependencies
├── requirements-test.txt          # Test dependencies
├── packages.txt                   # System dependencies
├── setupTests.sh                  # Automated test setup script
├── pytest.ini                     # Pytest configuration
├── conftest.py                    # Pytest shared configuration
├── .gitignore                     # Git ignore rules
├── README.md                      # This file
├── TEST_SETUP.md                  # Detailed test setup guide
├── INSTALLATION_VERIFICATION.md   # Installation verification report
├── .devcontainer/
│   └── devcontainer.json         # DevContainer configuration
└── tests/
    ├── __init__.py
    ├── test_dependencies.py      # Dependency import tests
    └── test_utils.py             # Utility function tests
```

## 🔧 Key Features

### Business Model Generation
- Collect business information and personas
- Generate comprehensive business model canvas
- Export to DOCX format

### Financial Planning
- Calculate startup costs
- Project revenue and expenses
- Analyze profitability and cash flow
- Handle loans and financing

### Market Analysis
- Competitor analysis
- Market factors evaluation
- Problem tree analysis

### Personas
- B2C persona development
- B2B persona development
- Household (Ménage) persona development

## 🛠️ Development

### Running Tests
```bash
pytest tests/ -v
```

### Code Coverage
```bash
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

### Linting (if configured)
```bash
# Add your linting commands here
```

## 📝 Documentation

- [TEST_SETUP.md](TEST_SETUP.md) - Comprehensive test setup guide
- [INSTALLATION_VERIFICATION.md](INSTALLATION_VERIFICATION.md) - Installation verification report

## 🐛 Troubleshooting

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

### Tests fail with ImportError
Make sure all dependencies are installed:
```bash
pip install --user -r requirements.txt
pip install --user -r requirements-test.txt
```

## 📄 License

[Add your license information here]

## 👥 Contributing

[Add contribution guidelines here]

## 📞 Support

[Add support/contact information here]

---

**Note**: This application requires an OpenAI API key to function. Set the `API_KEY` environment variable or configure it in Streamlit secrets.
