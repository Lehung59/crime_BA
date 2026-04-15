import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium.plugins import HeatMap
from sklearn.cluster import DBSCAN
import numpy as np
from streamlit_folium import st_folium
from datetime import datetime
import branca.colormap as cm

# --- Common style settings ---
COLOR_BG = 'rgba(0,0,0,0)'
COLOR_GRID = 'rgba(128,128,128,0.15)'
FONT_FAMILY = 'Inter, Segoe UI, Roboto, sans-serif'
ACCENT = '#1b9aaa'

common_layout = dict(
    font=dict(family=FONT_FAMILY, size=13, color='#333'),
    paper_bgcolor=COLOR_BG,
    plot_bgcolor=COLOR_BG,
    margin=dict(l=60, r=30, t=60, b=50),
    hoverlabel=dict(bgcolor='#1b2838', font_size=13, font_family=FONT_FAMILY,
                    font_color='white', bordercolor=ACCENT),
)

chart_colors = ['#1b9aaa', '#06d6a0', '#f4a261', '#e63946', '#577590',
                '#4ecdc4', '#ff6b6b', '#95e1d3', '#a8dadc', '#457b9d']


def temporal_analysis(crime_pattern_analysis):

    st.markdown("""
    <div style="background: linear-gradient(135deg, #e8f8f5, #d1f2eb); border-left: 4px solid #1b9aaa; 
                border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 1rem;">
        <b>Mục tiêu:</b> Phân tích xu hướng tội phạm theo <b>thời gian</b> — phát hiện các mùa/giai đoạn có tần suất tội phạm cao bất thường.<br>
        Chọn bộ lọc bên dưới và quan sát biểu đồ thay đổi theo thời gian.
    </div>
    """, unsafe_allow_html=True)

    # Filters in columns for cleaner layout
    col_f1, col_f2 = st.columns(2)

    with col_f1:
        district_options = ["Tất cả Quận/Huyện"] + sorted(crime_pattern_analysis["District_Name"].unique())
        selected_districts = st.multiselect("Chọn Quận/Huyện", district_options, default=[])

    with col_f2:
        crime_group_options = ["Tất cả Nhóm tội"] + sorted(crime_pattern_analysis["CrimeGroup_Name"].unique())
        selected_crime_groups = st.multiselect("Chọn Nhóm tội phạm", crime_group_options, default=[])

    selected_time_granularity = st.radio("Mức độ chi tiết thời gian", ["Năm", "Tháng", "Ngày"], horizontal=True)

    # Map Vietnamese to column names
    time_map = {"Năm": "Year", "Tháng": "Month", "Ngày": "Day"}
    time_col = time_map[selected_time_granularity]

    # Filter data based on selections
    filtered_df = crime_pattern_analysis.copy()
    if selected_districts and "Tất cả Quận/Huyện" not in selected_districts:
        filtered_df = filtered_df[filtered_df["District_Name"].isin(selected_districts)]
    if selected_crime_groups and "Tất cả Nhóm tội" not in selected_crime_groups:
        filtered_df = filtered_df[filtered_df["CrimeGroup_Name"].isin(selected_crime_groups)]

    # Temporal analysis visualizations
    if filtered_df.empty or (not selected_districts and not selected_crime_groups):
        st.warning("⚠️ Hãy chọn Quận/Huyện và Nhóm tội phạm từ bộ lọc phía trên để xem biểu đồ.")
    else:
        data = filtered_df.groupby([time_col, "District_Name", "CrimeGroup_Name"]).size().reset_index(name="Count")

        fig = px.bar(data, x=time_col, y="Count", color="District_Name",
                     barmode="group", hover_data=["CrimeGroup_Name"],
                     color_discrete_sequence=chart_colors,
                     labels={time_col: selected_time_granularity, "Count": "Số vụ",
                             "District_Name": "Quận/Huyện", "CrimeGroup_Name": "Nhóm tội"})

        layout_temporal = {**common_layout, 'margin': dict(l=60, r=30, t=60, b=100)}
        fig.update_layout(
            **layout_temporal,
            title=dict(text=f'Xu hướng Tội phạm theo {selected_time_granularity}',
                       font=dict(size=18, color='#1b2838')),
            xaxis=dict(title=selected_time_granularity, gridcolor=COLOR_GRID),
            yaxis=dict(title='Số vụ phạm tội', gridcolor=COLOR_GRID, showgrid=True),
            legend=dict(title_text='Quận/Huyện', orientation='h', yanchor='top', y=-0.18, xanchor='center', x=0.5,
                        font=dict(size=11)),
            bargap=0.2,
        )
        st.plotly_chart(fig, width='stretch')

        # Quick stats
        total = data['Count'].sum()
        peak_time = data.groupby(time_col)['Count'].sum().idxmax()
        peak_val = data.groupby(time_col)['Count'].sum().max()
        sc1, sc2, sc3 = st.columns(3)
        sc1.metric("Tổng số vụ (đã lọc)", f"{total:,}")
        sc2.metric(f"{selected_time_granularity} cao nhất", f"{peak_time}")
        sc3.metric("Số vụ cao nhất", f"{peak_val:,}")


