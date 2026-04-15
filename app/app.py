import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
from statsmodels.tsa.seasonal import seasonal_decompose
import folium
from folium import plugins
from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_folium import st_folium
from Criminal_Profiling import create_criminal_profiling_dashboard
from Crime_Pattern_Analysis import *
from Case_Outcome_Monitoring import create_case_outcome_dashboard
from Resource_Allocation import *
import os


root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# --- Custom CSS: Hide stale content during tab switch, show loading spinner ---
st.markdown("""
<style>
/* Hide old content when Streamlit is re-running (the "ghost" effect) */
[data-stale="true"] {
    opacity: 0 !important;
    transition: none !important;
}

/* Loading overlay that appears during re-run */
[data-stale="true"]::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(14, 17, 23, 0.92);
    z-index: 9998;
    opacity: 1 !important;
}

[data-stale="true"]::after {
    content: "⏳ Loading...";
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 9999;
    opacity: 1 !important;
    font-size: 1.5rem;
    font-weight: 600;
    color: #62d0ff;
    font-family: 'Inter', 'Segoe UI', sans-serif;
    text-align: center;
    animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
    50% { opacity: 0.5; transform: translate(-50%, -50%) scale(1.05); }
}

/* Also style the Streamlit running indicator */
.stStatusWidget { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu("Predictive Guardians",
        ['Phân tích Hình mẫu Tội phạm', 'Hồ sơ Tội phạm', 'Theo dõi Kết quả Xử lý', 'Phân bổ Nguồn lực Cảnh sát'],
        icons=['bar-chart-fill', 'fingerprint', 'clipboard-data-fill', 'diagram-3-fill'],
        menu_icon="shield-shaded", default_index=0, orientation="vertical",
        styles={
        "container": {"padding": "5!important", "background-color": "#1c1e21"},
        "menu-title": {"font-size": "18px", "font-weight": "bold", "color": "#e5e5e5"},
        "menu-icon": {"color": "#62d0ff"},
        "nav": {"background-color": "#1c1e21"},
        "nav-item": {"padding": "0px 10px"},
        "nav-link": {
            "text-decoration": "none",
            "color": "#e5e5e5",
            "font-size": "14px",
            "font-weight": "normal",
            "--hover-color": "#62d0ff",
        },
        "nav-link-selected": {
            "background-color": "#62d0ff",
            "color": "#1c1e21",
            "font-weight": "bold",
        },
        "icon": {"color": "#e5e5e5", "font-size": "16px"},
        "separator": {"margin": "5px 0px", "border-color": "#343a40"},
    }
    )


import json

# Cache data loading functions at module level
@st.cache_data
def load_crime_pattern_data():
    geojson_path = os.path.join(root_dir, 'data', 'raw', 'karnataka.json')
    with open(geojson_path, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
    data_file_path = os.path.join(root_dir, 'data', 'processed', 'Crime_Pattern_Analysis_Cleaned.csv')
    crime_pattern_analysis = pd.read_csv(data_file_path)
    mean_lat = crime_pattern_analysis['Latitude'].mean()
    mean_lon = crime_pattern_analysis['Longitude'].mean()
    return mean_lat, mean_lon, geojson_data, crime_pattern_analysis

@st.cache_data
def load_resource_data():
    data_file_path = os.path.join(root_dir, 'data', 'processed', 'Resource_Allocation_Cleaned.csv')
    return pd.read_csv(data_file_path)


# ============ PAGE ROUTING ============

if selected == "Phân tích Hình mẫu Tội phạm":
    mean_lat, mean_lon, geojson_data, crime_pattern_analysis = load_crime_pattern_data()

    st.title("Phân tích Hình mẫu Tội phạm")
    st.markdown("> *Khám phá xu hướng tội phạm theo thời gian, không gian và phát hiện điểm nóng bằng AI.*")
    st.markdown("---")

    st.subheader("Phân tích theo Thời gian")
    temporal_analysis(crime_pattern_analysis)

    st.markdown("---")

    st.subheader("Bản đồ Choropleth theo Quận/Huyện")
    chloropleth_maps(crime_pattern_analysis, geojson_data, mean_lat, mean_lon)

    st.markdown("---")

    st.subheader("Bản đồ Điểm nóng Tội phạm (Heatmap + DBSCAN)")
    crime_pattern_analysis = crime_pattern_analysis.reset_index(drop=True)
    mean_lat_sampled = crime_pattern_analysis['Latitude'].mean()
    mean_lon_sampled = crime_pattern_analysis['Longitude'].mean()
    crime_pattern_analysis['Date'] = pd.to_datetime(crime_pattern_analysis[['Year', 'Month', 'Day']])
    crime_hotspots(crime_pattern_analysis, mean_lat_sampled, mean_lon_sampled)

elif selected == "Hồ sơ Tội phạm":
    create_criminal_profiling_dashboard()

elif selected == "Theo dõi Kết quả Xử lý":
    create_case_outcome_dashboard()

elif selected == "Phân bổ Nguồn lực Cảnh sát":
    df = load_resource_data()
    resource_allocation(df)
