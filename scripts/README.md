# Solar Challenge Scripts

This directory contains utility scripts and command-line tools for processing solar energy data, training models, and generating reports.

## Purpose

- Solar data acquisition and preprocessing
- Weather data integration
- Automated model training and evaluation
- Batch prediction generation
- Report and visualization generation
- Data pipeline automation

## Available Scripts

### Data Processing

- `download_solar_data.py` - Downloads solar production data from specified sources
- `download_weather_data.py` - Downloads weather data for correlation with solar production
- `preprocess_solar_data.py` - Cleans and preprocesses raw solar data
- `merge_solar_weather.py` - Combines solar and weather datasets

### Modeling

- `train_forecasting_model.py` - Trains solar production forecasting models
- `evaluate_models.py` - Evaluates and compares different model performances
- `generate_predictions.py` - Generates predictions using trained models

### Reporting

- `generate_performance_report.py` - Creates performance reports for solar installations
- `create_visualization_dashboard.py` - Generates interactive visualizations
- `export_results.py` - Exports analysis results in various formats (CSV, Excel, JSON)

## Usage Examples

### Data Preprocessing

```bash
# Download solar production data for a specific date range
python scripts/download_solar_data.py --start-date 2023-01-01 --end-date 2023-12-31 --output data/raw/

# Preprocess solar data
python scripts/preprocess_solar_data.py --input data/raw/solar_data.csv --output data/processed/

# Merge solar data with weather data
python scripts/merge_solar_weather.py --solar data/processed/solar_clean.csv --weather data/raw/weather.csv --output data/processed/merged_data.csv
```

### Model Training and Evaluation

```bash
# Train a forecasting model
python scripts/train_forecasting_model.py --data data/processed/merged_data.csv --model-type random_forest --output models/rf_model.pkl

# Evaluate model performance
python scripts/evaluate_models.py --data data/processed/test_data.csv --models models/ --output reports/model_evaluation.json
```

### Report Generation

```bash
# Generate performance report
python scripts/generate_performance_report.py --data data/processed/merged_data.csv --predictions predictions/forecast.csv --output reports/performance_report.pdf
```

## Script Template

All scripts should follow this template structure:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Solar Challenge - [Script Name]

Description: Brief description of what the script does

Usage:
    python script_name.py [arguments]

Author: Your Name
Date: YYYY-MM-DD
"""

import argparse
import logging
import sys
from pathlib import Path

# Import project modules
from src.data import preprocessing
from src.models import forecasting

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Description of the script')

    parser.add_argument('--input', type=str, required=True,
                        help='Path to input data file')
    parser.add_argument('--output', type=str, required=True,
                        help='Path to output directory or file')

    return parser.parse_args()

def main():
    """Main function to execute the script."""
    # Parse arguments
    args = parse_arguments()

    # Log start of execution
    logger.info(f"Starting script with input: {args.input}")

    try:
        # Script logic here
        logger.info("Processing data...")

        # Example: Load data
        # data = pd.read_csv(args.input)

        # Example: Process data
        # processed_data = process_function(data)

        # Example: Save results
        # processed_data.to_csv(args.output)

        logger.info(f"Results saved to {args.output}")
        return 0

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```
