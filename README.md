# Solar Challenge Week 1

This repository contains the data science project for the Solar Challenge Week 1 assignment.

## Project Overview

This project is set up to analyze solar energy data and develop insights or models related to solar energy production, efficiency, or forecasting.

## Project Structure

```bash
├── .vscode/               # VSCode configuration
├── .github/               # GitHub Actions workflows
├── src/                   # Source code for use in this project
├── notebooks/             # Jupyter notebooks for exploration and analysis
├── tests/                 # Test files
├── scripts/               # Utility scripts
├── data/                  # Data files (not tracked by git)
├── requirements.txt       # Project dependencies
└── README.md              # The top-level README
```

## Environment Setup

### Prerequisites

- Python 3.8+
- Git

### Setting up the development environment

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/solar-challenge-week1.git
   cd solar-challenge-week1
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

- Use the notebooks in the `notebooks/` directory for data exploration and analysis
- Implement reusable code in the `src/` directory
- Add utility scripts to the `scripts/` directory
- Store data in the `data/` directory (not tracked by git)
- Run tests using pytest:

  ```bash
  pytest tests/
  ```

## Contributing

1. Create a new branch for your feature or bugfix
2. Make your changes
3. Run tests to ensure your changes don't break existing functionality
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
