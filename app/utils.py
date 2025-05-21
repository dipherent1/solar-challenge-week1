# app/utils.py
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Cache data loading to improve performance
@st.cache_data # Use st.cache_data for dataframes
def load_country_data(country_name):
    """Loads cleaned data for a single country."""
    try:
        file_path = f"data/{country_name.lower().replace(' ', '')}_clean.csv"
        df = pd.read_csv(file_path)
        if 'Timestamp' in df.columns:
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df['Country'] = country_name # Add country column for combining later
        return df
    except FileNotFoundError:
        st.error(f"Error: Cleaned data file for {country_name} not found at {file_path}.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data for {country_name}: {e}")
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

    fig, ax = plt.subplots(figsize=(8, 5)) # Create a figure and an axes
    
    # Filter for non-negative values for solar metrics
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
         # Reorder columns for a more logical flow
        summary_table_pivot = summary_table_pivot.reindex(columns=metrics, level='Metric')
    return summary_table_pivot

def create_ranking_chart(df, metric="GHI"):
    """Creates a bar chart ranking countries by average GHI (or other metric)."""
    if df.empty or metric not in df.columns or 'Country' not in df.columns:
        st.warning(f"Not enough data or missing columns for ranking chart by {metric}.")
        return None

    # Consider metric > 0 for daytime potential if it's a solar metric
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