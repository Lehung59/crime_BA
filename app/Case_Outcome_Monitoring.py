import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# Determine the root directory of the project
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# --- Common style (same as Criminal_Profiling.py) ---
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

crime_palette = ['#1b9aaa', '#06d6a0', '#f4a261', '#e63946', '#577590',
                 '#4ecdc4', '#ff6b6b', '#95e1d3']


# ======================================================================
# CACHED DATA LOADING — chỉ đọc CSV 1 lần duy nhất
# ======================================================================
@st.cache_data(show_spinner="⏳ Đang tải dữ liệu Case Outcome lần đầu...")
def load_case_outcome_data():
    data_path = os.path.join(root_dir, 'data', 'processed', 'Case_Outcome_Cleaned.csv')
    return pd.read_csv(data_path)


# ======================================================================
# CACHED AGGREGATIONS — tính groupby nặng 1 lần, cache mãi mãi
# ======================================================================
@st.cache_data(show_spinner="⏳ Đang tính toán... (chỉ lần đầu, sau đó tức thì)")
def compute_aggregations(_df):
    """
    Tính tất cả groupby nặng 1 lần và cache lại.
    Prefix _ trên tham số để Streamlit KHÔNG hash DataFrame
    (DataFrame 1.28M rows nếu hash sẽ rất chậm).
    Được gọi với df thực, chạy 1 lần duy nhất rồi cache mãi.
    """
    df = _df

    # --- Summary metrics ---
    total = len(df)
    convicted = (df['Case_Outcome'] == 'Convicted').sum()
    undetected = (df['Case_Outcome'] == 'Undetected').sum()
    pending = (df['Case_Outcome'] == 'Pending Trial').sum()

    # --- Section 1: Per-district outcome ---
    dist_outcome = df.groupby(['District_Name', 'Case_Outcome']).size().unstack(fill_value=0)
    dist_total = dist_outcome.sum(axis=1)
    dist_conv_rate = (dist_outcome.get('Convicted', 0) / dist_total * 100).sort_values(ascending=False)

    # --- Section 2: Heinous by year + by district ---
    heinous_year = df.groupby(['Year', 'FIR_Type']).size().unstack(fill_value=0)
    heinous_dist = df[df['FIR_Type'] == 'Heinous'].groupby('District_Name').size().nlargest(15)

    # --- Section 3: Victim totals + by crime ---
    total_male_v = int(df['Victim_Adult_Male'].sum())
    total_female_v = int(df['Victim_Adult_Female'].sum())
    total_minor_v = int(df['Victim_Minor'].sum())
    victim_by_crime = df.groupby('Crime_Category').agg(
        Male=('Victim_Adult_Male', 'sum'),
        Female=('Victim_Adult_Female', 'sum'),
        Minor=('Victim_Minor', 'sum'),
    ).sort_values(by=['Female'], ascending=False).head(10)

    # --- Section 4: Crime outcome rates ---
    crime_outcome = df.groupby(['Crime_Category', 'Case_Outcome']).size().unstack(fill_value=0)
    crime_total = crime_outcome.sum(axis=1)
    crime_undetect_rate = (crime_outcome.get('Undetected', 0) / crime_total * 100).sort_values(ascending=False)
    crime_conv_rate_series = (crime_outcome.get('Convicted', 0) / crime_total * 100)

    # --- Section 5: Complaint mode ---
    mode_counts = df['Complaint_Mode'].value_counts().head(5)

    # --- District list for filter ---
    all_districts = sorted(df['District_Name'].unique())
    top10_districts = dist_total.nlargest(10).index.tolist()

    return {
        'total': total,
        'convicted': int(convicted),
        'undetected': int(undetected),
        'pending': int(pending),
        'dist_outcome': dist_outcome,
        'dist_total': dist_total,
        'dist_conv_rate': dist_conv_rate,
        'heinous_year': heinous_year,
        'heinous_dist': heinous_dist,
        'total_male_v': total_male_v,
        'total_female_v': total_female_v,
        'total_minor_v': total_minor_v,
        'victim_by_crime': victim_by_crime,
        'crime_total': crime_total,
        'crime_undetect_rate': crime_undetect_rate,
        'crime_conv_rate_series': crime_conv_rate_series,
        'mode_counts': mode_counts,
        'all_districts': all_districts,
        'top10_districts': top10_districts,
    }


