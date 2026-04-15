import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# Determine the root directory of the project
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def normalize_rows(table):
    return table.div(table.sum(axis=1).replace(0, np.nan), axis=0).fillna(0) * 100


def log_color_scale(table):
    return np.log10(table + 1)


@st.cache_data
def prepare_time_heatmap_tables(time_data):
    month_axis = list(range(1, 13))

    dow_month = pd.crosstab(time_data['DayOfWeek'], time_data['Month']).reindex(
        index=range(7), columns=month_axis, fill_value=0
    )
    district_month = pd.crosstab(time_data['District_Name'], time_data['Month']).reindex(
        columns=month_axis, fill_value=0
    )
    district_month = district_month.loc[district_month.sum(axis=1).sort_values(ascending=False).index]

    top_crimes_time = time_data['CrimeGroup_Name'].value_counts().nlargest(8).index.tolist()
    crime_time_filtered = time_data[time_data['CrimeGroup_Name'].isin(top_crimes_time)]
    crime_month_heatmap = pd.crosstab(
        crime_time_filtered['CrimeGroup_Name'], crime_time_filtered['Month']
    ).reindex(index=top_crimes_time, columns=month_axis, fill_value=0)

    return (
        dow_month,
        normalize_rows(dow_month),
        district_month,
        normalize_rows(district_month),
        crime_month_heatmap,
        normalize_rows(crime_month_heatmap),
    )


def build_heatmap_figure(
    table,
    title,
    height,
    common_layout,
    use_percent=False,
    y_labels=None,
    show_text=True,
    color_table=None,
    colorbar_title=None,
):
    hover_template = (
        '<b>%{y}</b> — <b>%{x}</b><br>Tỷ trọng: %{z:.1f}%<extra></extra>'
        if use_percent
        else '<b>%{y}</b> — <b>%{x}</b><br>Số vụ: %{customdata:,}<extra></extra>'
    )
    z_values = table.values if color_table is None else color_table.values
    colorbar_title = colorbar_title or ('%' if use_percent else 'Số vụ')
    text_values = np.round(table.values, 1) if use_percent else table.values
    text_template = '%{text:.1f}' if use_percent else '%{text:,}'

    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        x=[f'Th{m}' for m in table.columns],
        y=y_labels if y_labels is not None else table.index,
        colorscale=[[0, '#f0fff1'], [0.25, '#b5fffc'], [0.5, '#41ead4'], [0.75, '#1b9aaa'], [1.0, '#0d1b2a']],
        hovertemplate=hover_template,
        colorbar=dict(title=dict(text=colorbar_title, font=dict(size=12))),
        customdata=table.values,
        text=text_values if show_text else None,
        texttemplate=text_template if show_text else None,
        textfont=dict(size=9 if height > 450 else 10),
    ))
    fig.update_layout(
        **common_layout,
        title=dict(text=title, font=dict(size=17, color='#1b2838')),
        xaxis=dict(title='Tháng', tickmode='linear', side='bottom'),
        yaxis=dict(title='', autorange='reversed'),
        height=height,
    )
    return fig


@st.fragment
def render_time_heatmaps_fragment(
    common_layout,
    dow_names,
    dow_month,
    dow_month_pct,
    district_month,
    district_month_pct,
    crime_month_heatmap,
    crime_month_heatmap_pct,
):
    heatmap_mode = st.radio(
        "Chế độ tính cho cụm heatmap mùa vụ",
        ["Số vụ", "Tỷ trọng (%)"],
        horizontal=True,
        key="criminal_profile_time_heatmap_mode",
    )
    use_percent = heatmap_mode == "Tỷ trọng (%)"

    selected_dow_month = dow_month_pct if use_percent else dow_month
    selected_district_month = district_month_pct if use_percent else district_month
    selected_crime_month = crime_month_heatmap_pct if use_percent else crime_month_heatmap

    st.markdown("#### 6a. Cụm heatmap mùa vụ")
    st.markdown(f"""
    <div class="story-insight">
        <b>Diễn giải:</b> Cụm này gom ba heatmap để đọc đồng thời theo cùng một cách tính; chế độ hiện tại là <b>{heatmap_mode}</b>.<br><br>
        <b>Vì sao có thể như vậy:</b> Khi đặt các heatmap cạnh nhau, có thể so sánh nhanh mẫu hình theo ngày, theo địa bàn và theo loại tội để xem biến động mùa vụ xuất hiện ở cấp nào rõ nhất.<br><br>
        <b>Điểm cần thận trọng:</b> {"Ở chế độ tỷ trọng, mỗi hàng được chuẩn hóa về 100% nên phù hợp để so sánh mẫu hình tương đối, không phải quy mô tuyệt đối." if use_percent else "Ở chế độ số vụ, heatmap Quận/Huyện × Tháng dùng thang màu log vì dữ liệu rất lệch về Bengaluru Urban; nếu không nén thang màu, các địa bàn còn lại sẽ gần như không đọc được."} Nguồn hiện ghi nhận <b>{len(district_month)}</b> quận/huyện.<br><br>
        <b>Gợi ý nghiệp vụ:</b> Nên dùng chế độ <b>Tỷ trọng (%)</b> để nhận diện thời điểm “nóng” trong từng địa bàn và dùng chế độ <b>Số vụ</b> để quyết định ưu tiên phân bổ lực lượng ở mức quy mô thực tế.
    </div>
    """, unsafe_allow_html=True)

    heatmap_tabs = st.tabs([
        "Ngày × Tháng",
        "Quận/Huyện × Tháng",
        "Loại tội × Tháng",
    ])

    with heatmap_tabs[0]:
        st.markdown("##### 6a. Bản đồ nhiệt: Ngày trong tuần × Tháng")
        fig_dow_month = build_heatmap_figure(
            selected_dow_month,
            f"Heatmap: Ngày trong tuần × Tháng ({heatmap_mode})",
            380,
            common_layout,
            use_percent=use_percent,
            y_labels=dow_names,
            show_text=True,
        )
        st.plotly_chart(fig_dow_month, use_container_width=True)

    with heatmap_tabs[1]:
        st.markdown("##### 6b. Tính mùa vụ theo địa lý: Quận/Huyện nào nóng vào tháng nào?")
        district_color_table = selected_district_month if use_percent else log_color_scale(selected_district_month)
        fig_dist_month = build_heatmap_figure(
            selected_district_month,
            f"Heatmap: Quận/Huyện × Tháng ({heatmap_mode}{', màu log' if not use_percent else ''})",
            max(380, len(selected_district_month) * 30 + 100),
            common_layout,
            use_percent=use_percent,
            show_text=False,
            color_table=district_color_table,
            colorbar_title='%' if use_percent else 'log10(Số vụ + 1)',
        )
        st.plotly_chart(fig_dist_month, use_container_width=True)

    with heatmap_tabs[2]:
        st.markdown("##### 6c. Chi tiết: Heatmap loại tội theo tháng")
        fig_time_heat = build_heatmap_figure(
            selected_crime_month,
            f"Heatmap: Top 8 nhóm tội × Tháng ({heatmap_mode})",
            450,
            common_layout,
            use_percent=use_percent,
            show_text=True,
        )
        st.plotly_chart(fig_time_heat, use_container_width=True)


