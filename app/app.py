import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import requests
import os
from Criminal_Profiling import create_criminal_profiling_dashboard
from Crime_Pattern_Analysis import temporal_analysis, chloropleth_maps, crime_hotspots
from Predictive_modeling import predictive_modeling_recidivism
from Resource_Allocation import resource_allocation


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
    selected = option_menu(
        "Predictive Guardians",
        ['Home', 'Crime Pattern Analysis', 'Criminal Profiling', 'Predictive Modeling', 'Police Resource Allocation and Management'],
        icons=['house-fill', 'bar-chart-fill', 'fingerprint', 'cpu-fill', 'diagram-3-fill'],
        menu_icon="shield-shaded", default_index=0, orientation="vertical",
        styles = {
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



if selected == "Home":
    st.markdown("""
    <style>
    .hero-title { font-size: 2.6rem; font-weight: 800; background: linear-gradient(135deg, #1b9aaa, #06d6a0); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem; }
    .hero-sub { font-size: 1.1rem; color: #666; margin-bottom: 2rem; }
    .model-card { background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; border-left: 4px solid #1b9aaa; }
    .model-card h4 { color: #1b2838; margin: 0 0 0.5rem 0; }
    .model-card p { color: #555; font-size: 0.95rem; margin: 0; }
    .tech-badge { display: inline-block; background: #1b9aaa22; color: #1b9aaa; padding: 2px 10px; border-radius: 12px; font-size: 0.8rem; margin: 2px 3px; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="hero-title">🛡️ Predictive Guardians</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">AI-Driven Crime Prevention & Law Enforcement Intelligence Platform</p>', unsafe_allow_html=True)

    col_img, col_desc = st.columns([1, 2])
    with col_img:
        img_path = os.path.join(root_dir, 'assets', 'Home_Page_image.jpg')
        if os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
    with col_desc:
        st.markdown("""
        Predictive Guardians is an end-to-end **AI-powered analytics platform** that empowers law enforcement agencies 
        to shift from **reactive policing** to **proactive crime prevention**. 
        
        The system integrates **machine learning models**, **geospatial analysis**, and **optimization algorithms** 
        to deliver actionable intelligence across the core analytical modules.
        """)

    st.markdown("---")
    st.subheader("🧠 Analytical Models & Techniques")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="model-card">
            <h4>📈 Crime Pattern Analysis</h4>
            <p>Phân tích xu hướng tội phạm theo <b>thời gian</b> (năm/tháng/ngày), <b>không gian</b> (bản đồ Choropleth theo quận/huyện), 
            và phát hiện <b>điểm nóng</b> bằng thuật toán phân cụm <b>DBSCAN</b> trên bản đồ nhiệt Heatmap.</p>
            <span class="tech-badge">Plotly</span>
            <span class="tech-badge">Folium Heatmap</span>
            <span class="tech-badge">DBSCAN Clustering</span>
            <span class="tech-badge">GeoJSON</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="model-card">
            <h4>🔮 Predictive Modeling – Recidivism</h4>
            <p>Dự đoán khả năng <b>tái phạm</b> của đối tượng dựa trên đặc điểm nhân khẩu học (tuổi, nghề nghiệp, đẳng cấp, thành phố). 
            Sử dụng <b>H2O AutoML</b> tự động huấn luyện nhiều mô hình (GBM, XGBoost, Stacked Ensemble) và chọn mô hình tốt nhất.</p>
            <span class="tech-badge">H2O AutoML</span>
            <span class="tech-badge">Stacked Ensemble</span>
            <span class="tech-badge">StandardScaler</span>
            <span class="tech-badge">Frequency Encoding</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="model-card">
            <h4>👤 Criminal Profiling</h4>
            <p>Phân tích sâu đặc điểm <b>nhân khẩu học</b> của tội phạm: phân bố tuổi, giới tính, nghề nghiệp, đẳng cấp. 
            Kết hợp dữ liệu từ 3 nguồn (AccusedData, MOBsData, RowdySheeterDetails) để xây dựng hồ sơ toàn diện.</p>
            <span class="tech-badge">Data Merging</span>
            <span class="tech-badge">Plotly Interactive</span>
            <span class="tech-badge">Correlation Analysis</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="model-card">
            <h4>🚔 Police Resource Allocation</h4>
            <p>Tối ưu hóa phân bổ <b>ASI, CHC, CPC</b> đến từng khu vực bằng thuật toán <b>Linear Programming</b> (PuLP). 
            Hàm mục tiêu: tối đa hóa tổng trọng số mức độ nghiêm trọng × số lượng cảnh sát được phân bổ.</p>
            <span class="tech-badge">Linear Programming</span>
            <span class="tech-badge">PuLP Optimizer</span>
            <span class="tech-badge">Crime Severity Score</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("⚙️ Data Pipeline")
    st.markdown("""
    ```
    Raw Data (CSV) → Ingest → Clean & Feature Engineering → Train Models (H2O AutoML) → Save Models (.zip/.pkl)
                                                                                              ↓
    Streamlit App ← Load Cleaned Data (Component_datasets/) ← Load Trained Models (models/)
    ```
    """)

    c1, c2, c3 = st.columns(3)
    c1.metric("📂 Data Sources", "5 CSV Files")
    c2.metric("🤖 ML Framework", "H2O AutoML")
    c3.metric("📊 Visualization", "Plotly + Folium")



# Cache data loading functions at module level (not inside conditionals)
@st.cache_data
def load_crime_pattern_data():
    url = "https://raw.githubusercontent.com/adarshbiradar/maps-geojson/master/states/karnataka.json"
    response = requests.get(url)
    geojson_data = response.json()
    data_file_path = os.path.join(root_dir, 'Component_datasets', 'Crime_Pattern_Analysis_Cleaned.csv')
    crime_pattern_analysis = pd.read_csv(data_file_path)
    mean_lat = crime_pattern_analysis['Latitude'].mean()
    mean_lon = crime_pattern_analysis['Longitude'].mean()
    return mean_lat, mean_lon, geojson_data, crime_pattern_analysis

@st.cache_data
def load_resource_data():
    data_file_path = os.path.join(root_dir, 'Component_datasets', 'Resource_Allocation_Cleaned.csv')
    return pd.read_csv(data_file_path)


# ============ PAGE ROUTING (elif chain = only ONE page renders) ============

if selected == "Crime Pattern Analysis":
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

elif selected == "Criminal Profiling":
    create_criminal_profiling_dashboard()

elif selected == "Predictive Modeling":
    predictive_modeling_recidivism()

elif selected == "Police Resource Allocation and Management":
    df = load_resource_data()
    resource_allocation(df)