def crime_hotspot_analysis(df, mean_lat, mean_lon):
    # Create base map
    m = folium.Map(location=[mean_lat, mean_lon], zoom_start=7)

    # Create colormap
    colormap = cm.LinearColormap(colors=['blue', 'yellow', 'red'], vmin=0, vmax=df['Count'].max())

    # Add heatmap
    HeatMap(df[['Latitude', 'Longitude', 'Count']].values.tolist(),
            gradient={"0.4": 'blue', "0.65": 'yellow', "1.0": 'red'},
            radius=15).add_to(m)

    # Perform DBSCAN clustering
    coords = df[['Latitude', 'Longitude']].values
    dbscan = DBSCAN(eps=0.1, min_samples=5)
    df['Cluster'] = dbscan.fit_predict(coords)

    # Add markers for cluster centers
    for cluster in df['Cluster'].unique():
        if cluster != -1:  # -1 is noise in DBSCAN
            cluster_points = df[df['Cluster'] == cluster]
            center_lat = cluster_points['Latitude'].mean()
            center_lon = cluster_points['Longitude'].mean()
            count = cluster_points['Count'].sum()
            folium.Marker(
                [center_lat, center_lon],
                popup=f'Cụm {cluster}<br>Số vụ: {count}',
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)

    # Add colormap legend to map
    colormap.add_to(m)
    colormap.caption = 'Mật độ Tội phạm'

    return m



def crime_hotspots(crime_pattern_analysis, mean_lat, mean_lon):

    st.markdown("""
    <div style="background: linear-gradient(135deg, #e8f8f5, #d1f2eb); border-left: 4px solid #1b9aaa; 
                border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 1rem;">
        <b>Mục tiêu:</b> Phát hiện <b>điểm nóng tội phạm</b> bằng thuật toán phân cụm <b>DBSCAN</b> 
        kết hợp bản đồ nhiệt (Heatmap).<br>
        Chọn khoảng thời gian và loại tội, nhấn <b>"Hiển thị bản đồ"</b> để xem kết quả.
    </div>
    """, unsafe_allow_html=True)

    # Filters in columns
    col1, col2 = st.columns(2)

    with col1:
        dates = st.radio("Khoảng thời gian", ["Tất cả", "Tùy chỉnh"], horizontal=True)

    if dates == "Tất cả":
        date_range = (crime_pattern_analysis['Date'].min(), crime_pattern_analysis['Date'].max())
    else:
        date_range = st.date_input("Chọn khoảng ngày",
                                    [crime_pattern_analysis['Date'].min(), crime_pattern_analysis['Date'].max()],
                                    key='date_range')

    if len(date_range) != 2:
        st.stop()

    # Crime type filter
    crime_types = st.multiselect("Chọn loại tội phạm", crime_pattern_analysis['CrimeGroup_Name'].unique())

    if len(crime_types) == 0:
        st.info("👆 Hãy chọn ít nhất 1 loại tội phạm để hiển thị bản đồ điểm nóng.")

    # Filter data
    filtered_data = crime_pattern_analysis[
        (crime_pattern_analysis['Date'] >= pd.Timestamp(date_range[0])) &
        (crime_pattern_analysis['Date'] <= pd.Timestamp(date_range[1]))
    ]
    if crime_types:
        filtered_data = filtered_data[filtered_data['CrimeGroup_Name'].isin(crime_types)]

    if st.button("Hiển thị bản đồ", type="primary") and len(crime_types) != 0:
        with st.spinner("Đang phân tích và vẽ bản đồ..."):
            # Aggregate data
            aggregated_data = filtered_data.groupby(
                ['District_Name', 'UnitName', 'Latitude', 'Longitude', 'CrimeGroup_Name']
            ).size().reset_index(name='Count')

            # Calculate mean lat and lon
            mean_lat = aggregated_data['Latitude'].mean()
            mean_lon = aggregated_data['Longitude'].mean()

            total_crimes = aggregated_data['Count'].sum()

            s1, s2, s3 = st.columns(3)
            s1.metric("Tổng số vụ", f"{total_crimes:,}")
            s2.metric("Số khu vực", f"{len(aggregated_data)}")
            s3.metric("Thuật toán", "DBSCAN")

            # Create and display maps
            m = crime_hotspot_analysis(aggregated_data, mean_lat, mean_lon)
            st_folium(m, width=900, height=500)

        # Explanation
        st.markdown("""
        ---
        #### 🔎 Cách đọc bản đồ:
        - **Vùng đỏ** trên bản đồ nhiệt = mật độ tội phạm **cao** (điểm nóng)
        - **Vùng xanh** = mật độ **thấp**
        - **📍 Markers đỏ** = tâm của các **cụm tội phạm** do DBSCAN phát hiện (click để xem chi tiết)
        - 🔍 **Zoom vào** để xem chi tiết từng khu vực cụ thể
        """)



