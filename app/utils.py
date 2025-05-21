# app/utils.py
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Define the correct mapping for filenames
COUNTRY_FILENAME_MAP = {
    "Benin": "benin_clean.csv",
    "Sierra Leone": "sierraleone-bumbuna_clean.csv",
    "Togo": "togo-dapaong_qc_clean.csv"
}

# Function to find the data directory and file
def find_data_file(filename):
    """
    Attempts to locate a data file by trying multiple possible paths.
    This helps the app work both locally and when deployed on Streamlit.
    """
    # List of possible paths to try, from most to least specific
    possible_paths = [
        # Current directory
        filename,
        # Relative to current directory
        os.path.join("data", filename),
        # Relative to parent directory
        os.path.join("..", "data", filename),
        # Absolute path from root directory
        os.path.join("/", "app", "data", filename),
        # Streamlit-specific paths
        os.path.join(os.getcwd(), "data", filename),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", filename),
    ]

    # Try each path
    for path in possible_paths:
        if os.path.exists(path):
            return path

    # If we get here, we couldn't find the file
    return None

# Cache data loading to improve performance
@st.cache_data
def load_country_data(country_name):
    """Loads cleaned data for a single country using the mapped filename."""
    if country_name not in COUNTRY_FILENAME_MAP:
        st.error(f"Error: Filename mapping not found for {country_name}.")
        return pd.DataFrame()

    specific_filename = COUNTRY_FILENAME_MAP[country_name]

    # Try to find the file using our helper function
    file_path = find_data_file(specific_filename)

    # If we couldn't find the file, try to provide helpful debugging info
    if file_path is None:
        # Show debugging information to help troubleshoot
        st.error(f"Error: Could not find data file for {country_name} ({specific_filename})")
        st.info(f"Current working directory: {os.getcwd()}")
        st.info(f"Files in current directory: {os.listdir('.')}")
        if os.path.exists("data"):
            st.info(f"Files in data directory: {os.listdir('data')}")
        else:
            st.warning("Data directory not found!")
        return pd.DataFrame()

    try:
        df = pd.read_csv(file_path)
        if 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['Country'] = country_name
        return df
    except FileNotFoundError:
        st.error(f"Error: Data file for {country_name} not found at path '{file_path}'.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data for {country_name} from '{file_path}': {e}")
        return pd.DataFrame()

def get_combined_data(selected_countries_list):
    """Combines data for selected countries."""
    all_dfs = []
    for country in selected_countries_list:
        df = load_country_data(country)
        if not df.empty:
            all_dfs.append(df)

    if not all_dfs:
        return pd.DataFrame()

    return pd.concat(all_dfs, ignore_index=True)

def create_boxplot(df, metric, title):
    """Creates a boxplot for a given metric, colored by country."""
    if df.empty or metric not in df.columns or 'Country' not in df.columns:
        st.warning(f"Not enough data or missing columns ('{metric}', 'Country') to create boxplot for {metric}.")
        return None

    fig, ax = plt.subplots(figsize=(8, 5))

    plot_data = df[df[metric] >= 0] if metric in ['GHI', 'DNI', 'DHI'] else df

    if not plot_data.empty:
        sns.boxplot(data=plot_data, x='Country', y=metric, palette='viridis', ax=ax)
        ax.set_title(title)
        ax.set_ylabel(f'{metric} (W/m²)')
        ax.set_xlabel('Country')
        return fig
    else:
        st.warning(f"No data with {metric} >= 0 to plot.")
        return None

def create_summary_table(df, metrics):
    """Creates a summary table (mean, median, std) for selected metrics."""
    if df.empty:
        return pd.DataFrame()

    summary_stats_list = []
    for metric in metrics:
        if metric in df.columns:
            metric_data = df[df[metric] >= 0] if metric in ['GHI','DNI','DHI'] else df
            if not metric_data.empty:
                country_summary = metric_data.groupby('Country')[metric].agg(['mean', 'median', 'std']).reset_index()
                country_summary['Metric'] = metric
                summary_stats_list.append(country_summary)

    if not summary_stats_list:
        return pd.DataFrame()

    summary_table_concat = pd.concat(summary_stats_list)
    summary_table_pivot = summary_table_concat.pivot_table(
        index='Country',
        columns='Metric',
        values=['mean', 'median', 'std']
    )
    if not summary_table_pivot.empty:
         summary_table_pivot = summary_table_pivot.reindex(columns=metrics, level='Metric')
    return summary_table_pivot

def create_ranking_chart(df, metric="GHI"):
    """Creates a bar chart ranking countries by average GHI (or other metric)."""
    if df.empty or metric not in df.columns or 'Country' not in df.columns:
        st.warning(f"Not enough data or missing columns for ranking chart by {metric}.")
        return None

    data_for_ranking = df[df[metric] > 0] if metric in ['GHI', 'DNI', 'DHI'] else df

    if data_for_ranking.empty:
        st.warning(f"No data with {metric} > 0 for ranking chart.")
        return None

    avg_ranking = data_for_ranking.groupby('Country')[metric].mean().sort_values(ascending=False)

    if avg_ranking.empty:
        st.warning(f"Could not compute averages for ranking chart by {metric}.")
        return None

    fig, ax = plt.subplots(figsize=(7, 4))
    palette = sns.color_palette('viridis', n_colors=len(avg_ranking))
    avg_ranking.plot(kind='bar', color=palette, ax=ax)
    ax.set_title(f'Average {metric} (Daytime, {metric} > 0) by Country')
    ax.set_ylabel(f'Average {metric} (W/m²)')
    ax.set_xlabel('Country')
    plt.xticks(rotation=0)
    plt.tight_layout()
    return fig