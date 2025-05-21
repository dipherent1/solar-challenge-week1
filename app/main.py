# app/main.py
import streamlit as st
import pandas as pd
from utils import get_combined_data, create_boxplot, create_summary_table, create_ranking_chart

# Page Configuration (do this first)
st.set_page_config(
    page_title="Solar Irradiance Dashboard",
    page_icon="☀️",
    layout="wide", # Use wide layout
    initial_sidebar_state="expanded"
)

# --- Main App ---
st.title("☀️ Cross-Country Solar Irradiance Comparison")
st.markdown("""
This dashboard visualizes and compares key solar irradiance metrics (GHI, DNI, DHI) 
for Benin, Sierra Leone, and Togo based on cleaned datasets.
""")

# --- Sidebar for User Inputs ---
st.sidebar.header("User Controls")
all_available_countries = ["Benin", "Sierra Leone", "Togo"]

# Widget to select countries
selected_countries = st.sidebar.multiselect(
    "Select countries to compare:",
    options=all_available_countries,
    default=all_available_countries # Default to all selected
)

if not selected_countries:
    st.warning("Please select at least one country from the sidebar to view data.")
    st.stop() # Stop execution if no countries are selected

# --- Load and Process Data based on selection ---
# This will use the cached function from utils.py
combined_df_selected = get_combined_data(selected_countries)

if combined_df_selected.empty:
    st.error("No data available for the selected countries. Please check data files or selections.")
    st.stop()

# --- Display Visualizations and Tables ---

st.header("Metric Distributions (Boxplots)")
st.markdown("Shows the distribution of GHI, DNI, and DHI for selected countries (values >= 0 W/m²).")

metrics_to_display = ['GHI', 'DNI', 'DHI']
selected_metric_boxplot = st.selectbox(
    "Select metric for Boxplot:",
    options=metrics_to_display,
    index=0 # Default to GHI
)

if selected_metric_boxplot:
    boxplot_fig = create_boxplot(combined_df_selected, selected_metric_boxplot, 
                                 f"Distribution of {selected_metric_boxplot} for Selected Countries")
    if boxplot_fig:
        st.pyplot(boxplot_fig)
    else:
        st.write(f"Could not generate boxplot for {selected_metric_boxplot}.")

st.markdown("---") # Separator

st.header("Summary Statistics Table")
st.markdown("Mean, Median, and Standard Deviation for GHI, DNI, DHI (values >= 0 W/m²).")
summary_df = create_summary_table(combined_df_selected, metrics_to_display)

if not summary_df.empty:
    # st.dataframe(summary_df.style.format("{:.2f}"))
    st.table(summary_df.style.format("{:.2f}")) # st.table is often cleaner for this
else:
    st.write("Could not generate summary table for the selected countries.")

st.markdown("---") # Separator

st.header("Country Ranking by Average GHI")
st.markdown("Ranks selected countries by their average GHI (daytime values, GHI > 0 W/m²).")
ranking_fig = create_ranking_chart(combined_df_selected, metric="GHI")
if ranking_fig:
    st.pyplot(ranking_fig)
else:
    st.write("Could not generate ranking chart.")


# --- Add Key Observations (from your notebook) ---
st.sidebar.markdown("---")
st.sidebar.header("Key Observations Summary")
st.sidebar.markdown("""
*   **Benin** often shows highest GHI & DNI.
*   **Sierra Leone** generally has lower GHI & very low DNI (more diffuse).
*   **Togo** performs strongly in GHI, often comparable to Benin.
*   *Differences in GHI across countries are statistically significant.*
""")
st.sidebar.markdown("*(This is a simplified summary. Refer to the full EDA notebook for details.)*")