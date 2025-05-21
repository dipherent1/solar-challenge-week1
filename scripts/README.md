## Interactive Dashboard

An interactive dashboard has been developed using Streamlit to visualize the cross-country comparison of solar irradiance data.

### Setup and Running the Dashboard

1. **Prerequisites:**
    * Python 3.8+
    * Ensure cleaned CSV data files (`benin_clean.csv`, `sierraleone_clean.csv`, `togo_clean.csv`) are present in the `data/` directory.

2. **Create a virtual environment (recommended):**

    ```bash
    python -m venv .venv
    # On Windows
    .venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Streamlit application:**

    ```bash
    streamlit run app/main.py
    ```

    The application will open in your default web browser.

### Features

* Select one or more countries (Benin, Sierra Leone, Togo) for comparison.
* View boxplots for GHI, DNI, or DHI.
* See a summary table of mean, median, and standard deviation for these metrics.
* View a bar chart ranking countries by average GHI.
