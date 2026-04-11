import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# Determine the root directory of the project
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


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

    st.title("👤 Criminal Profiling — Data Story")
    st.markdown("> *Phân tích đặc điểm nhân khẩu học của đối tượng phạm tội tại Karnataka, Ấn Độ — "
                "dựa trên dữ liệu từ Cảnh sát Bang Karnataka (KSP).*")
    
    total_records = len(Criminal_Profiling)
    n_castes = Criminal_Profiling['Caste'].nunique() if 'Caste' in Criminal_Profiling.columns else 0
    n_crimes = Criminal_Profiling['Crime_Group1'].nunique() if 'Crime_Group1' in Criminal_Profiling.columns else 0

    m1, m2, m3 = st.columns(3)
    m1.metric("📋 Tổng hồ sơ", f"{total_records:,}")
    m2.metric("🏷️ Số nhóm đẳng cấp", f"{n_castes}")
    m3.metric("📂 Loại tội phạm", f"{n_crimes}")

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
        📌 <b>Insight:</b> Tuổi trung bình của đối tượng phạm tội là <b>{age_mean:.1f} tuổi</b> (trung vị: {age_median:.0f}). 
        Đáng chú ý, <b>{young_pct:.1f}%</b> đối tượng dưới 35 tuổi — cho thấy tội phạm tập trung chủ yếu ở nhóm <b>thanh niên và trung niên trẻ</b>.
        Đây là thông tin quan trọng để xây dựng chính sách phòng chống tội phạm hướng đến nhóm tuổi lao động.
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
    col1.metric("👥 Tổng", f"{len(age_data):,}")
    col2.metric("📍 Trung bình", f"{age_mean:.1f}")
    col3.metric("📍 Trung vị", f"{age_median:.0f}")
    col4.metric("📏 Độ lệch chuẩn", f"{age_data.std():.1f}")

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
        📌 <b>Insight:</b> <b>{dominant_pct:.1f}%</b> đối tượng phạm tội là <b>{dominant_gender}</b>. 
        Dữ liệu cho thấy sự chênh lệch giới tính cực kỳ lớn — gần như toàn bộ hồ sơ là nam giới.
        Tuy nhiên, cần lưu ý rằng điều này phản ánh dữ liệu ghi nhận của cảnh sát, không hoàn toàn đại diện cho thực tế.
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
        📌 <b>Insight:</b> Đẳng cấp <b>"{top1_caste}"</b> chiếm <b>{top1_pct:.1f}%</b> trong tổng số hồ sơ có ghi nhận đẳng cấp.
        Top 10 đẳng cấp chiếm <b>{top_castes.sum()/caste_counts.sum()*100:.1f}%</b> tổng số — cho thấy sự tập trung cao ở một số nhóm xã hội nhất định.
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
    # SECTION 4: OCCUPATION ANALYSIS
    # ======================================================================
    st.markdown('<p class="story-question"><span class="section-num">4</span>Đối tượng phạm tội làm nghề gì?</p>', unsafe_allow_html=True)

    occupation_counts = Criminal_Profiling[
        (Criminal_Profiling['Occupation'] != "unknown") &
        (Criminal_Profiling['Occupation'] != "Others PI Specify")
    ]['Occupation'].value_counts()
    top_occs = occupation_counts.sort_values(ascending=True)[-10:]
    top1_occ = occupation_counts.index[0]

    st.markdown(f"""
    <div class="story-insight">
        📌 <b>Insight:</b> Nghề nghiệp phổ biến nhất trong hồ sơ tội phạm là <b>"{top1_occ}"</b> 
        với <b>{occupation_counts.iloc[0]:,}</b> đối tượng. Nhiều đối tượng thuộc nhóm lao động phổ thông, 
        cho thấy mối tương quan giữa <b>điều kiện kinh tế</b> và hành vi phạm tội.
    </div>
    """, unsafe_allow_html=True)

    occ_colors = [f'rgba(6, 214, 160, {0.35 + 0.065*i})' for i in range(len(top_occs))]
    fig_occ = go.Figure(data=[go.Bar(
        x=top_occs.values, y=top_occs.index, orientation='h',
        marker=dict(color=occ_colors, line=dict(color='rgba(255,255,255,0.4)', width=1)),
        hovertemplate='<b>%{y}</b><br>Count: %{x:,}<extra></extra>',
        text=top_occs.values, textposition='outside', textfont=dict(size=11, color='#555'),
    )])
    fig_occ.update_layout(**common_layout,
        title=dict(text='Top 10 Nghề nghiệp liên quan đến Tội phạm', font=dict(size=18, color='#1b2838')),
        xaxis=dict(title='Số lượng', gridcolor=COLOR_GRID, showgrid=True),
        yaxis=dict(title='', gridcolor=COLOR_GRID), bargap=0.25, height=450)
    st.plotly_chart(fig_occ, width='stretch')

    st.markdown("---")

    # ======================================================================
    # SECTION 5: CRIME CATEGORIES
    # ======================================================================
    st.markdown('<p class="story-question"><span class="section-num">5</span>Loại tội phạm nào phổ biến nhất?</p>', unsafe_allow_html=True)

    top_crime_groups = Criminal_Profiling['Crime_Group1'].value_counts().nlargest(5)
    top_crime_heads = Criminal_Profiling['Crime_Head2'].value_counts().nlargest(5)
    top1_crime = top_crime_groups.index[0]

    st.markdown(f"""
    <div class="story-insight">
        📌 <b>Insight:</b> Loại tội phạm phổ biến nhất là <b>"{top1_crime}"</b> với <b>{top_crime_groups.iloc[0]:,}</b> vụ.
        Top 5 loại tội chiếm <b>{top_crime_groups.sum()/Criminal_Profiling['Crime_Group1'].value_counts().sum()*100:.1f}%</b> tổng số vụ phạm tội.
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["📁 Nhóm tội chính", "📂 Phân loại nhỏ"])

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
    # SECTION 6: CORRELATION & RELATIONSHIP ANALYSIS (4 charts)
    # ======================================================================
    st.markdown('<p class="story-question"><span class="section-num">6</span>Các yếu tố nhân khẩu học có mối tương quan nào với loại tội phạm?</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="story-insight">
        📌 Phần này khám phá <b>mối quan hệ chéo</b> giữa các biến: tuổi, giới tính, nghề nghiệp, quận/huyện và loại tội phạm.
        Mỗi biểu đồ trả lời một câu hỏi phân tích cụ thể.
    </div>
    """, unsafe_allow_html=True)

    # --- 6a: Age Group vs Crime Type Heatmap ---
    st.markdown("#### 6a. Nhóm tuổi nào liên quan đến loại tội phạm nào nhiều nhất?")

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
        📌 <b>Insight:</b> Ô nóng nhất là nhóm tuổi <b>{max_cell[0]}</b> × loại tội <b>"{max_cell[1]}"</b> 
        với <b>{heatmap_data.loc[max_cell[0], max_cell[1]]:,}</b> vụ. Nhóm <b>25-35 tuổi</b> có mật đo cao nhất ở hầu hết các loại tội.
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

    # --- 6b: Caste-Crime Treemap ---
    st.markdown("#### 6b. Đẳng cấp nào liên quan đến loại tội phạm nào?")

    cp_caste = Criminal_Profiling[Criminal_Profiling['Caste'] != 'unknown'].copy()
    top8_castes = cp_caste['Caste'].value_counts().nlargest(8).index.tolist()
    cp_caste = cp_caste[cp_caste['Caste'].isin(top8_castes)]
    cp_caste['Crime_Short'] = cp_caste['Crime_Group1'].str[:30]
    top1_caste_6b = top8_castes[0]
    top1_c_count = cp_caste[cp_caste['Caste'] == top1_caste_6b].shape[0]

    st.markdown(f"""
    <div class="story-insight">
        📌 <b>Insight:</b> Đẳng cấp <b>"{top1_caste_6b}"</b> dẫn đầu với <b>{top1_c_count:,}</b> hồ sơ phạm tội.
        Click vào Treemap để xem chi tiết loại tội phạm ở mỗi nhóm đẳng cấp.
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

    # --- 6c: Age-Gender-Crime Sunburst ---
    st.markdown("#### 6c. Mối quan hệ đa chiều: Giới tính → Tuổi → Loại tội?")

    cp_sun = Criminal_Profiling.copy()
    cp_sun['Age_Group'] = pd.cut(cp_sun['age'], bins=[0, 25, 40, 60, 100],
                                 labels=['Trẻ (<25)', 'Trưởng thành (25-40)', 'Trung niên (40-60)', 'Cao tuổi (60+)'])
    top5_crimes_sun = cp_sun['Crime_Group1'].value_counts().nlargest(5).index.tolist()
    cp_sun = cp_sun[cp_sun['Crime_Group1'].isin(top5_crimes_sun)]
    cp_sun['Crime_Short'] = cp_sun['Crime_Group1'].str[:25]
    sun_data = cp_sun.groupby(['Sex', 'Age_Group', 'Crime_Short']).size().reset_index(name='Count')

    st.markdown("""
    <div class="story-insight">
        📌 <b>Insight:</b> Biểu đồ Sunburst cho phép quan sát <b>3 chiều cùng lúc</b>: Giới tính (vòng trong) 
        → Nhóm tuổi (vòng giữa) → Loại tội (vòng ngoài). Click để phóng to từng lớp.
    </div>
    """, unsafe_allow_html=True)

    fig_sun = px.sunburst(sun_data, path=['Sex', 'Age_Group', 'Crime_Short'], values='Count',
                          color='Count', color_continuous_scale=[[0, '#f0fff1'], [0.5, '#06d6a0'], [1.0, '#0d1b2a']],
                          title='Sunburst: Giới tính → Nhóm tuổi → Loại tội')
    fig_sun.update_layout(**common_layout, height=550, title=dict(font=dict(size=17, color='#1b2838')))
    fig_sun.update_traces(hovertemplate='<b>%{label}</b><br>Số vụ: %{value:,}<br>% của nhóm cha: %{percentParent:.1%}<extra></extra>')
    st.plotly_chart(fig_sun, width='stretch')

    st.markdown("---")

    # --- 6d: Occupation vs Crime Group (Stacked Bar) ---
    st.markdown("#### 6d. Mối liên hệ giữa nghề nghiệp và loại hình tội phạm?")

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
        📌 <b>Insight:</b> Biểu đồ Stacked Bar cho thấy mỗi nhóm nghề nghiệp có xu hướng phạm loại tội nào nhiều nhất.
        Sự khác biệt trong cấu phần màu sắc giữa các nghề cho thấy <b>hành vi phạm tội có liên hệ với bối cảnh xã hội-kinh tế</b>.
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
    # CONCLUSION
    # ======================================================================
    st.markdown("### 🎯 Kết luận & Khuyến nghị")
    st.markdown(f"""
    Từ việc phân tích **{total_records:,}** hồ sơ tội phạm tại Karnataka, chúng tôi rút ra các kết luận chính:
    
    1. **Nhóm tuổi rủi ro cao**: Đối tượng phạm tội tập trung mạnh ở độ tuổi **25-35** ({young_pct:.0f}% dưới 35 tuổi).
    2. **Giới tính**: **{dominant_pct:.0f}%** là nam giới — chính sách phòng chống nên tập trung vào nhóm này.
    3. **Yếu tố xã hội**: Đẳng cấp và nghề nghiệp có mối tương quan rõ rệt với tần suất phạm tội.
    4. **Đẳng cấp trọng điểm**: Nhóm đẳng cấp **"{top1_caste}"** có số hồ sơ phạm tội cao nhất.
    5. **Loại tội chủ đạo**: **"{top1_crime}"** chiếm tỷ trọng lớn nhất.
    
    > 💡 *Các insight trên có thể được sử dụng để xây dựng mô hình dự đoán tái phạm (Recidivism Prediction) 
    > và tối ưu hóa phân bổ nguồn lực cảnh sát (Resource Allocation) — hai module tiếp theo trong hệ thống.*
    """)