def create_criminal_profiling_dashboard():

    # Construct the file path
    data_file_path = os.path.join(root_dir, 'data', 'processed', 'Criminal_Profiling_cleaned.csv')
    Criminal_Profiling = pd.read_csv(data_file_path)

    # --- Common style settings ---
    COLOR_BG = 'rgba(0,0,0,0)'
    COLOR_GRID = 'rgba(128,128,128,0.15)'
    FONT_FAMILY = 'Inter, Segoe UI, Roboto, sans-serif'
    ACCENT = '#1b9aaa'
    ACCENT2 = '#06d6a0'

    common_layout = dict(
        font=dict(family=FONT_FAMILY, size=13, color='#333'),
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        margin=dict(l=60, r=30, t=60, b=50),
        hoverlabel=dict(bgcolor='#1b2838', font_size=13, font_family=FONT_FAMILY,
                        font_color='white', bordercolor=ACCENT),
    )

    crime_palette = ['#1b9aaa', '#06d6a0', '#f4a261', '#e63946', '#577590', '#4ecdc4', '#ff6b6b', '#95e1d3']

    # ======================================================================
    # HEADER
    # ======================================================================
    st.markdown("""
    <style>
    .story-question { font-size: 1.3rem; font-weight: 700; color: #1b2838; margin: 0.5rem 0 0.3rem 0; }
    .story-insight { background: linear-gradient(135deg, #e8f8f5, #d1f2eb); border-left: 4px solid #1b9aaa; 
                     border-radius: 8px; padding: 1rem 1.2rem; margin: 0.8rem 0 1rem 0; font-size: 0.95rem; color: #2c3e50; }
    .story-insight b { color: #1b9aaa; }
    .section-num { display: inline-block; background: #1b9aaa; color: white; width: 32px; height: 32px; 
                   border-radius: 50%; text-align: center; line-height: 32px; font-weight: 700; font-size: 0.95rem; margin-right: 10px; }
    </style>
    """, unsafe_allow_html=True)

    st.title("Criminal Profiling — Data Story")
    st.markdown("> *Phân tích đặc điểm nhân khẩu học của đối tượng phạm tội tại Karnataka, Ấn Độ — "
                "dựa trên dữ liệu từ Cảnh sát Bang Karnataka (KSP).*")
    
    total_records = len(Criminal_Profiling)
    n_castes = Criminal_Profiling['Caste'].nunique() if 'Caste' in Criminal_Profiling.columns else 0
    n_crimes = Criminal_Profiling['Crime_Group1'].nunique() if 'Crime_Group1' in Criminal_Profiling.columns else 0

    m1, m2, m3 = st.columns(3)
    m1.metric("Tổng hồ sơ", f"{total_records:,}")
    m2.metric("Số nhóm đẳng cấp", f"{n_castes}")
    m3.metric("Loại tội phạm", f"{n_crimes}")

    st.markdown("---")

    # ======================================================================
    # SECTION 1: AGE DISTRIBUTION
    # ======================================================================
    st.markdown('<p class="story-question"><span class="section-num">1</span>Tội phạm có độ tuổi tập trung như thế nào?</p>', unsafe_allow_html=True)

    age_data = Criminal_Profiling['age'].dropna()
    age_mean = age_data.mean()
    age_median = age_data.median()
    age_mode = age_data.mode().iloc[0] if len(age_data.mode()) > 0 else age_mean

    # Compute age group distribution for insight
    young = (age_data < 35).sum()
    young_pct = young / len(age_data) * 100

    st.markdown(f"""
    <div class="story-insight">
        <b>Diễn giải:</b> Phân bố tuổi tập trung mạnh ở nhóm trẻ và trung niên trẻ; tuổi trung bình là <b>{age_mean:.1f}</b>, trung vị là <b>{age_median:.0f}</b>, và khoảng <b>{young_pct:.1f}%</b> hồ sơ nằm dưới 35 tuổi.<br><br>
        <b>Vì sao có thể như vậy:</b> Đây thường là nhóm tham gia lao động, di chuyển và tương tác xã hội nhiều nhất, nên vừa có mức phơi nhiễm xung đột cao hơn, vừa dễ xuất hiện trong các vụ việc đường phố, tranh chấp hoặc vi phạm bột phát.<br><br>
        <b>Điểm cần thận trọng:</b> Biểu đồ phản ánh số hồ sơ đã ghi nhận, không phải rủi ro thực tế sau khi chuẩn hóa theo quy mô dân số từng nhóm tuổi; vì vậy không nên diễn giải trực tiếp thành “nhóm tuổi nào nguy hiểm hơn”.<br><br>
        <b>Gợi ý nghiệp vụ:</b> Nếu mục tiêu là phòng ngừa, có thể ưu tiên chương trình can thiệp sớm cho nhóm 18-35 tuổi tại các điểm nóng về xung đột, rượu bia, giao thông và tái phạm.
    </div>
    """, unsafe_allow_html=True)

    # Histogram
    counts, bin_edges = np.histogram(age_data, bins=25)
    bin_centers = [(bin_edges[i] + bin_edges[i+1]) / 2 for i in range(len(bin_edges)-1)]
    max_count = max(counts) if max(counts) > 0 else 1
    bar_colors = [f'rgba(27, {154 - int(100*c/max_count)}, {170 - int(60*c/max_count)}, {0.6 + 0.4*c/max_count})' for c in counts]

    fig_age = go.Figure()
    fig_age.add_trace(go.Bar(
        x=bin_centers, y=counts,
        width=[(bin_edges[1] - bin_edges[0]) * 0.9] * len(counts),
        marker=dict(color=bar_colors, line=dict(color='rgba(255,255,255,0.3)', width=1)),
        hovertemplate='<b>Age:</b> %{x:.0f}<br><b>Count:</b> %{y:,}<extra></extra>',
    ))
    fig_age.add_vline(x=age_mean, line_dash="dash", line_color="#e63946", line_width=2,
                      annotation_text=f"Mean: {age_mean:.1f}", annotation_position="top right",
                      annotation_font=dict(color="#e63946", size=12, family=FONT_FAMILY))
    fig_age.add_vline(x=age_median, line_dash="dot", line_color="#f4a261", line_width=2,
                      annotation_text=f"Median: {age_median:.1f}", annotation_position="top left",
                      annotation_font=dict(color="#f4a261", size=12, family=FONT_FAMILY))
    fig_age.update_layout(**common_layout,
        title=dict(text='Phân bố Tuổi Đối tượng Phạm tội', font=dict(size=18, color='#1b2838')),
        xaxis=dict(title='Tuổi', gridcolor=COLOR_GRID, showgrid=True, zeroline=False, dtick=10, range=[5, 100]),
        yaxis=dict(title='Số lượng', gridcolor=COLOR_GRID, showgrid=True, zeroline=False),
        bargap=0.05, showlegend=False)
    st.plotly_chart(fig_age, width='stretch')

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tổng", f"{len(age_data):,}")
    col2.metric("Trung bình", f"{age_mean:.1f}")
    col3.metric("Trung vị", f"{age_median:.0f}")
    col4.metric("Độ lệch chuẩn", f"{age_data.std():.1f}")

    st.markdown("---")

    # ======================================================================
    # SECTION 2: GENDER ANALYSIS
    # ======================================================================
    st.markdown('<p class="story-question"><span class="section-num">2</span>Tỷ lệ giới tính trong hồ sơ tội phạm ra sao?</p>', unsafe_allow_html=True)

    gender_counts = Criminal_Profiling['Sex'].value_counts()
    dominant_gender = gender_counts.index[0]
    dominant_pct = gender_counts.iloc[0] / gender_counts.sum() * 100

    st.markdown(f"""
    <div class="story-insight">
        <b>Diễn giải:</b> Cơ cấu giới tính trong dữ liệu lệch rất mạnh; <b>{dominant_pct:.1f}%</b> hồ sơ thuộc về <b>{dominant_gender}</b>.<br><br>
        <b>Vì sao có thể như vậy:</b> Một phần có thể đến từ khác biệt về mô hình hành vi, mức độ tham gia vào các tình huống đối đầu ngoài xã hội và loại tội được ghi nhận phổ biến trong dữ liệu này.<br><br>
        <b>Điểm cần thận trọng:</b> Chênh lệch lớn cũng có thể phản ánh sai lệch ở khâu báo cáo, điều tra hoặc lập hồ sơ; do đó không nên xem đây là bằng chứng đầy đủ về phân bố giới trong toàn bộ hành vi phạm tội.<br><br>
        <b>Gợi ý nghiệp vụ:</b> Có thể dùng kết quả này để tinh chỉnh truyền thông phòng ngừa và tuần tra theo nhóm đối tượng tại các bối cảnh rủi ro cao, nhưng cần tránh biến nó thành tiêu chí suy đoán cá nhân.
    </div>
    """, unsafe_allow_html=True)

    # Only bar chart (no donut to avoid label overlap)
    gen_colors = crime_palette[:len(gender_counts)]
    fig_gen = go.Figure(data=[go.Bar(
        x=gender_counts.index, y=gender_counts.values,
        marker=dict(color=gen_colors, line=dict(color='rgba(255,255,255,0.4)', width=1)),
        text=[f"{v:,}<br>({v/gender_counts.sum()*100:.2f}%)" for v in gender_counts.values],
        textposition='outside', textfont=dict(size=13, color='#555'),
        hovertemplate='<b>%{x}</b><br>Count: %{y:,}<extra></extra>',
    )])
    fig_gen.update_layout(**common_layout,
        title=dict(text='Phân bố Giới tính', font=dict(size=18, color='#1b2838')),
        xaxis=dict(title='Giới tính', gridcolor=COLOR_GRID),
        yaxis=dict(title='Số lượng (log scale)', gridcolor=COLOR_GRID, showgrid=True, type='log'),
        height=400, bargap=0.4)
    st.plotly_chart(fig_gen, width='stretch')

    # Stats
    gen_cols = st.columns(len(gender_counts))
    for i, (label, count) in enumerate(gender_counts.items()):
        gen_cols[i].metric(label, f"{count:,}", f"{count/gender_counts.sum()*100:.2f}%")

    st.markdown("---")

    # ======================================================================
    # SECTION 3: CASTE ANALYSIS
    # ======================================================================
    st.markdown('<p class="story-question"><span class="section-num">3</span>Đẳng cấp (Caste) nào xuất hiện nhiều nhất trong hồ sơ?</p>', unsafe_allow_html=True)

    caste_counts = Criminal_Profiling[Criminal_Profiling['Caste'] != 'unknown']['Caste'].value_counts()
    top_castes = caste_counts[:10]
    top1_caste = top_castes.index[0]
    top1_pct = top_castes.iloc[0] / caste_counts.sum() * 100

    st.markdown(f"""
    <div class="story-insight">
        <b>Diễn giải:</b> Trong số hồ sơ có ghi nhận trường Caste, nhóm <b>"{top1_caste}"</b> chiếm <b>{top1_pct:.1f}%</b>; top 10 nhóm cộng lại chiếm <b>{top_castes.sum()/caste_counts.sum()*100:.1f}%</b> số quan sát hợp lệ.<br><br>
        <b>Vì sao có thể như vậy:</b> Kết quả có thể phản ánh đồng thời cơ cấu dân cư, điều kiện kinh tế - xã hội, mức độ hiện diện của từng nhóm trong địa bàn dữ liệu và cách hệ thống ghi nhận thông tin nhân thân.<br><br>
        <b>Điểm cần thận trọng:</b> Đây là biến rất nhạy cảm, lại có giá trị thiếu và chất lượng nhập liệu không đồng đều; không phù hợp để dùng như một tín hiệu dự báo trực tiếp hoặc căn cứ ưu tiên kiểm tra một nhóm xã hội cụ thể.<br><br>
        <b>Gợi ý nghiệp vụ:</b> Hướng sử dụng phù hợp hơn là rà soát chất lượng trường dữ liệu nhân thân, đánh giá thiên lệch ghi nhận và chỉ dùng biến này cho mục đích kiểm định dữ liệu hoặc nghiên cứu bối cảnh ở mức tổng hợp.
    </div>
    """, unsafe_allow_html=True)

    n_bars = len(top_castes)
    caste_colors = [f'rgba(27, 154, 170, {0.4 + 0.06*i})' for i in range(n_bars)][::-1]
    fig_caste = go.Figure(data=[go.Bar(
        x=top_castes.index, y=top_castes.values,
        marker=dict(color=caste_colors, line=dict(color='rgba(255,255,255,0.4)', width=1)),
        hovertemplate='<b>%{x}</b><br>Count: %{y:,}<extra></extra>',
        text=top_castes.values, textposition='outside', textfont=dict(size=11, color='#555'),
    )])
    fig_caste.update_layout(**common_layout,
        title=dict(text='Top 10 Đẳng cấp trong Hồ sơ Tội phạm', font=dict(size=18, color='#1b2838')),
        xaxis=dict(title='Đẳng cấp', gridcolor=COLOR_GRID, tickangle=-30),
        yaxis=dict(title='Số lượng', gridcolor=COLOR_GRID, showgrid=True), bargap=0.2)
    st.plotly_chart(fig_caste, width='stretch')

    st.markdown("---")

    # ======================================================================
    # SECTION 4: CRIME CATEGORIES
    # ======================================================================
    st.markdown('<p class="story-question"><span class="section-num">4</span>Loại tội phạm nào phổ biến nhất?</p>', unsafe_allow_html=True)

    top_crime_groups = Criminal_Profiling['Crime_Group1'].value_counts().nlargest(5)
    top_crime_heads = Criminal_Profiling['Crime_Head2'].value_counts().nlargest(5)
    top1_crime = top_crime_groups.index[0]

    st.markdown(f"""
    <div class="story-insight">
        <b>Diễn giải:</b> Nhóm tội phổ biến nhất là <b>"{top1_crime}"</b> với <b>{top_crime_groups.iloc[0]:,}</b> hồ sơ; top 5 nhóm chiếm <b>{top_crime_groups.sum()/Criminal_Profiling['Crime_Group1'].value_counts().sum()*100:.1f}%</b> toàn bộ dữ liệu, cho thấy cơ cấu hồ sơ tập trung vào một số nhóm chính.<br><br>
        <b>Vì sao có thể như vậy:</b> Những nhóm tội xuất hiện nhiều thường là các loại dễ phát hiện, dễ lập hồ sơ, hoặc có tần suất phát sinh cao trong đời sống thường nhật và môi trường đô thị.<br><br>
        <b>Điểm cần thận trọng:</b> Một nhóm tội lớn có thể đang gộp nhiều hành vi khác nhau theo cách phân loại của hệ thống; vì vậy cần đọc thêm lớp phân loại chi tiết trước khi ra quyết định nghiệp vụ.<br><br>
        <b>Gợi ý nghiệp vụ:</b> Công an có thể dùng biểu đồ này để xác định nhóm tội cần ưu tiên nguồn lực chuyên trách, truyền thông phòng ngừa và chỉ tiêu phân tích sâu ở bước tiếp theo.
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["Nhóm tội chính", "Phân loại nhỏ"])

    with tabs[0]:
        fig_cg = go.Figure(data=[go.Bar(
            x=top_crime_groups.index, y=top_crime_groups.values,
            marker=dict(color=crime_palette[:len(top_crime_groups)], line=dict(color='rgba(255,255,255,0.4)', width=1)),
            hovertemplate='<b>%{x}</b><br>Count: %{y:,}<extra></extra>',
            text=top_crime_groups.values, textposition='outside', textfont=dict(size=12, color='#555'))])
        fig_cg.update_layout(**common_layout,
            title=dict(text='Top 5 Nhóm Tội phạm Phổ biến nhất', font=dict(size=17, color='#1b2838')),
            xaxis=dict(title='Nhóm tội', gridcolor=COLOR_GRID, tickangle=-15),
            yaxis=dict(title='Số lượng', gridcolor=COLOR_GRID, showgrid=True), bargap=0.3)
        st.plotly_chart(fig_cg, width='stretch')

    with tabs[1]:
        fig_ch = go.Figure(data=[go.Bar(
            x=top_crime_heads.index, y=top_crime_heads.values,
            marker=dict(color=crime_palette[:len(top_crime_heads)], line=dict(color='rgba(255,255,255,0.4)', width=1)),
            hovertemplate='<b>%{x}</b><br>Count: %{y:,}<extra></extra>',
            text=top_crime_heads.values, textposition='outside', textfont=dict(size=12, color='#555'))])
        fig_ch.update_layout(**common_layout,
            title=dict(text='Top 5 Phân loại nhỏ', font=dict(size=17, color='#1b2838')),
            xaxis=dict(title='Phân loại', gridcolor=COLOR_GRID, tickangle=-15),
            yaxis=dict(title='Số lượng', gridcolor=COLOR_GRID, showgrid=True), bargap=0.3)
        st.plotly_chart(fig_ch, width='stretch')

    st.markdown("---")

    # ======================================================================
    # SECTION 5: CORRELATION & RELATIONSHIP ANALYSIS
    # ======================================================================
    st.markdown('<p class="story-question"><span class="section-num">5</span>Các yếu tố nhân khẩu học có mối tương quan nào với loại tội phạm?</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="story-insight">
        Phần này diễn giải các mối liên hệ chéo giữa tuổi, nghề nghiệp, đẳng cấp và loại tội phạm ở mức dữ liệu hồ sơ. Các biểu đồ dưới đây phù hợp để nhận diện mẫu hình mô tả, chưa đủ để kết luận quan hệ nguyên nhân.
    </div>
    """, unsafe_allow_html=True)

    # --- 5a: Age Group vs Crime Type Heatmap ---
    st.markdown("#### 5a. Nhóm tuổi nào liên quan đến loại tội phạm nào nhiều nhất?")

    cp_temp = Criminal_Profiling.copy()
    cp_temp['Age_Group'] = pd.cut(cp_temp['age'], bins=[0, 18, 25, 35, 45, 55, 65, 100],
                                  labels=['<18', '18-25', '25-35', '35-45', '45-55', '55-65', '65+'])
    top8_crimes = cp_temp['Crime_Group1'].value_counts().nlargest(8).index.tolist()
    cp_filtered = cp_temp[cp_temp['Crime_Group1'].isin(top8_crimes)]
    heatmap_data = pd.crosstab(cp_filtered['Age_Group'], cp_filtered['Crime_Group1'])

    # Find the peak cell for insight
    max_cell = heatmap_data.stack().idxmax()

    st.markdown(f"""
    <div class="story-insight">
        <b>Diễn giải:</b> Ô có tần suất lớn nhất nằm ở nhóm tuổi <b>{max_cell[0]}</b> và nhóm tội <b>"{max_cell[1]}"</b>, với <b>{heatmap_data.loc[max_cell[0], max_cell[1]]:,}</b> hồ sơ; nhìn tổng thể, nhóm <b>25-35</b> xuất hiện nổi bật hơn ở nhiều loại tội.<br><br>
        <b>Vì sao có thể như vậy:</b> Đây là giai đoạn tuổi có cường độ tham gia lao động, di chuyển và va chạm xã hội cao, nên dễ xuất hiện đồng thời ở nhiều nhóm hành vi khác nhau trong dữ liệu hồ sơ.<br><br>
        <b>Điểm cần thận trọng:</b> Heatmap dùng số lượng tuyệt đối, chưa chuẩn hóa theo quy mô dân số hay cơ cấu tuổi từng địa bàn; ô “nóng” vì vậy có thể phản ánh quy mô nhóm lớn chứ không hẳn là rủi ro cao hơn sau chuẩn hóa.<br><br>
        <b>Gợi ý nghiệp vụ:</b> Có thể dùng kết quả này để ưu tiên phân tích sâu hơn theo cặp <i>nhóm tuổi - nhóm tội</i>, từ đó thiết kế cảnh báo sớm và biện pháp phòng ngừa phù hợp hơn cho từng nhóm mục tiêu.
    </div>
    """, unsafe_allow_html=True)

    fig_heat = go.Figure(data=go.Heatmap(
        z=heatmap_data.values, x=heatmap_data.columns,
        y=heatmap_data.index.astype(str),
        colorscale=[[0, '#f0fff1'], [0.3, '#41ead4'], [0.6, '#1b9aaa'], [1.0, '#0d1b2a']],
        hovertemplate='<b>Tuổi:</b> %{y}<br><b>Tội:</b> %{x}<br><b>Số vụ:</b> %{z:,}<extra></extra>',
        colorbar=dict(title=dict(text='Số vụ', font=dict(size=12))),
    ))
    fig_heat.update_layout(**common_layout,
        title=dict(text='Heatmap: Nhóm tuổi × Loại tội phạm', font=dict(size=17, color='#1b2838')),
        xaxis=dict(title='Loại tội phạm', tickangle=-25),
        yaxis=dict(title='Nhóm tuổi'), height=450)
    st.plotly_chart(fig_heat, width='stretch')

    st.markdown("---")

    # --- 5b: Caste-Crime Treemap ---
    st.markdown("#### 5b. Đẳng cấp nào liên quan đến loại tội phạm nào?")

    cp_caste = Criminal_Profiling[Criminal_Profiling['Caste'] != 'unknown'].copy()
    top8_castes = cp_caste['Caste'].value_counts().nlargest(8).index.tolist()
    cp_caste = cp_caste[cp_caste['Caste'].isin(top8_castes)]
    cp_caste['Crime_Short'] = cp_caste['Crime_Group1'].str[:30]
    top1_caste_6b = top8_castes[0]
    top1_c_count = cp_caste[cp_caste['Caste'] == top1_caste_6b].shape[0]

    st.markdown(f"""
    <div class="story-insight">
        <b>Diễn giải:</b> Trong tập đã lọc để trực quan hóa, nhóm <b>"{top1_caste_6b}"</b> có số hồ sơ cao nhất với <b>{top1_c_count:,}</b> bản ghi; treemap cho thấy quy mô từng nhánh Caste và loại tội không phân bố đều.<br><br>
        <b>Vì sao có thể như vậy:</b> Sự chênh lệch có thể đến từ tổ hợp nhiều yếu tố như quy mô nhóm trong dân cư, đặc điểm địa bàn, chất lượng ghi nhận thông tin nhân thân và cách dữ liệu được lọc để hiển thị.<br><br>
        <b>Điểm cần thận trọng:</b> Đây là biểu đồ nhạy cảm và rất dễ bị diễn giải quá mức; nó chỉ nên được dùng để kiểm tra mẫu phân bố trong dữ liệu hồ sơ, không nên chuyển trực tiếp thành nhận định nghiệp vụ nhắm vào một nhóm xã hội.<br><br>
        <b>Gợi ý nghiệp vụ:</b> Nếu cần hành động, ưu tiên phù hợp là kiểm tra chất lượng dữ liệu, đối chiếu với cấu trúc dân cư địa bàn và đánh giá nguy cơ thiên lệch ghi nhận trước khi dùng biến này trong bất kỳ báo cáo chính sách nào.
    </div>
    """, unsafe_allow_html=True)

    treemap_data = cp_caste.groupby(['Caste', 'Crime_Short']).size().reset_index(name='Count')
    treemap_data = treemap_data.sort_values('Count', ascending=False).groupby('Caste').head(5)

    fig_tree = px.treemap(treemap_data, path=['Caste', 'Crime_Short'], values='Count',
                          color='Count', color_continuous_scale=[[0, '#b5fffc'], [0.5, '#1b9aaa'], [1.0, '#0d1b2a']],
                          title='Treemap: Đẳng cấp → Loại tội phạm')
    fig_tree.update_layout(**common_layout, height=550, title=dict(font=dict(size=17, color='#1b2838')))
    fig_tree.update_traces(hovertemplate='<b>%{label}</b><br>Số vụ: %{value:,}<extra></extra>', textinfo='label+value')
    st.plotly_chart(fig_tree, width='stretch')

    st.markdown("---")

    # --- 5c: Occupation vs Crime Group (Stacked Bar) ---
    st.markdown("#### 5c. Mối liên hệ giữa nghề nghiệp và loại hình tội phạm?")

    cp_occ = Criminal_Profiling[
        (Criminal_Profiling['Occupation'] != 'unknown') &
        (Criminal_Profiling['Occupation'] != 'Others PI Specify')
    ].copy()
    top_occs_list = cp_occ['Occupation'].value_counts().nlargest(8).index.tolist()
    top_crms_list = cp_occ['Crime_Group1'].value_counts().nlargest(5).index.tolist()
    cp_occ = cp_occ[cp_occ['Occupation'].isin(top_occs_list) & cp_occ['Crime_Group1'].isin(top_crms_list)]
    cp_occ['Crime_Short'] = cp_occ['Crime_Group1'].str[:25]
    cross_data = pd.crosstab(cp_occ['Occupation'], cp_occ['Crime_Short'])

    st.markdown("""
    <div class="story-insight">
        <b>Diễn giải:</b> Cơ cấu loại tội giữa các nhóm nghề nghiệp không giống nhau; mỗi nhóm có một mẫu phân bổ tương đối riêng trong tập hồ sơ được giữ lại.<br><br>
        <b>Vì sao có thể như vậy:</b> Môi trường làm việc, nhịp sinh hoạt, loại xung đột thường gặp và mức độ tiếp xúc với các bối cảnh rủi ro có thể khác nhau theo từng nhóm nghề nghiệp.<br><br>
        <b>Điểm cần thận trọng:</b> Biểu đồ đã loại các giá trị nghề nghiệp mơ hồ như <b>unknown</b> và <b>Others PI Specify</b>; do đó kết quả phù hợp để so sánh tương đối giữa các nhóm còn lại, nhưng không đại diện trọn vẹn cho toàn bộ hồ sơ.<br><br>
        <b>Gợi ý nghiệp vụ:</b> Nếu muốn ứng dụng thực tế, nên dùng kết quả này để thiết kế hoạt động phòng ngừa theo bối cảnh nghề nghiệp hoặc môi trường lao động, thay vì coi nghề nghiệp là đặc điểm dùng để suy đoán cá nhân.
    </div>
    """, unsafe_allow_html=True)

    fig_stack = go.Figure()
    stack_colors = ['#1b9aaa', '#06d6a0', '#f4a261', '#e63946', '#577590']
    for idx, crime_col in enumerate(cross_data.columns):
        fig_stack.add_trace(go.Bar(
            name=crime_col, y=cross_data.index, x=cross_data[crime_col], orientation='h',
            marker_color=stack_colors[idx % len(stack_colors)],
            hovertemplate=f'<b>{crime_col}</b><br>Nghề: %{{y}}<br>Số vụ: %{{x:,}}<extra></extra>',
        ))
    fig_stack.update_layout(**common_layout, barmode='stack',
        title=dict(text='Nghề nghiệp × Loại tội phạm (Stacked Bar)', font=dict(size=17, color='#1b2838')),
        xaxis=dict(title='Tổng số vụ', gridcolor=COLOR_GRID, showgrid=True),
        yaxis=dict(title='', gridcolor=COLOR_GRID),
        legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5, font=dict(size=11)),
        height=500, bargap=0.2)
    st.plotly_chart(fig_stack, width='stretch')

    st.markdown("---")

    # ======================================================================
    # SECTION 6: TIME ANALYSIS (YẾU TỐ THỜI GIAN)
    # ======================================================================
    st.markdown('<p class="story-question"><span class="section-num">6</span>Thời điểm nào trong năm/tháng thường xảy ra nhiều vụ phạm tội nhất?</p>', unsafe_allow_html=True)
    
    time_data_path = os.path.join(root_dir, 'data', 'processed', 'Crime_Pattern_Analysis_Cleaned.csv')
    if os.path.exists(time_data_path):
        time_data = pd.read_csv(time_data_path)
        time_data['Date'] = pd.to_datetime(time_data[['Year', 'Month', 'Day']], errors='coerce')
        time_data['DayOfWeek'] = time_data['Date'].dt.dayofweek  # 0=Mon, 6=Sun
        
        month_counts = time_data['Month'].value_counts().sort_index()
        top_month = month_counts.idxmax()
        top_month_val = month_counts.max()
        
        day_counts = time_data['Day'].value_counts().sort_index()
        top_day = day_counts.idxmax()
        top_day_val = day_counts.max()
        
        dow_counts = time_data['DayOfWeek'].value_counts().sort_index()
        dow_names = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'CN']
        busiest_dow = dow_names[dow_counts.idxmax()]
        quietest_dow = dow_names[dow_counts.idxmin()]
        
        st.markdown(f"""
        <div class="story-insight">
            <b>Diễn giải:</b> Theo dữ liệu hiện có, số hồ sơ đạt mức cao nhất vào <b>Tháng {top_month}</b> với <b>{top_month_val:,}</b> vụ; theo trục ngày trong tuần, <b>{busiest_dow}</b> là ngày có tần suất cao nhất và <b>{quietest_dow}</b> là thấp nhất.<br><br>
            <b>Vì sao có thể như vậy:</b> Mẫu hình thời gian thường chịu ảnh hưởng bởi nhịp sinh hoạt, lịch làm việc, mùa lễ hội, hoạt động kinh tế và cường độ tuần tra hoặc ghi nhận hồ sơ ở từng giai đoạn.<br><br>
            <b>Điểm cần thận trọng:</b> Đây là mẫu hình mô tả từ dữ liệu lịch sử; mức cao hay thấp ở một thời điểm có thể phản ánh đồng thời cả biến động thật ngoài thực tế lẫn thay đổi trong quy trình ghi nhận.<br><br>
            <b>Gợi ý nghiệp vụ:</b> Kết quả phù hợp để bố trí lực lượng theo mùa, theo ngày trong tuần và để xây dựng lịch tăng cường tuần tra vào các mốc có xác suất phát sinh cao hơn.
        </div>
        """, unsafe_allow_html=True)
        
        # --- 6.0: Key metrics row ---
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Tháng cao điểm", f"Tháng {top_month}", f"{top_month_val:,} vụ")
        m2.metric("Ngày cao điểm", f"Ngày {top_day}", f"{top_day_val:,} vụ")
        m3.metric("Thứ bận nhất", busiest_dow, f"{dow_counts.max():,} vụ")
        m4.metric("Thứ thấp nhất", quietest_dow, f"{dow_counts.min():,} vụ")

        (
            dow_month,
            dow_month_pct,
            district_month,
            district_month_pct,
            crime_month_heatmap,
            crime_month_heatmap_pct,
        ) = prepare_time_heatmap_tables(time_data)

        render_time_heatmaps_fragment(
            common_layout,
            dow_names,
            dow_month,
            dow_month_pct,
            district_month,
            district_month_pct,
            crime_month_heatmap,
            crime_month_heatmap_pct,
        )

        st.markdown("---")

        yearly_counts = time_data.groupby('Year').size().reset_index(name='Count')
        full_years = yearly_counts[yearly_counts['Year'] < 2024].copy()
        full_years['Growth'] = full_years['Count'].pct_change() * 100
        full_years['Growth_Text'] = full_years['Growth'].apply(
            lambda x: f"+{x:.1f}%" if x > 0 else (f"{x:.1f}%" if pd.notna(x) else "—"))
        covid_year = full_years.loc[full_years['Year'] == 2020]

        pre_covid = time_data[time_data['Year'].isin([2018, 2019])].groupby('Month').size() / 2
        during_covid = time_data[time_data['Year'] == 2020].groupby('Month').size()
        post_covid = time_data[time_data['Year'].isin([2022, 2023])].groupby('Month').size() / 2

        st.markdown("#### 6d. Xu hướng hàng năm & Tốc độ tăng trưởng tội phạm")
        st.markdown(f"""
        <div class="story-insight">
            <b>Diễn giải:</b> Chuỗi thời gian cho thấy số hồ sơ giảm mạnh trong giai đoạn <b>2019-2020</b>, sau đó phục hồi từ <b>2021</b> và đạt mức cao mới vào <b>2023</b>.<br><br>
            <b>Vì sao có thể như vậy:</b> Biến động này có thể gắn với thay đổi trong mức độ di chuyển, hoạt động kinh tế - xã hội, ưu tiên tuần tra và năng lực xử lý hồ sơ qua các giai đoạn khác nhau.<br><br>
            <b>Điểm cần thận trọng:</b> {f"Năm 2020 là năm giảm mạnh nhất, với tốc độ thay đổi <b>{covid_year['Growth'].values[0]:.1f}%</b> so với năm trước; tuy nhiên tăng trưởng phần trăm luôn cần đọc cùng quy mô tuyệt đối." if len(covid_year) > 0 and pd.notna(covid_year['Growth'].values[0]) else "Cần đọc chỉ số tăng trưởng cùng quy mô tuyệt đối để tránh hiểu sai các năm nền thấp."}<br><br>
            <b>Gợi ý nghiệp vụ:</b> Biểu đồ này phù hợp để đánh giá nhu cầu nguồn lực theo chu kỳ năm và rà soát xem thay đổi chính sách hay tổ chức trong từng giai đoạn có đi kèm biến động về khối lượng vụ việc hay không.
        </div>
        """, unsafe_allow_html=True)
        fig_yoy = go.Figure()
        bar_colors = ['#e63946' if y == 2020 else '#1b9aaa' for y in full_years['Year']]
        fig_yoy.add_trace(go.Bar(
            x=full_years['Year'], y=full_years['Count'],
            marker=dict(color=bar_colors, line=dict(color='rgba(255,255,255,0.4)', width=1)),
            text=[f"{v:,}" for v in full_years['Count']],
            textposition='outside', textfont=dict(size=11, color='#555'),
            hovertemplate='<b>Năm %{x}</b><br>Số vụ: %{y:,}<extra></extra>',
            name='Số vụ',
            yaxis='y'
        ))

        growth_data = full_years.dropna(subset=['Growth'])
        fig_yoy.add_trace(go.Scatter(
            x=growth_data['Year'], y=growth_data['Growth'],
            mode='lines+markers+text',
            line=dict(color='#f4a261', width=3, dash='dot'),
            marker=dict(size=10, color='#f4a261', line=dict(width=2, color='white')),
            text=growth_data['Growth_Text'],
            textposition='top center', textfont=dict(size=11, color='#f4a261', family=FONT_FAMILY),
            hovertemplate='<b>Năm %{x}</b><br>Tăng trưởng: %{y:.1f}%<extra></extra>',
            name='% Tăng trưởng',
            yaxis='y2'
        ))

        fig_yoy.update_layout(
            **common_layout,
            title=dict(text='Xu hướng Tội phạm Hàng năm (2016-2023)', font=dict(size=17, color='#1b2838')),
            xaxis=dict(title='Năm', tickmode='linear', dtick=1, gridcolor=COLOR_GRID),
            yaxis=dict(title='Số vụ phạm tội', gridcolor=COLOR_GRID, showgrid=True),
            yaxis2=dict(title='% Tăng trưởng', overlaying='y', side='right',
                       showgrid=False, zeroline=True, zerolinecolor='rgba(244,162,97,0.3)'),
            legend=dict(orientation='h', yanchor='bottom', y=-0.25, xanchor='center', x=0.5, font=dict(size=11)),
            height=500, bargap=0.3
        )
        st.plotly_chart(fig_yoy, use_container_width=True)

        st.markdown("---")

        st.markdown("#### 6e. Tác động COVID-19 lên xu hướng tội phạm theo tháng")
        st.markdown("""
        <div class="story-insight">
            <b>Diễn giải:</b> So sánh ba giai đoạn <b>trước COVID</b>, <b>trong COVID</b> và <b>sau COVID</b> cho thấy số hồ sơ giảm sâu nhất trong các tháng giữa năm 2020, sau đó phục hồi rõ ở giai đoạn hậu dịch.<br><br>
            <b>Vì sao có thể như vậy:</b> Các hạn chế đi lại, thay đổi cường độ hoạt động kinh tế và dịch chuyển ưu tiên quản lý trong thời gian dịch có thể làm thay đổi cả số vụ phát sinh lẫn số vụ được phát hiện hoặc lập hồ sơ.<br><br>
            <b>Điểm cần thận trọng:</b> Đây vẫn là so sánh mô tả giữa các giai đoạn; biểu đồ cho thấy sự trùng hợp về thời điểm, nhưng chưa đủ để khẳng định toàn bộ biến động là do riêng COVID.<br><br>
            <b>Gợi ý nghiệp vụ:</b> Có thể dùng kết quả này để xây dựng kịch bản ứng phó cho các giai đoạn gián đoạn lớn trong tương lai, nhất là bài toán giữ ổn định ghi nhận hồ sơ và phân bổ lực lượng theo mức độ hạn chế xã hội.
        </div>
        """, unsafe_allow_html=True)

        fig_covid = go.Figure()
        fig_covid.add_trace(go.Scatter(
            x=list(range(1, 13)), y=pre_covid.reindex(range(1, 13), fill_value=0).values,
            mode='lines+markers', name='Trước COVID (TB 2018-19)',
            line=dict(color='#577590', width=2.5),
            marker=dict(size=7, color='#577590'),
            hovertemplate='Tháng %{x}<br>TB/tháng: %{y:,.0f} vụ<extra></extra>'
        ))
        fig_covid.add_trace(go.Scatter(
            x=list(range(1, 13)), y=during_covid.reindex(range(1, 13), fill_value=0).values,
            mode='lines+markers', name='COVID (2020)',
            line=dict(color='#e63946', width=3, dash='dash'),
            marker=dict(size=9, color='#e63946', symbol='x'),
            hovertemplate='Tháng %{x}<br>Số vụ: %{y:,} vụ<extra></extra>'
        ))
        fig_covid.add_trace(go.Scatter(
            x=list(range(1, 13)), y=post_covid.reindex(range(1, 13), fill_value=0).values,
            mode='lines+markers', name='Sau COVID (TB 2022-23)',
            line=dict(color='#06d6a0', width=2.5),
            marker=dict(size=7, color='#06d6a0'),
            hovertemplate='Tháng %{x}<br>TB/tháng: %{y:,.0f} vụ<extra></extra>'
        ))
        fig_covid.add_vrect(
            x0=3.5, x1=6.5, fillcolor='rgba(230,57,70,0.08)', line_width=0,
            annotation_text='Lockdown', annotation_position='top',
            annotation_font=dict(size=11, color='#e63946')
        )
        fig_covid.update_layout(
            **common_layout,
            title=dict(text='So sánh trước / trong / sau COVID', font=dict(size=17, color='#1b2838')),
            xaxis=dict(title='Tháng', tickmode='linear', tick0=1, dtick=1, gridcolor=COLOR_GRID),
            yaxis=dict(title='Số vụ phạm tội (trung bình/tháng)', gridcolor=COLOR_GRID, showgrid=True),
            legend=dict(orientation='h', yanchor='bottom', y=-0.28, xanchor='center', x=0.5, font=dict(size=10)),
            height=500
        )
        st.plotly_chart(fig_covid, use_container_width=True)

        st.markdown("---")

        # --- 6f: Monthly Crime Composition — Stacked Area ---
        st.markdown("#### 6f. Cơ cấu loại tội phạm thay đổi như thế nào theo tháng?")

        top6_crimes = time_data['CrimeGroup_Name'].value_counts().nlargest(6).index.tolist()
        crime_month_comp = time_data[time_data['CrimeGroup_Name'].isin(top6_crimes)].groupby(
            ['Month', 'CrimeGroup_Name']).size().reset_index(name='Count')
        total_per_month = crime_month_comp.groupby('Month')['Count'].transform('sum')
        crime_month_comp['Share'] = crime_month_comp['Count'] / total_per_month * 100

        st.markdown("""
        <div class="story-insight">
            <b>Diễn giải:</b> Biểu đồ thể hiện sự thay đổi trong <b>cơ cấu</b> các nhóm tội theo tháng; trọng tâm ở đây là tỷ trọng tương đối giữa các nhóm, không phải quy mô tuyệt đối của toàn bộ vụ việc.<br><br>
            <b>Vì sao có thể như vậy:</b> Một số nhóm tội có thể nhạy hơn với mùa lễ hội, chu kỳ lao động, thời tiết hoặc cường độ kiểm tra chuyên đề, nên tỷ trọng của chúng thay đổi theo tháng.<br><br>
            <b>Điểm cần thận trọng:</b> Khi một nhóm tăng tỷ trọng, điều đó không nhất thiết đồng nghĩa số vụ tuyệt đối của nhóm đó tăng; cũng có thể là các nhóm khác giảm nhanh hơn trong cùng giai đoạn.<br><br>
            <b>Gợi ý nghiệp vụ:</b> Biểu đồ này phù hợp để lên kế hoạch theo mùa cho lực lượng chuyên trách, ví dụ điều chỉnh nhân sự theo nhóm tội có xu hướng tăng tỷ trọng trong từng giai đoạn của năm.
        </div>
        """, unsafe_allow_html=True)

        area_colors = ['#1b9aaa', '#06d6a0', '#f4a261', '#e63946', '#577590', '#4ecdc4']
        fig_area = go.Figure()
        for i, crime in enumerate(top6_crimes):
            crime_data = crime_month_comp[crime_month_comp['CrimeGroup_Name'] == crime].sort_values('Month')
            base_color = area_colors[i % len(area_colors)]
            fill_color = f"rgba({int(base_color[1:3], 16)}, {int(base_color[3:5], 16)}, {int(base_color[5:7], 16)}, 0.7)"

            fig_area.add_trace(go.Scatter(
                x=crime_data['Month'], y=crime_data['Share'],
                mode='lines', stackgroup='one',
                name=crime[:35],
                line=dict(width=0.5, color=base_color),
                fillcolor=fill_color,
                hovertemplate=f'<b>{crime[:30]}</b><br>Tháng %{{x}}<br>Tỷ trọng: %{{y:.1f}}%<extra></extra>',
            ))
        fig_area.update_layout(
            **common_layout,
            title=dict(text='Cơ cấu Top 6 loại tội theo Tháng (Stacked Area %)', font=dict(size=17, color='#1b2838')),
            xaxis=dict(title='Tháng', tickmode='linear', tick0=1, dtick=1, gridcolor=COLOR_GRID),
            yaxis=dict(title='Tỷ trọng (%)', gridcolor=COLOR_GRID, showgrid=True, range=[0, 100]),
            legend=dict(orientation='h', yanchor='bottom', y=-0.35, xanchor='center', x=0.5, font=dict(size=10)),
            height=450
        )
        st.plotly_chart(fig_area, use_container_width=True)

    st.markdown("---")

    # ======================================================================
    # SECTION 7: TIME ANALYSIS (YẾU TỐ THỜI GIAN)
    # ======================================================================
    st.markdown('<p class="story-question"><span class="section-num">7</span>Thời điểm nào trong năm/tháng thường xảy ra nhiều vụ phạm tội nhất?</p>', unsafe_allow_html=True)
    
    time_data_path = os.path.join(root_dir, 'Component_datasets', 'Crime_Pattern_Analysis_Cleaned.csv')
    if os.path.exists(time_data_path):
        time_data = pd.read_csv(time_data_path)
        
        month_counts = time_data['Month'].value_counts().sort_index()
        top_month = month_counts.idxmax()
        top_month_val = month_counts.max()
        
        day_counts = time_data['Day'].value_counts().sort_index()
        top_day = day_counts.idxmax()
        top_day_val = day_counts.max()
        
        st.markdown(f"""
        <div class="story-insight">
            📌 <b>Insight Phân tích Chuyên sâu:</b> Dữ liệu cho thấy số lượng tội phạm đạt đỉnh vào giai đoạn <b>Tháng 2 và Tháng 3</b> (tháng cao điểm nhất ghi nhận <b>{top_month_val:,}</b> vụ). 
            Tại Ấn Độ (đặc biệt là tiểu bang tỷ trọng nông nghiệp cao như Karnataka), đây là thời điểm kết thúc vụ mùa thu hoạch mùa đông (Rabi crop) và bước vào mùa khô hạn, 
            đồng thời 31/3 cũng là thời điểm chốt sổ cuối năm tài chính. 
            <br><br>
            Việc này phản ánh một thực tế đặc trưng: Hoạt động giao thương và tích trữ nông sản bán ra khiến tiền mặt lưu thông nhiều ở vùng nông thôn, 
            nhưng việc bảo vệ lỏng lẻo kết hợp với áp lực trả nợ cuối năm đẩy tỷ lệ <b>Trộm cắp (Theft)</b> và <b>Lừa đảo công nghệ cao (Cyber Crime)</b> tăng đột biến. 
            Thêm vào đó, đây là mùa của các lễ hội lớn đầu năm (Holi, Shivaratri), sự di chuyển ồ ạt dẫn đến bùng nổ các vụ <b>Tai nạn giao thông (Motor Vehicle Accidents)</b>.
            hiểu được "Tính mùa vụ" (Seasonality) này giúp cảnh sát chủ động điều phối quân số tuần tra trên quốc lộ và các điểm thu mua nông sản trước thềm tháng 2 hằng năm.
        </div>
        """, unsafe_allow_html=True)
        
        t1, t2 = st.columns(2)
        with t1:
            fig_month = px.line(x=month_counts.index, y=month_counts.values, markers=True)
            fig_month.update_traces(line_color='#e63946', line_width=3, marker=dict(size=8, color='#1b9aaa', line=dict(width=2, color='white')))
            fig_month.update_layout(**common_layout, 
                title=dict(text="Xu hướng tội phạm theo Tháng trong năm", font=dict(size=17, color='#1b2838')),
                xaxis=dict(title="Tháng", tickmode='linear', tick0=1, dtick=1, gridcolor=COLOR_GRID),
                yaxis=dict(title="Số vụ phạm tội", gridcolor=COLOR_GRID))
            st.plotly_chart(fig_month, use_container_width=True)
            
        with t2:
            fig_day = px.line(x=day_counts.index, y=day_counts.values, markers=True)
            fig_day.update_traces(line_color='#1b9aaa', line_width=3, marker=dict(size=6, color='#e63946', line=dict(width=1, color='white')))
            fig_day.update_layout(**common_layout, 
                title=dict(text="Tần suất tội phạm theo Ngày trong tháng", font=dict(size=17, color='#1b2838')),
                xaxis=dict(title="Ngày", tickmode='linear', tick0=1, dtick=5, gridcolor=COLOR_GRID),
                yaxis=dict(title="Số vụ phạm tội", gridcolor=COLOR_GRID))
            st.plotly_chart(fig_day, use_container_width=True)
            
        st.markdown("#### 7a. Mức độ tập trung loại hình tội phạm theo Tháng")
        top_crimes_time = time_data['CrimeGroup_Name'].value_counts().nlargest(6).index
        heatmap_time = pd.crosstab(time_data[time_data['CrimeGroup_Name'].isin(top_crimes_time)]['CrimeGroup_Name'], time_data['Month'])
        
        fig_time_heat = go.Figure(data=go.Heatmap(
            z=heatmap_time.values, x=heatmap_time.columns, y=heatmap_time.index,
            colorscale=[[0, '#f0fff1'], [0.4, '#41ead4'], [0.7, '#1b9aaa'], [1.0, '#0d1b2a']],
            hovertemplate='<b>Tháng:</b> %{x}<br><b>Loại tội:</b> %{y}<br><b>Số vụ:</b> %{z:,}<extra></extra>',
            colorbar=dict(title=dict(text='Số vụ', font=dict(size=12))),
        ))
        fig_time_heat.update_layout(**common_layout, 
            title=dict(text='Heatmap: Tần suất nhóm tội phạm mũi nhọn theo Tháng', font=dict(size=17, color='#1b2838')),
            xaxis=dict(title="Tháng", tickmode='linear', dtick=1),
            yaxis=dict(title=""), height=420)
        st.plotly_chart(fig_time_heat, use_container_width=True)

    st.markdown("---")

    # ======================================================================
    # CONCLUSION
    # ======================================================================
    st.markdown("### Kết luận & Khuyến nghị")
    st.markdown(f"""
    Từ việc phân tích **{total_records:,}** hồ sơ tội phạm tại Karnataka, chúng tôi rút ra các kết luận chính:
    
    1. **Nhóm tuổi rủi ro cao**: Đối tượng phạm tội tập trung mạnh ở độ tuổi **25-35** ({young_pct:.0f}% dưới 35 tuổi).
    2. **Giới tính**: **{dominant_pct:.0f}%** là nam giới — chính sách phòng chống nên tập trung vào nhóm này.
    3. **Yếu tố xã hội**: Đẳng cấp và nghề nghiệp có mối tương quan rõ rệt với tần suất phạm tội.
    4. **Đẳng cấp trọng điểm**: Nhóm đẳng cấp **"{top1_caste}"** có số hồ sơ phạm tội cao nhất.
    5. **Loại tội chủ đạo**: **"{top1_crime}"** chiếm tỷ trọng lớn nhất.
    {f'6. **Thời điểm phạm tội**: Tháng {top_month} và ngày {top_day} hàng tháng là các mốc có tần suất cao nhất, cần chú ý tuần tra.' if 'top_month' in locals() else ''}
    
    > *Các kết quả trên phù hợp để làm đầu vào cho các bước phân tích tiếp theo như dự báo tái phạm hoặc hỗ trợ phân bổ nguồn lực, với điều kiện tiếp tục kiểm tra chất lượng dữ liệu và mức độ đại diện của từng biến.*
    """)