def chloropleth_maps(df, geojson_data, mean_lat, mean_lon):

    st.markdown("""
    <div style="background: linear-gradient(135deg, #e8f8f5, #d1f2eb); border-left: 4px solid #1b9aaa; 
                border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 1rem;">
        <b>Mục tiêu:</b> So sánh mức độ tội phạm giữa các <b>quận/huyện</b> trên bản đồ Choropleth — 
        quận nào có màu đậm hơn là quận có tội phạm nhiều hơn.
    </div>
    """, unsafe_allow_html=True)

    # Group data by District_Name
    district_stats = df.groupby('District_Name').agg({
        'FIRNo': 'count', 'VICTIM COUNT': 'sum', 'Accused Count': 'sum'
    }).reset_index()

    # Compact summary row
    top_district = district_stats.sort_values('FIRNo', ascending=False).iloc[0]
    st.markdown(f"""
    <div style="display: flex; gap: 2rem; font-size: 0.9rem; color: #555; margin-bottom: 0.8rem;">
        <span><b>Quận cao nhất:</b> {top_district['District_Name']}</span>
        <span><b>Số vụ:</b> {int(top_district['FIRNo']):,}</span>
        <span><b>Nạn nhân:</b> {int(top_district['VICTIM COUNT']):,}</span>
    </div>
    """, unsafe_allow_html=True)

    # Choose the crime statistic to display
    stat_options = {
        'Số vụ phạm tội': ('FIRNo', 'Crime Incidents'),
        'Tổng số nạn nhân': ('VICTIM COUNT', 'Total Victim Count'),
        'Tổng số bị cáo': ('Accused Count', 'Total Accused Count'),
    }
    selected_stat = st.selectbox('Chọn chỉ số hiển thị', list(stat_options.keys()))
    col_name, label = stat_options[selected_stat]

    fig = px.choropleth_mapbox(
        district_stats,
        geojson=geojson_data,
        locations='District_Name',
        featureidkey="properties.district",
        color=col_name,
        color_continuous_scale=[[0, '#b5fffc'], [0.3, '#41ead4'], [0.6, '#1b9aaa'], [1.0, '#0d1b2a']],
        mapbox_style="carto-positron",
        zoom=5,
        center={"lat": mean_lat, "lon": mean_lon},
        opacity=0.65,
        labels={col_name: selected_stat},
        title=f'Bản đồ Choropleth: {selected_stat} theo Quận/Huyện'
    )

    fig.update_layout(
        **common_layout,
        height=550,
        title=dict(font=dict(size=17, color='#1b2838')),
    )
    st.plotly_chart(fig, width='stretch')

    st.caption("Hover chuột lên từng quận để xem chi tiết số liệu. Màu càng đậm = tội phạm càng nhiều.")