def create_case_outcome_dashboard():
    """Module: Theo dõi & Đánh giá Hiệu quả Xử lý Vụ án"""

    # --- CSS (reuse Criminal Profiling style) ---
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

    # --- Load data & pre-computed aggregations (from cache) ---
    # Lần đầu: đọc CSV + tính groupby (~30-60s). Lần sau: lấy từ cache, tức thì.
    df = load_case_outcome_data()
    agg = compute_aggregations(df)
    
    # Unpack aggregations
    total = agg['total']
    convicted = agg['convicted']
    undetected = agg['undetected']
    pending = agg['pending']
    dist_outcome = agg['dist_outcome']
    dist_total = agg['dist_total']
    dist_conv_rate = agg['dist_conv_rate']
    heinous_year = agg['heinous_year']
    heinous_dist = agg['heinous_dist']
    total_male_v = agg['total_male_v']
    total_female_v = agg['total_female_v']
    total_minor_v = agg['total_minor_v']
    victim_by_crime = agg['victim_by_crime']
    crime_total = agg['crime_total']
    crime_undetect_rate = agg['crime_undetect_rate']
    crime_conv_rate_series = agg['crime_conv_rate_series']
    mode_counts = agg['mode_counts']
    all_districts = agg['all_districts']
    top10_districts = agg['top10_districts']

    conv_rate = convicted / total * 100
    detect_rate = (1 - undetected / total) * 100
    best_dist = dist_conv_rate.index[0]
    worst_dist = dist_conv_rate.index[-1]
    total_victims = total_male_v + total_female_v + total_minor_v

    # ======================================================================
    # HEADER
    # ======================================================================
    st.title("📊 Theo dõi & Đánh giá Hiệu quả Xử lý Vụ án")
    st.markdown("> *Phân tích tỷ lệ phá án, kết án, và đặc điểm nạn nhân — dựa trên 1.28 triệu hồ sơ FIR thực tế.*")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📋 Tổng hồ sơ FIR", f"{total:,}")
    m2.metric("✅ Kết án", f"{convicted:,}", f"{conv_rate:.1f}%")
    m3.metric("🔍 Tỷ lệ phá án", f"{detect_rate:.1f}%")
    m4.metric("⏳ Đang chờ xử", f"{pending:,}")

    st.markdown("---")

    # ======================================================================
    # SECTION 1: Case Outcome by District
    # ======================================================================
    st.markdown('<p class="story-question"><span class="section-num">1</span>'
                'Tỷ lệ kết án và phá án từng quận như thế nào?</p>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="story-insight">
        📌 <b>Insight:</b> Quận có tỷ lệ kết án cao nhất là <b>{best_dist}</b> ({dist_conv_rate.iloc[0]:.1f}%),
        trong khi quận thấp nhất là <b>{worst_dist}</b> ({dist_conv_rate.iloc[-1]:.1f}%).
        Sự chênh lệch lớn giữa các quận phản ánh sự khác biệt trong năng lực điều tra và nguồn lực tư pháp.
    </div>
    """, unsafe_allow_html=True)

    # Interactive filter (chỉ widget này cần re-run, biểu đồ dựa trên agg đã cache)
    selected_districts = st.multiselect(
        "Chọn quận/huyện để so sánh (mặc định: Top 10 quận có nhiều vụ nhất):",
        options=all_districts,
        default=top10_districts
    )

    dist_filtered = dist_outcome.loc[dist_outcome.index.isin(selected_districts)] \
        if selected_districts else dist_outcome.loc[dist_total.nlargest(10).index]

    outcome_colors = {
        'Convicted': '#06d6a0', 'Pending Trial': '#f4a261',
        'Undetected': '#e63946', 'Discharged/Acquitted': '#577590', 'Other': '#95e1d3',
    }
    fig_dist = go.Figure()
    for outcome in ['Convicted', 'Pending Trial', 'Undetected', 'Discharged/Acquitted', 'Other']:
        if outcome in dist_filtered.columns:
            fig_dist.add_trace(go.Bar(
                name=outcome, x=dist_filtered.index, y=dist_filtered[outcome],
                marker_color=outcome_colors.get(outcome, '#aaa'),
                hovertemplate=f'<b>{outcome}</b><br>Quận: %{{x}}<br>Số vụ: %{{y:,}}<extra></extra>',
            ))
    fig_dist.update_layout(**common_layout, barmode='stack',
        title=dict(text='Kết quả Xử lý Vụ án theo Quận/Huyện', font=dict(size=18, color='#1b2838')),
        xaxis=dict(title='Quận/Huyện', gridcolor=COLOR_GRID, tickangle=-30),
        yaxis=dict(title='Số vụ án', gridcolor=COLOR_GRID, showgrid=True),
        legend=dict(orientation='h', yanchor='bottom', y=-0.35, xanchor='center', x=0.5, font=dict(size=11)),
        height=500, bargap=0.2)
    st.plotly_chart(fig_dist, width='stretch')

    st.markdown("---")

    # ======================================================================
    # SECTION 2: Heinous vs Non-Heinous trend
    # ======================================================================
    st.markdown('<p class="story-question"><span class="section-num">2</span>'
                'Xu hướng tội phạm Nghiêm trọng vs Không nghiêm trọng qua các năm?</p>',
                unsafe_allow_html=True)

    heinous_rate = heinous_year.get('Heinous', 0) / heinous_year.sum(axis=1) * 100
    trend_dir = "tăng" if (len(heinous_rate) >= 2 and heinous_rate.iloc[-1] > heinous_rate.iloc[0]) else "giảm"

    st.markdown(f"""
    <div class="story-insight">
        📌 <b>Insight:</b> Tỷ lệ tội phạm nghiêm trọng (Heinous) đang có xu hướng <b>{trend_dir}</b>.
        Năm gần nhất, tội nghiêm trọng chiếm <b>{heinous_rate.iloc[-1]:.1f}%</b> tổng số vụ.
        Thông tin này giúp cảnh sát đánh giá liệu tình hình an ninh đang cải thiện hay xấu đi.
    </div>
    """, unsafe_allow_html=True)

    fig_heinous = go.Figure()
    for ftype, color in [('Heinous', '#e63946'), ('Non Heinous', '#1b9aaa')]:
        if ftype in heinous_year.columns:
            fig_heinous.add_trace(go.Scatter(
                x=heinous_year.index, y=heinous_year[ftype],
                name=ftype, mode='lines+markers',
                line=dict(width=3, color=color), marker=dict(size=8),
                hovertemplate=f'<b>{ftype}</b><br>Năm: %{{x}}<br>Số vụ: %{{y:,}}<extra></extra>',
            ))
    fig_heinous.update_layout(**common_layout,
        title=dict(text='Xu hướng Tội phạm Nghiêm trọng vs Không nghiêm trọng', font=dict(size=18, color='#1b2838')),
        xaxis=dict(title='Năm', gridcolor=COLOR_GRID, showgrid=True, dtick=1),
        yaxis=dict(title='Số vụ', gridcolor=COLOR_GRID, showgrid=True),
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5),
        height=420)
    st.plotly_chart(fig_heinous, width='stretch')

    fig_hd = go.Figure(data=[go.Bar(
        x=heinous_dist.values, y=heinous_dist.index, orientation='h',
        marker=dict(color=[f'rgba(230, 57, 70, {0.4 + 0.04*i})' for i in range(len(heinous_dist))][::-1]),
        text=heinous_dist.values, textposition='outside', textfont=dict(size=11, color='#555'),
        hovertemplate='<b>%{y}</b><br>Số vụ Heinous: %{x:,}<extra></extra>',
    )])
    fig_hd.update_layout(**common_layout,
        title=dict(text='Top 15 Quận có Tội phạm Nghiêm trọng nhiều nhất', font=dict(size=17, color='#1b2838')),
        xaxis=dict(title='Số vụ', gridcolor=COLOR_GRID, showgrid=True),
        yaxis=dict(title=''), height=480, bargap=0.2)
    st.plotly_chart(fig_hd, width='stretch')

    st.markdown("---")

    # ======================================================================
    # SECTION 3: Victim Analysis
    # ======================================================================
    st.markdown('<p class="story-question"><span class="section-num">3</span>'
                'Phân tích Nạn nhân: Ai là đối tượng bị hại nhiều nhất?</p>',
                unsafe_allow_html=True)

    st.markdown(f"""
    <div class="story-insight">
        📌 <b>Insight:</b> Trong tổng số <b>{total_victims:,}</b> nạn nhân được ghi nhận:
        Nam giới chiếm <b>{total_male_v/total_victims*100:.1f}%</b>,
        Nữ giới chiếm <b>{total_female_v/total_victims*100:.1f}%</b>,
        và Trẻ em chiếm <b>{total_minor_v/total_victims*100:.1f}%</b>.
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["👨‍👩‍👧‍👦 Theo loại tội", "📊 Tổng quan giới tính"])

    with tabs[0]:
        fig_victim = go.Figure()
        for col, color, label in [('Male', '#1b9aaa', 'Nam'), ('Female', '#f4a261', 'Nữ'), ('Minor', '#e63946', 'Trẻ em')]:
            fig_victim.add_trace(go.Bar(
                name=label, y=victim_by_crime.index, x=victim_by_crime[col],
                orientation='h', marker_color=color,
                hovertemplate=f'<b>{label}</b><br>Loại tội: %{{y}}<br>Số nạn nhân: %{{x:,}}<extra></extra>',
            ))
        fig_victim.update_layout(**common_layout, barmode='stack',
            title=dict(text='Phân bố Nạn nhân theo Loại tội & Giới tính', font=dict(size=17, color='#1b2838')),
            xaxis=dict(title='Số nạn nhân', gridcolor=COLOR_GRID, showgrid=True),
            yaxis=dict(title=''),
            legend=dict(orientation='h', yanchor='bottom', y=-0.25, xanchor='center', x=0.5),
            height=480, bargap=0.2)
        st.plotly_chart(fig_victim, width='stretch')

    with tabs[1]:
        fig_donut = go.Figure(data=[go.Pie(
            labels=['Nam giới', 'Nữ giới', 'Trẻ em'],
            values=[total_male_v, total_female_v, total_minor_v],
            hole=0.5,
            marker=dict(colors=['#1b9aaa', '#f4a261', '#e63946']),
            textinfo='label+percent', textfont=dict(size=14),
            hovertemplate='<b>%{label}</b><br>Số nạn nhân: %{value:,}<br>Tỷ lệ: %{percent}<extra></extra>',
        )])
        fig_donut.update_layout(**common_layout,
            title=dict(text='Tỷ lệ Nạn nhân theo Giới tính & Tuổi', font=dict(size=17, color='#1b2838')),
            height=420,
            annotations=[dict(text=f'{total_victims:,}<br>Nạn nhân', x=0.5, y=0.5,
                              font_size=16, showarrow=False, font_color='#1b2838')])
        st.plotly_chart(fig_donut, width='stretch')

    st.markdown("---")

    # ======================================================================
    # SECTION 4: Detection Rate by Crime Category
    # ======================================================================
    st.markdown('<p class="story-question"><span class="section-num">4</span>'
                'Loại tội phạm nào khó phá án nhất?</p>', unsafe_allow_html=True)

    hardest = crime_undetect_rate.index[0]
    easiest = crime_undetect_rate.index[-1]

    st.markdown(f"""
    <div class="story-insight">
        📌 <b>Insight:</b> Loại tội khó phá nhất là <b>"{hardest}"</b> với tỷ lệ chưa phá án lên đến
        <b>{crime_undetect_rate.iloc[0]:.1f}%</b>. Ngược lại, <b>"{easiest}"</b> có tỷ lệ phá án cao nhất.
        Điều này giúp cơ quan chức năng biết cần đầu tư nguồn lực điều tra vào đâu.
    </div>
    """, unsafe_allow_html=True)

    top_crimes = crime_total.nlargest(12).index
    fig_rate = go.Figure()
    fig_rate.add_trace(go.Bar(
        name='Tỷ lệ Kết án (%)', x=top_crimes,
        y=[crime_conv_rate_series.get(c, 0) for c in top_crimes],
        marker_color='#06d6a0',
        hovertemplate='<b>%{x}</b><br>Tỷ lệ kết án: %{y:.1f}%<extra></extra>',
    ))
    fig_rate.add_trace(go.Bar(
        name='Tỷ lệ Chưa phá (%)', x=top_crimes,
        y=[crime_undetect_rate.get(c, 0) for c in top_crimes],
        marker_color='#e63946',
        hovertemplate='<b>%{x}</b><br>Tỷ lệ chưa phá: %{y:.1f}%<extra></extra>',
    ))
    fig_rate.update_layout(**common_layout, barmode='group',
        title=dict(text='Tỷ lệ Kết án vs Chưa phá án theo Loại tội (Top 12)', font=dict(size=17, color='#1b2838')),
        xaxis=dict(title='Loại tội', gridcolor=COLOR_GRID, tickangle=-30),
        yaxis=dict(title='Tỷ lệ (%)', gridcolor=COLOR_GRID, showgrid=True),
        legend=dict(orientation='h', yanchor='bottom', y=-0.35, xanchor='center', x=0.5),
        height=500, bargap=0.15)
    st.plotly_chart(fig_rate, width='stretch')

    st.markdown("---")

    # ======================================================================
    # SECTION 5: Complaint Mode Analysis
    # ======================================================================
    st.markdown('<p class="story-question"><span class="section-num">5</span>'
                'Tội phạm được phát hiện qua hình thức nào?</p>', unsafe_allow_html=True)

    top_mode = mode_counts.index[0]

    st.markdown(f"""
    <div class="story-insight">
        📌 <b>Insight:</b> Hình thức phát hiện tội phạm phổ biến nhất là <b>"{top_mode}"</b>
        ({mode_counts.iloc[0]:,} vụ, chiếm {mode_counts.iloc[0]/total*100:.1f}%).
        Đây là thông tin hữu ích để đánh giá hiệu quả tuần tra chủ động của cảnh sát
        so với tố giác từ dân.
    </div>
    """, unsafe_allow_html=True)

    fig_mode = go.Figure(data=[go.Bar(
        x=mode_counts.index, y=mode_counts.values,
        marker=dict(color=crime_palette[:len(mode_counts)]),
        text=[f"{v:,}<br>({v/total*100:.1f}%)" for v in mode_counts.values],
        textposition='outside', textfont=dict(size=12, color='#555'),
        hovertemplate='<b>%{x}</b><br>Số vụ: %{y:,}<extra></extra>',
    )])
    fig_mode.update_layout(**common_layout,
        title=dict(text='Hình thức Phát hiện / Tiếp nhận Tội phạm', font=dict(size=17, color='#1b2838')),
        xaxis=dict(title='Hình thức', gridcolor=COLOR_GRID),
        yaxis=dict(title='Số vụ', gridcolor=COLOR_GRID, showgrid=True),
        height=420, bargap=0.3)
    st.plotly_chart(fig_mode, width='stretch')

    st.markdown("---")

    # ======================================================================
    # CONCLUSION
    # ======================================================================
    st.markdown("### 🎯 Kết luận & Khuyến nghị")
    st.markdown(f"""
    Từ phân tích **{total:,}** hồ sơ FIR tại Karnataka:

    1. **Tỷ lệ kết án toàn bang:** **{conv_rate:.1f}%** — vẫn còn dư địa cải thiện đáng kể.
    2. **Chênh lệch giữa các quận:** Quận tốt nhất ({best_dist}) kết án cao hơn rất nhiều so với quận thấp nhất ({worst_dist}).
    3. **Nạn nhân nữ và trẻ em** tập trung ở nhóm tội Crimes Against Women và POCSO.
    4. **Loại tội khó phá nhất:** "{hardest}" — cần tăng cường đội ngũ điều tra chuyên biệt.
    5. **Phương thức phát hiện:** Đa số vụ án qua hình thức "{top_mode}".

    > 💡 *Module này bổ sung góc nhìn "hậu phạm tội" — giúp đánh giá hiệu quả hệ thống tư pháp,
    > kết hợp với Crime Pattern (phát hiện) và Resource Allocation (phân bổ) để tạo vòng phản hồi hoàn chỉnh.*
    """)

