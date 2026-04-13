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
    data_file_path = os.path.join(root_dir, 'Component_datasets', 'Criminal_Profiling_cleaned.csv')
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
        Đáng chú ý, <b>{young_pct:.1f}%</b> đối tượng dưới 35 tuổi — cho thấy tội phạm tập trung chủ yếu ở nhóm <b>thanh niên và trung niên trẻ</b>.<br><br>
        🤔 <b>Vì sao?</b> Đây là độ tuổi lao động chính, chịu áp lực tài chính lớn sinh ra nhiều biến động tâm lý, cộng đồng này cũng có xung năng và độ bốc đồng cao.<br><br>
        ⚠️ <b>Điểm bất hợp lý:</b> Nhóm cao tuổi (>60) rất thấp nhưng vẫn xuất hiện trong hồ sơ. Đôi khi điều này không phản ánh đúng thủ phạm thực mà họ chỉ đứng ra "nhận tội thay" cho con cháu trong gia tộc để giữ tương lai cho thế hệ trẻ.
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
    st.plotly_chart(fig_age, use_container_width=True)

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
        Dữ liệu cho thấy sự chênh lệch giới tính cực kỳ lớn — gần như toàn bộ hồ sơ là nam giới.<br><br>
        🤔 <b>Vì sao?</b> Nam giới tại xã hội truyền thống tham gia các hoạt động kinh tế ngoài xã hội nhiều hơn và thường có xu hướng giải quyết xung đột bằng bạo lực thể chất.<br><br>
        ⚠️ <b>Hạn chế dữ liệu (Data Bias):</b> Tỷ lệ nữ thấp kỷ lục có thể do cảnh sát có xu hướng bỏ qua vi phạm nhỏ của phụ nữ hoặc chỉ xử lý nội bộ. Phụ nữ cũng thường là đồng phạm ẩn danh không bị lên hồ sơ.
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
    st.plotly_chart(fig_gen, use_container_width=True)

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
        Top 10 đẳng cấp chiếm <b>{top_castes.sum()/caste_counts.sum()*100:.1f}%</b> tổng số.<br><br>
        🤔 <b>Vì sao?</b> Nhiều nhóm đứng dưới thang bậc xã hội phải đối mặt với khó khăn kinh tế, khiến tỷ lệ án trộm cắp mưu sinh và tệ nạn cao hơn.<br><br>
        ⚠️ <b>Điểm bất hợp lý (Profiling Bias):</b> Rất nhiều hồ sơ "unknown". Ngoài ra, số lượng án lớn có thể đến từ việc cảnh sát định kiến và có tần suất tuần tra, kiểm tra gắt gao quá mức tại các khu ổ chuột của các nhóm thiểu số này.
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
    st.plotly_chart(fig_caste, use_container_width=True)

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
        với <b>{occupation_counts.iloc[0]:,}</b> đối tượng. Phần lớn thuộc nhóm lao động phổ thông.<br><br>
        🤔 <b>Vì sao?</b> Nỗi lo cơm áo gạo tiền ở nhóm lao động bấp bênh dễ bị kích phát thành các vụ trộm cướp, bạo động, hoặc ẩu đả nhỏ lẻ khi có các biến cố lạm phát.<br><br>
        ⚠️ <b>Điểm bất hợp lý:</b> Khuyết thiếu hoàn toàn "Tội phạm cổ cồn trắng" (quan chức, doanh nhân lớn). Dữ liệu này chủ yếu phản ánh bề nổi phân khúc "tội phạm đường phố" của cảnh sát cơ sở, bỏ lọt mảng án mưu mô/tài chính cấp cao.
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
    st.plotly_chart(fig_occ, use_container_width=True)

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
        Top 5 loại tội chiếm <b>{top_crime_groups.sum()/Criminal_Profiling['Crime_Group1'].value_counts().sum()*100:.1f}%</b> tổng số vụ.<br><br>
        🤔 <b>Vì sao?</b> Trộm cắp, va chạm giao thông, và xô xát là những rủi ro thường trực và trực diện nhất, bắt nguồn từ thói quen sinh hoạt và di chuyển vùng đô thị.<br><br>
        ⚠️ <b>Sinh cảnh bất hợp lý:</b> Các loại án như đánh bạc (Gambling) hoặc buôn rượu lậu có thể tăng vọt vào dịp nhất định trong năm. Đó thường là hệ quả của áp lực tăng KPI "chiến dịch quét dọn" của cảnh sát chứ không hẳn do trào lưu tội phạm tăng.
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
        st.plotly_chart(fig_cg, use_container_width=True)

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
        st.plotly_chart(fig_ch, use_container_width=True)

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
        với <b>{heatmap_data.loc[max_cell[0], max_cell[1]]:,}</b> vụ. Nhóm <b>25-35 tuổi</b> có mật độ cao nhất ở hầu hết các loại tội.<br><br>
        🤔 <b>Vì sao?</b> Nhóm này di chuyển liên tục, tụ tập uống rượu đi đêm nhiều, hay bị áp lực kinh doanh túng quẫn nên dẫn tới đa dạng các hình thức phạm tội.<br><br>
        ⚠️ <b>Điểm bất hợp lý:</b> Tội phạm vị thành niên hiển thị cường độ khá thấp. Có thể các vụ án liên quan vị thành niên bị gộp chung, hoặc giấu mờ danh tính theo quy định đạo luật bảo vệ quyền trẻ em.
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
    st.plotly_chart(fig_heat, use_container_width=True)

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
        📌 <b>Insight:</b> Đẳng cấp <b>"{top1_caste_6b}"</b> dẫn đầu với <b>{top1_c_count:,}</b> hồ sơ phạm tội.<br><br>
        🤔 <b>Vì sao?</b> Môi trường sống khép kín của từng cộng đồng đặc thù sinh ra các loại hành vi phạm tội có tính lây lan cục bộ (mang tính tổ chức hoặc buôn lậu).<br><br>
        ⚠️ <b>Điểm bất hợp lý:</b> Con số án khổng lồ ở vài nhóm có thể bị độn lên bởi văn hóa bắt người tập thể (Mob Violence). Một cuộc ẩu đả làng xã có thể ghi nhận tới hàng chục, hàng trăm cáo buộc cho cùng một mã án.
    </div>
    """, unsafe_allow_html=True)

    treemap_data = cp_caste.groupby(['Caste', 'Crime_Short']).size().reset_index(name='Count')
    treemap_data = treemap_data.sort_values('Count', ascending=False).groupby('Caste').head(5)

    fig_tree = px.treemap(treemap_data, path=['Caste', 'Crime_Short'], values='Count',
                          color='Count', color_continuous_scale=[[0, '#b5fffc'], [0.5, '#1b9aaa'], [1.0, '#0d1b2a']],
                          title='Treemap: Đẳng cấp → Loại tội phạm')
    fig_tree.update_layout(**common_layout, height=550, title=dict(font=dict(size=17, color='#1b2838')))
    fig_tree.update_traces(hovertemplate='<b>%{label}</b><br>Số vụ: %{value:,}<extra></extra>', textinfo='label+value')
    st.plotly_chart(fig_tree, use_container_width=True)

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
        📌 <b>Insight:</b> Biểu đồ Sunburst cho phép quan sát <b>3 chiều cùng lúc</b>: Giới tính → Nhóm tuổi → Loại tội.<br><br>
        🤔 <b>Vì sao?</b> Nam - trẻ thường gây án bạo lực/đường phố. Nữ giới (nếu bị bắt) thì thường mắc vào các mâu thuẫn gia đình (như của hồi môn bạo lực). Phân tầng rõ rệt thể hiện định kiến phân công lao động.<br><br>
        ⚠️ <b>Điểm bất hợp lý:</b> Dữ liệu bị thắt cổ chai bởi sự áp đảo đến 94% của Nam, khiến trục Nữ giới bị lu mờ hoàn toàn trong các phân tích tương quan tổng quát.
    </div>
    """, unsafe_allow_html=True)

    fig_sun = px.sunburst(sun_data, path=['Sex', 'Age_Group', 'Crime_Short'], values='Count',
                          color='Count', color_continuous_scale=[[0, '#f0fff1'], [0.5, '#06d6a0'], [1.0, '#0d1b2a']],
                          title='Sunburst: Giới tính → Nhóm tuổi → Loại tội')
    fig_sun.update_layout(**common_layout, height=550, title=dict(font=dict(size=17, color='#1b2838')))
    fig_sun.update_traces(hovertemplate='<b>%{label}</b><br>Số vụ: %{value:,}<br>% của nhóm cha: %{percentParent:.1%}<extra></extra>')
    st.plotly_chart(fig_sun, use_container_width=True)

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
        📌 <b>Insight:</b> Mỗi nhóm nghề nghiệp có xu hướng phạm loại tội nào nhiều nhất.<br><br>
        🤔 <b>Vì sao?</b> Nông dân (Farmer) gắn kết chặt với tranh chấp ranh giới đất/trồng trọt. Trong khi dân kinh doanh buôn bán (Business) dễ dính líu lừa đảo công nợ và hình sự hóa quan hệ dân sự.<br><br>
        ⚠️ <b>Điểm bất hợp lý:</b> Nhóm "Unknown" hay "Others" ở nghề nghiệp có thể đang ôm đồm các nhóm lao động tự do không chính quy siêu lớn, làm ẩn đi tính đặc thù sâu xa mà bộ dữ liệu muốn khai thác ban đầu.
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
    st.plotly_chart(fig_stack, use_container_width=True)

    st.markdown("---")

    # ======================================================================
    # SECTION 7: TIME ANALYSIS (YẾU TỐ THỜI GIAN) — ENHANCED
    # ======================================================================
    st.markdown('<p class="story-question"><span class="section-num">7</span>Thời điểm nào trong năm/tháng thường xảy ra nhiều vụ phạm tội nhất?</p>', unsafe_allow_html=True)
    
    time_data_path = os.path.join(root_dir, 'Component_datasets', 'Crime_Pattern_Analysis_Cleaned.csv')
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
            📌 <b>Insight Phân tích Chuyên sâu:</b> Dữ liệu cho thấy số lượng tội phạm đạt đỉnh vào giai đoạn <b>Tháng 2 và Tháng 3</b> (tháng cao điểm nhất ghi nhận <b>{top_month_val:,}</b> vụ). 
            Tại Ấn Độ (đặc biệt là tiểu bang tỷ trọng nông nghiệp cao như Karnataka), đây là thời điểm kết thúc vụ mùa thu hoạch mùa đông (Rabi crop) và bước vào mùa khô hạn, 
            đồng thời 31/3 cũng là thời điểm chốt sổ cuối năm tài chính. 
            <br><br>
            Trong tuần, <b>{busiest_dow}</b> có tần suất tội phạm cao nhất, trong khi <b>{quietest_dow}</b> thấp nhất — cho thấy sự khác biệt rõ rệt giữa ngày thường làm việc và cuối tuần.
        </div>
        """, unsafe_allow_html=True)
        
        # --- 7.0: Key metrics row ---
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("📅 Tháng cao điểm", f"Tháng {top_month}", f"{top_month_val:,} vụ")
        m2.metric("📆 Ngày cao điểm", f"Ngày {top_day}", f"{top_day_val:,} vụ")
        m3.metric("🗓️ Thứ bận nhất", busiest_dow, f"{dow_counts.max():,} vụ")
        m4.metric("🗓️ Thứ thấp nhất", quietest_dow, f"{dow_counts.min():,} vụ")
        
        # --- 7a: Polar Radar — Monthly Seasonality ---
        st.markdown("#### 7a. Tính mùa vụ — Biểu đồ Radar theo Tháng")
        
        month_names_vn = ['Th1', 'Th2', 'Th3', 'Th4', 'Th5', 'Th6', 'Th7', 'Th8', 'Th9', 'Th10', 'Th11', 'Th12']
        
        r1, r2 = st.columns([3, 2])
        with r1:
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=list(month_counts.values) + [month_counts.values[0]],
                theta=month_names_vn + [month_names_vn[0]],
                fill='toself',
                fillcolor='rgba(27, 154, 170, 0.2)',
                line=dict(color='#1b9aaa', width=3),
                marker=dict(size=8, color='#e63946'),
                hovertemplate='<b>%{theta}</b><br>Số vụ: %{r:,}<extra></extra>',
                name='Số vụ phạm tội'
            ))
            fig_radar.update_layout(
                **common_layout,
                polar=dict(
                    radialaxis=dict(visible=True, gridcolor=COLOR_GRID, tickfont=dict(size=10)),
                    angularaxis=dict(tickfont=dict(size=12, color='#1b2838')),
                    bgcolor='rgba(0,0,0,0)',
                ),
                title=dict(text='Radar: Tần suất tội phạm theo Tháng', font=dict(size=17, color='#1b2838')),
                showlegend=False, height=450,
            )
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with r2:
            st.markdown("""
            <div class="story-insight">
                📌 <b>Đọc biểu đồ Radar:</b><br>
                • Các "cánh" <b>dài ra</b> = tháng có tội phạm <b>cao</b><br>
                • Hình dạng <b>không tròn đều</b> cho thấy tội phạm có <b>tính mùa vụ</b> rõ ràng<br>
                • Nếu hình gần tròn → tội phạm phân bố đều quanh năm<br><br>
                <b>🌾 Bối cảnh Karnataka:</b><br>
                • <b>Th1-Th3:</b> Thu hoạch vụ Rabi → tiền mặt lưu thông nhiều → trộm cắp tăng<br>
                • <b>Th3:</b> Chốt sổ năm tài chính (31/3) → giao dịch tài chính dồn dập → lừa đảo tăng<br>
                • <b>Th2-Th3:</b> Lễ hội lớn (Holi, Shivaratri) → di chuyển ồ ạt → tai nạn giao thông tăng<br>
                • <b>Th7-Th8:</b> Mùa mưa (Monsoon) → giảm di chuyển → tội phạm giảm
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # --- 7b: Day of Week × Month Heatmap ---
        st.markdown("#### 7b. Bản đồ nhiệt: Ngày trong tuần × Tháng")
        
        dow_month = pd.crosstab(time_data['DayOfWeek'], time_data['Month'])
        
        st.markdown("""
        <div class="story-insight">
            📌 <b>Insight:</b> Heatmap này cho thấy <b>khi nào chính xác trong tuần và tháng</b> tội phạm tập trung nhất.
            Các ô <b>tối nhất</b> = thời điểm cảnh sát cần tăng cường tuần tra mạnh nhất. Đây là công cụ lập kế hoạch <b>ca trực chiến thuật</b>.
        </div>
        """, unsafe_allow_html=True)
        
        fig_dow_month = go.Figure(data=go.Heatmap(
            z=dow_month.values, 
            x=[f'Th{m}' for m in dow_month.columns],
            y=dow_names,
            colorscale=[[0, '#f0fff1'], [0.25, '#b5fffc'], [0.5, '#41ead4'], [0.75, '#1b9aaa'], [1.0, '#0d1b2a']],
            hovertemplate='<b>%{y}</b> — <b>%{x}</b><br>Số vụ: %{z:,}<extra></extra>',
            colorbar=dict(title=dict(text='Số vụ', font=dict(size=12))),
            text=dow_month.values,
            texttemplate='%{text:,}',
            textfont=dict(size=10),
        ))
        fig_dow_month.update_layout(**common_layout,
            title=dict(text='Heatmap: Ngày trong tuần × Tháng', font=dict(size=17, color='#1b2838')),
            xaxis=dict(title='Tháng', tickmode='linear', side='bottom'),
            yaxis=dict(title='', autorange='reversed'),
            height=380)
        st.plotly_chart(fig_dow_month, use_container_width=True)
        
        st.markdown("---")
        
        # --- 7c: Year-over-Year Trend with Growth Rate ---
        st.markdown("#### 7c. Xu hướng hàng năm & Tốc độ tăng trưởng tội phạm")
        
        yearly_counts = time_data.groupby('Year').size().reset_index(name='Count')
        # Exclude 2024 if data is incomplete
        full_years = yearly_counts[yearly_counts['Year'] < 2024].copy()
        full_years['Growth'] = full_years['Count'].pct_change() * 100
        full_years['Growth_Text'] = full_years['Growth'].apply(
            lambda x: f"+{x:.1f}%" if x > 0 else (f"{x:.1f}%" if pd.notna(x) else "—"))
        
        # Find COVID year
        covid_year = full_years.loc[full_years['Year'] == 2020]
        
        st.markdown(f"""
        <div class="story-insight">
            📌 <b>Insight:</b> Tội phạm giảm mạnh vào năm <b>2019-2020</b> (trùng với giai đoạn lockdown COVID-19), 
            sau đó <b>phục hồi mạnh mẽ từ 2021</b> và đạt đỉnh mới vào <b>2023</b>. Năm 2024 chỉ có dữ liệu một phần nên được loại khỏi phân tích xu hướng.
            {f"Năm 2020 ghi nhận mức giảm <b>{covid_year['Growth'].values[0]:.1f}%</b> — mức giảm lớn nhất trong chuỗi dữ liệu." if len(covid_year) > 0 and pd.notna(covid_year['Growth'].values[0]) else ""}
        </div>
        """, unsafe_allow_html=True)
        
        fig_yoy = go.Figure()
        
        # Bar chart for absolute counts
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
        
        # Line for growth rate on secondary axis
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
        
        fig_yoy.update_layout(**common_layout,
            title=dict(text='Xu hướng Tội phạm Hàng năm (2016-2023)', font=dict(size=17, color='#1b2838')),
            xaxis=dict(title='Năm', tickmode='linear', dtick=1, gridcolor=COLOR_GRID),
            yaxis=dict(title='Số vụ phạm tội', gridcolor=COLOR_GRID, showgrid=True),
            yaxis2=dict(title='% Tăng trưởng', overlaying='y', side='right', 
                       showgrid=False, zeroline=True, zerolinecolor='rgba(244,162,97,0.3)'),
            legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5, font=dict(size=12)),
            height=480, bargap=0.3)
        st.plotly_chart(fig_yoy, use_container_width=True)
        
        st.markdown("---")
        
        # --- 7d: District × Month Heatmap (Geographic Seasonality) ---
        st.markdown("#### 7d. Tính mùa vụ theo địa lý: Quận/Huyện nào nóng vào tháng nào?")
        
        district_month = pd.crosstab(time_data['District_Name'], time_data['Month'])
        # Normalize per district (row-wise %) to show seasonal pattern, not absolute volume
        district_month_pct = district_month.div(district_month.sum(axis=1), axis=0) * 100
        
        st.markdown("""
        <div class="story-insight">
            📌 <b>Insight:</b> Heatmap này được <b>chuẩn hóa theo từng quận</b> (mỗi hàng = 100%) để so sánh <b>mẫu hình mùa vụ</b> 
            giữa các địa phương — cho thấy mỗi quận "nóng" vào thời điểm khác nhau, phục vụ phân bổ nguồn lực <b>luân chuyển theo mùa</b>.
        </div>
        """, unsafe_allow_html=True)
        
        fig_dist_month = go.Figure(data=go.Heatmap(
            z=district_month_pct.values,
            x=[f'Th{m}' for m in district_month_pct.columns],
            y=district_month_pct.index,
            colorscale=[[0, '#f0fff1'], [0.3, '#b5fffc'], [0.5, '#41ead4'], [0.75, '#1b9aaa'], [1.0, '#0d1b2a']],
            hovertemplate='<b>%{y}</b> — <b>%{x}</b><br>Tỷ trọng: %{z:.1f}%<extra></extra>',
            colorbar=dict(title=dict(text='%', font=dict(size=12))),
            text=np.round(district_month_pct.values, 1),
            texttemplate='%{text:.1f}',
            textfont=dict(size=9),
        ))
        fig_dist_month.update_layout(**common_layout,
            title=dict(text='Heatmap: Quận/Huyện × Tháng (chuẩn hóa %)', font=dict(size=17, color='#1b2838')),
            xaxis=dict(title='Tháng', tickmode='linear', side='bottom'),
            yaxis=dict(title='', autorange='reversed'),
            height=max(380, len(district_month_pct) * 30 + 100))
        st.plotly_chart(fig_dist_month, use_container_width=True)
        
        st.markdown("---")
        
        # --- 7e: Monthly Crime Composition — Stacked Area ---
        st.markdown("#### 7e. Cơ cấu loại tội phạm thay đổi như thế nào theo tháng?")
        
        top6_crimes = time_data['CrimeGroup_Name'].value_counts().nlargest(6).index.tolist()
        crime_month_comp = time_data[time_data['CrimeGroup_Name'].isin(top6_crimes)].groupby(
            ['Month', 'CrimeGroup_Name']).size().reset_index(name='Count')
        
        # Calculate share
        total_per_month = crime_month_comp.groupby('Month')['Count'].transform('sum')
        crime_month_comp['Share'] = crime_month_comp['Count'] / total_per_month * 100
        
        st.markdown("""
        <div class="story-insight">
            📌 <b>Insight:</b> Biểu đồ vùng xếp chồng (Stacked Area) cho thấy <b>cơ cấu tội phạm dịch chuyển theo mùa</b>:
            ví dụ, tỷ trọng <b>Tai nạn giao thông</b> tăng vào mùa lễ hội (Th2-3), trong khi <b>Mất tích (Missing Person)</b> 
            có xu hướng ổn định hơn suốt năm. Điều này hỗ trợ cảnh sát bố trí đúng <b>lực lượng chuyên trách</b> cho từng giai đoạn.
        </div>
        """, unsafe_allow_html=True)
        
        area_colors = ['#1b9aaa', '#06d6a0', '#f4a261', '#e63946', '#577590', '#4ecdc4']
        fig_area = go.Figure()
        for i, crime in enumerate(top6_crimes):
            crime_data = crime_month_comp[crime_month_comp['CrimeGroup_Name'] == crime].sort_values('Month')
            base_color = area_colors[i % len(area_colors)]
            if 'rgb' in base_color:
                fill_color = base_color.replace(')', ', 0.7)').replace('rgb', 'rgba')
            else:
                fill_color = f"rgba({int(base_color[1:3], 16)}, {int(base_color[3:5], 16)}, {int(base_color[5:7], 16)}, 0.7)"
            
            fig_area.add_trace(go.Scatter(
                x=crime_data['Month'], y=crime_data['Share'],
                mode='lines', stackgroup='one',
                name=crime[:35],
                line=dict(width=0.5, color=base_color),
                fillcolor=fill_color,
                hovertemplate=f'<b>{crime[:30]}</b><br>Tháng %{{x}}<br>Tỷ trọng: %{{y:.1f}}%<extra></extra>',
            ))
        fig_area.update_layout(**common_layout,
            title=dict(text='Cơ cấu Top 6 loại tội theo Tháng (Stacked Area %)', font=dict(size=17, color='#1b2838')),
            xaxis=dict(title='Tháng', tickmode='linear', tick0=1, dtick=1, gridcolor=COLOR_GRID),
            yaxis=dict(title='Tỷ trọng (%)', gridcolor=COLOR_GRID, showgrid=True, range=[0, 100]),
            legend=dict(orientation='h', yanchor='bottom', y=-0.35, xanchor='center', x=0.5, font=dict(size=10)),
            height=450)
        st.plotly_chart(fig_area, use_container_width=True)
        
        st.markdown("---")
        
        # --- 7f: Day-of-Week Pattern by Crime Type (Grouped Bar) ---
        st.markdown("#### 7f. Loại tội phạm nào có mẫu hình ngày trong tuần đặc biệt?")
        
        top5_crimes_dow = time_data['CrimeGroup_Name'].value_counts().nlargest(5).index.tolist()
        dow_crime = time_data[time_data['CrimeGroup_Name'].isin(top5_crimes_dow)].copy()
        dow_crime_ct = pd.crosstab(dow_crime['CrimeGroup_Name'], dow_crime['DayOfWeek'])
        # Normalize per crime type (row-wise)
        dow_crime_pct = dow_crime_ct.div(dow_crime_ct.sum(axis=1), axis=0) * 100
        
        st.markdown("""
        <div class="story-insight">
            📌 <b>Insight:</b> Mỗi loại tội phạm có <b>nhịp điệu tuần khác nhau</b>. Ví dụ: Tai nạn giao thông thường <b>giảm rõ rệt vào Chủ Nhật</b> 
            (ít xe cộ hơn), trong khi Trộm cắp có thể <b>cao hơn vào cuối tuần</b> (nhà vắng chủ). 
            Nhận diện mẫu hình này giúp bố trí ca trực phù hợp cho từng đội chuyên trách.
        </div>
        """, unsafe_allow_html=True)
        
        fig_dow_crime = go.Figure()
        dow_colors = ['#1b9aaa', '#06d6a0', '#f4a261', '#e63946', '#577590']
        for i, crime in enumerate(dow_crime_pct.index):
            fig_dow_crime.add_trace(go.Bar(
                x=dow_names, y=dow_crime_pct.loc[crime].values,
                name=crime[:30],
                marker_color=dow_colors[i % len(dow_colors)],
                hovertemplate=f'<b>{crime[:30]}</b><br>%{{x}}<br>Tỷ trọng: %{{y:.1f}}%<extra></extra>',
            ))
        fig_dow_crime.update_layout(**common_layout, barmode='group',
            title=dict(text='Phân bố Ngày trong tuần theo Loại tội (chuẩn hóa %)', font=dict(size=17, color='#1b2838')),
            xaxis=dict(title='Ngày trong tuần', gridcolor=COLOR_GRID),
            yaxis=dict(title='Tỷ trọng trong tuần (%)', gridcolor=COLOR_GRID, showgrid=True),
            legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5, font=dict(size=10)),
            height=450, bargap=0.15, bargroupgap=0.05)
        st.plotly_chart(fig_dow_crime, use_container_width=True)
        
        st.markdown("---")
        
        # --- 7g: COVID-19 Impact — Before vs During vs After ---
        st.markdown("#### 7g. Tác động COVID-19 lên xu hướng tội phạm theo tháng")
        
        pre_covid = time_data[time_data['Year'].isin([2018, 2019])].groupby('Month').size() / 2
        during_covid = time_data[time_data['Year'] == 2020].groupby('Month').size()
        post_covid = time_data[time_data['Year'].isin([2022, 2023])].groupby('Month').size() / 2
        
        st.markdown("""
        <div class="story-insight">
            📌 <b>Insight:</b> So sánh <b>trước COVID (2018-2019)</b>, <b>trong COVID (2020)</b> và <b>sau COVID (2022-2023)</b> 
            cho thấy lockdown khiến tội phạm giảm đặc biệt mạnh vào <b>Th4-Th6/2020</b> (giai đoạn phong tỏa nghiêm ngặt nhất). 
            Tuy nhiên, sau dịch, tội phạm không chỉ phục hồi mà còn <b>vượt qua mức trước dịch</b> ở nhiều tháng — 
            phản ánh hiệu ứng "bùng nổ sau kiềm chế" và các áp lực kinh tế hậu đại dịch.
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
        
        # Add lockdown annotation
        fig_covid.add_vrect(x0=3.5, x1=6.5, fillcolor='rgba(230,57,70,0.08)', line_width=0,
                           annotation_text='🔒 Lockdown', annotation_position='top',
                           annotation_font=dict(size=11, color='#e63946'))
        
        fig_covid.update_layout(**common_layout,
            title=dict(text='Tác động COVID-19: So sánh xu hướng tháng (Trước / Trong / Sau)', font=dict(size=17, color='#1b2838')),
            xaxis=dict(title='Tháng', tickmode='linear', tick0=1, dtick=1, gridcolor=COLOR_GRID),
            yaxis=dict(title='Số vụ phạm tội (trung bình/tháng)', gridcolor=COLOR_GRID, showgrid=True),
            legend=dict(orientation='h', yanchor='bottom', y=-0.25, xanchor='center', x=0.5, font=dict(size=12)),
            height=450)
        st.plotly_chart(fig_covid, use_container_width=True)
        
        # --- 7h: Monthly trend line chart + Heatmap (original charts, refined) ---
        st.markdown("---")
        st.markdown("#### 7h. Chi tiết: Biểu đồ đường & Heatmap loại tội theo tháng")
        
        t1, t2 = st.columns(2)
        with t1:
            fig_month = go.Figure()
            fig_month.add_trace(go.Scatter(
                x=month_counts.index, y=month_counts.values, mode='lines+markers',
                line=dict(color='#e63946', width=3),
                marker=dict(size=8, color='#1b9aaa', line=dict(width=2, color='white')),
                fill='tozeroy', fillcolor='rgba(27, 154, 170, 0.1)',
                hovertemplate='Tháng %{x}<br>Số vụ: %{y:,}<extra></extra>',
            ))
            # Mark peak month
            fig_month.add_annotation(x=top_month, y=top_month_val,
                text=f"🔺 Đỉnh: {top_month_val:,}", showarrow=True, arrowhead=2,
                font=dict(size=11, color='#e63946'), bgcolor='rgba(255,255,255,0.8)')
            fig_month.update_layout(**common_layout, 
                title=dict(text="Xu hướng tội phạm theo Tháng", font=dict(size=17, color='#1b2838')),
                xaxis=dict(title="Tháng", tickmode='linear', tick0=1, dtick=1, gridcolor=COLOR_GRID),
                yaxis=dict(title="Số vụ phạm tội", gridcolor=COLOR_GRID), showlegend=False)
            st.plotly_chart(fig_month, use_container_width=True)
            
        with t2:
            fig_day = go.Figure()
            fig_day.add_trace(go.Scatter(
                x=day_counts.index, y=day_counts.values, mode='lines+markers',
                line=dict(color='#1b9aaa', width=3),
                marker=dict(size=6, color='#e63946', line=dict(width=1, color='white')),
                fill='tozeroy', fillcolor='rgba(230, 57, 70, 0.08)',
                hovertemplate='Ngày %{x}<br>Số vụ: %{y:,}<extra></extra>',
            ))
            fig_day.update_layout(**common_layout, 
                title=dict(text="Tần suất tội phạm theo Ngày trong tháng", font=dict(size=17, color='#1b2838')),
                xaxis=dict(title="Ngày", tickmode='linear', tick0=1, dtick=5, gridcolor=COLOR_GRID),
                yaxis=dict(title="Số vụ phạm tội", gridcolor=COLOR_GRID), showlegend=False)
            st.plotly_chart(fig_day, use_container_width=True)
            
        # Heatmap: Crime Group × Month
        top_crimes_time = time_data['CrimeGroup_Name'].value_counts().nlargest(8).index
        heatmap_time = pd.crosstab(time_data[time_data['CrimeGroup_Name'].isin(top_crimes_time)]['CrimeGroup_Name'], time_data['Month'])
        
        fig_time_heat = go.Figure(data=go.Heatmap(
            z=heatmap_time.values, 
            x=[f'Th{m}' for m in heatmap_time.columns], 
            y=heatmap_time.index,
            colorscale=[[0, '#f0fff1'], [0.4, '#41ead4'], [0.7, '#1b9aaa'], [1.0, '#0d1b2a']],
            hovertemplate='<b>%{x}</b> — <b>%{y}</b><br>Số vụ: %{z:,}<extra></extra>',
            colorbar=dict(title=dict(text='Số vụ', font=dict(size=12))),
        ))
        fig_time_heat.update_layout(**common_layout, 
            title=dict(text='Heatmap: Top 8 nhóm tội × Tháng', font=dict(size=17, color='#1b2838')),
            xaxis=dict(title="Tháng", tickmode='linear', dtick=1),
            yaxis=dict(title=""), height=450)
        st.plotly_chart(fig_time_heat, use_container_width=True)

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
    {f'6. **Thời điểm phạm tội**: Tháng {top_month} và ngày {top_day} hàng tháng là các mốc có tần suất cao nhất, cần chú ý tuần tra.' if 'top_month' in locals() else ''}
    
    > 💡 *Các insight trên có thể được sử dụng để xây dựng mô hình dự đoán tái phạm (Recidivism Prediction) 
    > và tối ưu hóa phân bổ nguồn lực cảnh sát (Resource Allocation) — hai module tiếp theo trong hệ thống.*
    """)
