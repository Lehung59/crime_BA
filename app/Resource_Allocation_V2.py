import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pulp import LpVariable, LpProblem, LpMaximize, lpSum

# Define Crime Categories Mapping Hardcoded
TECH_CRIMES = [
    'CYBER CRIME', 'FORGERY', 'CHEATING', 'COUNTERFEITING', 
    'CRIMINAL BREACH OF TRUST', 'FALSE EVIDENCE', 
    'Concealment of birth by secret disposal of Child', 
    'Disobedience to Order Promulgated by PublicServan', 
    'ELECTION', 'OFFENCES AGAINST PUBLIC SERVANTS (Public servant is a victim)', 
    'SCHEDULED CASTE AND THE SCHEDULED TRIBES ', 'CONSUMER', 
    'BONDED LABOUR SYSTEM', 'ANTIQUES (CULTURAL PROPERTY)'
]

PATROL_CRIMES = [
    'THEFT', 'ROBBERY', 'BURGLARY - NIGHT', 'BURGLARY - DAY', 'DACOITY', 
    'MOTOR VEHICLE ACCIDENTS FATAL', 'MOTOR VEHICLE ACCIDENTS NON-FATAL', 
    'CRIMINAL TRESPASS', 'MISCHIEF', 'ARSON', 'EXPLOSIVES', 
    ' PREVENTION OF DAMAGE TO PUBLIC PROPERTY ACT 1984', 'RIOTS'
]

# ======================================================================
# THUẬT TOÁN TỐI ƯU HÓA V2
# ======================================================================
def optimise_resource_allocation_v2(district_df, sanctioned_asi, sanctioned_chc, sanctioned_cpc):
    """
    Giải bài toán Linear Programming để phân bổ quân số tối ưu V2.
    Sử dụng Trọng số Loại tội phạm (ASI_Weight, CHC_Weight, CPC_Weight) để điều chỉnh giới hạn trần phân bổ.
    """
    problem = LpProblem("Phan_Bo_Nguon_Luc_V2", LpMaximize)

    asi_vars = LpVariable.dicts("ASI", district_df.index, lowBound=0, cat='Integer')
    chc_vars = LpVariable.dicts("CHC", district_df.index, lowBound=0, cat='Integer')
    cpc_vars = LpVariable.dicts("CPC", district_df.index, lowBound=0, cat='Integer')

    # Hàm mục tiêu có xét Trọng số loại tội phạm
    problem += lpSum(
        district_df.loc[i, 'Normalised Crime Severity'] * (
            district_df.loc[i, 'ASI_Weight'] * asi_vars[i] +
            district_df.loc[i, 'CHC_Weight'] * chc_vars[i] +
            district_df.loc[i, 'CPC_Weight'] * cpc_vars[i]
        )
        for i in district_df.index
    )

    # Ràng buộc biên chế
    problem += lpSum(asi_vars[i] for i in district_df.index) <= sanctioned_asi
    problem += lpSum(chc_vars[i] for i in district_df.index) <= sanctioned_chc
    problem += lpSum(cpc_vars[i] for i in district_df.index) <= sanctioned_cpc

    # Mỗi tuyến ít nhất 1 cảnh sát
    for i in district_df.index:
        problem += asi_vars[i] + chc_vars[i] + cpc_vars[i] >= 1

    # Ràng buộc tối đa theo Trọng số tội phạm
    # Nhân với 3 vì trung bình mỗi weight là 1/3, giữ nguyên scale trần của hàm V1
    for i in district_df.index:
        problem += asi_vars[i] <= max(1.0, sanctioned_asi * district_df.loc[i, 'Normalised Crime Severity'] * district_df.loc[i, 'ASI_Weight'] * 3.0)
        problem += chc_vars[i] <= max(1.0, sanctioned_chc * district_df.loc[i, 'Normalised Crime Severity'] * district_df.loc[i, 'CHC_Weight'] * 3.0)
        problem += cpc_vars[i] <= max(1.0, sanctioned_cpc * district_df.loc[i, 'Normalised Crime Severity'] * district_df.loc[i, 'CPC_Weight'] * 3.0)

    with st.spinner("Đang tính toán phân bổ tối ưu bằng Linear Programming (V2)..."):
        problem.solve()

    result_df = district_df.copy()
    result_df['Allocated ASI'] = [asi_vars[i].varValue for i in result_df.index]
    result_df['Allocated CHC'] = [chc_vars[i].varValue for i in result_df.index]
    result_df['Allocated CPC'] = [cpc_vars[i].varValue for i in result_df.index]
    
    cols = ['Allocated ASI', 'Allocated CHC', 'Allocated CPC']
    result_df[cols] = result_df[cols].apply(np.round).astype(int)
    result_df['Tổng phân bổ'] = result_df[cols].sum(axis=1)

    return result_df


# ======================================================================
# HIỂN THỊ KẾT QUẢ V2
# ======================================================================
def allocate_resources_v2(option, district_df, updated_asi, updated_chc, updated_cpc, profiles_df):
    """Chạy tối ưu hóa và hiển thị kết quả Trực quan V2."""
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f0f4f8, #e2eaf2);
                border-left: 4px solid #06d6a0; border-radius: 8px;
                padding: 0.9rem 1.2rem; margin: 0.8rem 0 1rem 0;
                font-size: 0.93rem; color: #2c3e50;">
        <b>Biên chế được duyệt — {option}:</b><br>
        &nbsp;&nbsp;ASI (Trợ lý Thanh tra): <b>{updated_asi}</b> người &nbsp;|&nbsp;
        CHC (Thượng sĩ): <b>{updated_chc}</b> người &nbsp;|&nbsp;
        CPC (Hạ sĩ / Chiến sĩ): <b>{updated_cpc}</b> người<br>
        &nbsp;&nbsp;Tổng biên chế: <b>{updated_asi + updated_chc + updated_cpc}</b> cảnh sát
    </div>
    """, unsafe_allow_html=True)

    # Chạy LP
    result = optimise_resource_allocation_v2(district_df, updated_asi, updated_chc, updated_cpc)
    st.success("Thành công! Phân bổ Nguồn lực V2 (dựa theo Loại Tội phạm) đã hoàn tất.")

    # Số liệu tổng hợp
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tổng ASI phân bổ", f"{int(result['Allocated ASI'].sum()):,}")
    col2.metric("Tổng CHC phân bổ", f"{int(result['Allocated CHC'].sum()):,}")
    col3.metric("Tổng CPC phân bổ", f"{int(result['Allocated CPC'].sum()):,}")
    col4.metric("Số tuyến tuần tra", f"{len(result):,}")

    st.markdown("---")
    st.markdown("#### Bảng kết quả phân bổ chi tiết")

    # Bộ lọc theo đơn vị cảnh sát
    police_units = ["Tất cả"] + list(result["Police Unit"].unique())
    selected_units = st.multiselect(
        "Lọc theo Đơn vị cảnh sát:", police_units, default=["Tất cả"]
    )
    view = result if ("Tất cả" in selected_units or not selected_units) \
        else result[result["Police Unit"].isin(selected_units)]

    st.dataframe(
        view[[
            "Police Unit", "Village Area Name", "Beat Name",
            "Total Crimes per beat", "Normalised Crime Severity",
            "ASI_Weight", "CPC_Weight", "CHC_Weight",
            "Allocated ASI", "Allocated CHC", "Allocated CPC", "Tổng phân bổ",
        ]].rename(columns={
            "Police Unit": "Đồn Cảnh Sát",
            "Village Area Name": "Khu vực",
            "Beat Name": "Tuyến tuần tra",
            "Total Crimes per beat": "Tổng vụ án",
            "Normalised Crime Severity": "Nghiêm trọng (Chuẩn hoá)",
            "ASI_Weight": "Tỷ lệ Án Công Nghệ (ASI)",
            "CPC_Weight": "Tỷ lệ Án Tuần Tra (CPC)",
            "CHC_Weight": "Tỷ lệ Án Khác (CHC)",
            "Allocated ASI": "ASI phân bổ",
            "Allocated CHC": "CHC phân bổ",
            "Allocated CPC": "CPC phân bổ",
        }).reset_index(drop=True),
        width='stretch',
        height=400,
    )
    
    # Vẽ biểu đồ trực quan
    st.markdown("#### Cơ Cấu Loại Tội Phạm Tại Các Đồn Cảnh Sát")
    st.caption("Trọng số (Tỷ lệ %) được sử dụng để định hướng mô hình AI tự thiết lập ưu tiên cơ cấu cấp bậc.")
    
    vis_df = profiles_df.copy()
    if ("Tất cả" not in selected_units and selected_units):
        vis_df = vis_df[vis_df['UnitName'].isin(selected_units)]
    
    # Calculate group counts for charting
    vis_df['Loại Tội Phạm'] = 'Khác (General)'
    vis_df.loc[vis_df['CrimeGroup_Name'].isin(TECH_CRIMES), 'Loại Tội Phạm'] = 'Công nghệ/Phức Tạp (Tech)'
    vis_df.loc[vis_df['CrimeGroup_Name'].isin(PATROL_CRIMES), 'Loại Tội Phạm'] = 'Hiện trường/Tuần tra (Patrol)'
    
    chart_data = vis_df.groupby(['UnitName', 'Loại Tội Phạm']).size().reset_index(name='Số lượng')
    
    fig = px.bar(chart_data, x="UnitName", y="Số lượng", color="Loại Tội Phạm", title="Phân bổ Án theo Đồn",
                 color_discrete_map={
                     'Công nghệ/Phức Tạp (Tech)': '#e63946', 
                     'Hiện trường/Tuần tra (Patrol)': '#1b9aaa', 
                     'Khác (General)': '#f4a261'
                 }, barmode='stack')
    fig.update_layout(xaxis_title="Đồn Cảnh Sát", yaxis_title="Tổng Số Vụ Án", legend_title="Tính chất")
    st.plotly_chart(fig, use_container_width=True)

    st.session_state.v2_default = False
    st.session_state.v2_apply = False


# ======================================================================
# HÀM CHÍNH
# ======================================================================
def resource_allocation_v2(df_resources, df_crimes):
    st.title("Phân bổ Nguồn lực Cảnh sát V2")
    st.markdown(
        "Tối ưu hóa phân bổ ASI, CHC, CPC đến từng tuyến tuần tra "
        "bằng thuật toán **Linear Programming (PuLP)** kết hợp **Trọng Số Phân Loại Tội Phạm**."
    )

    with st.expander("Hướng dẫn sử dụng & Điểm mới của V2"):
        st.markdown("""
        **Sự Khác Biệt Giữa V1 và V2:**
        - **V1:** Chỉ dựa trên mức độ nghiêm trọng chung (`Normalised Crime Severity`).
        - **V2:** Trích xuất chi tiết phân tích từng loại tội phạm (từ Dữ liệu lịch sử), tỷ lệ các nhóm vụ án sẽ định hình cấu trúc nguồn lực.
          - Tội phạm Công Nghệ/Phức Tạp -> Trọng số điều động thêm **ASI**
          - Tội phạm Hiện Trường/Tuần Tra (Trộm cướp, Tai nạn, Đột nhập) -> Trọng số điều động thêm **CPC**
          - Khác (Án phổ thông) -> Trọng số điều động loại trung hoà **CHC**

        1. Chọn quận/huyện cần phân bổ.
        2. Nhấn **Dùng biên chế mặc định** hoặc Tùy chỉnh (±10%) rồi nhấn **Áp dụng**.
        3. Kết quả bảng và biểu đồ sẽ giải thích lý do tại sao AI chọn cách phân phối nhân sự cho đồn đó theo cấu trúc vụ án.
        """)

    st.markdown("---")

    options = ["-- Chọn Quận/Huyện --"] + list(df_resources["District Name"].unique())
    option = st.selectbox("Chọn Quận/Huyện", options, key="v2_selectbox")

    if option == "-- Chọn Quận/Huyện --":
        return

    # Lọc resource
    district_df = df_resources[df_resources["District Name"] == option].copy()
    
    # Lọc profiles crimes theo district selected Units
    police_units = list(district_df["Police Unit"].unique())
    district_crimes = df_crimes[df_crimes['UnitName'].isin(police_units)].copy()
    
    if not district_crimes.empty:
        # Gán Nhóm
        district_crimes['Crime_Category'] = 'General'
        district_crimes.loc[district_crimes['CrimeGroup_Name'].isin(TECH_CRIMES), 'Crime_Category'] = 'Tech'
        district_crimes.loc[district_crimes['CrimeGroup_Name'].isin(PATROL_CRIMES), 'Crime_Category'] = 'Patrol'
        
        # Thống kê tỉ lệ
        crime_stats = district_crimes.groupby(['UnitName', 'Crime_Category']).size().unstack(fill_value=0)
        
        if 'Tech' not in crime_stats: crime_stats['Tech'] = 0
        if 'Patrol' not in crime_stats: crime_stats['Patrol'] = 0
        if 'General' not in crime_stats: crime_stats['General'] = 0
            
        crime_stats['Total'] = crime_stats.sum(axis=1)
        crime_stats['ASI_Weight'] = crime_stats['Tech'] / crime_stats['Total']
        crime_stats['CPC_Weight'] = crime_stats['Patrol'] / crime_stats['Total']
        crime_stats['CHC_Weight'] = crime_stats['General'] / crime_stats['Total']
        
        # Map weights back to district_df
        weights_dict = crime_stats[['ASI_Weight', 'CPC_Weight', 'CHC_Weight']].to_dict('index')
        
        district_df['ASI_Weight'] = district_df['Police Unit'].map(lambda x: weights_dict.get(x, {}).get('ASI_Weight', 0.3333))
        district_df['CPC_Weight'] = district_df['Police Unit'].map(lambda x: weights_dict.get(x, {}).get('CPC_Weight', 0.3333))
        district_df['CHC_Weight'] = district_df['Police Unit'].map(lambda x: weights_dict.get(x, {}).get('CHC_Weight', 0.3333))
    else:
        # Không có dữ liệu chi tiết, dùng default weights
        district_df['ASI_Weight'] = 0.3333
        district_df['CPC_Weight'] = 0.3333
        district_df['CHC_Weight'] = 0.3333

    # Giao diện
    total_beats = len(district_df)
    total_crimes = int(district_df['Total Crimes per beat'].sum())
    st.markdown(
        f"Quận **{option}** có **{total_beats}** tuyến tuần tra, "
        f"tổng cộng **{total_crimes:,}** vụ án (Beat level)."
    )

    default_asi = int(district_df['Sanctioned Strength of Assistant Sub-Inspectors per District'].iloc[0])
    default_chc = int(district_df['Sanctioned Strength of Head Constables per District'].iloc[0])
    default_cpc = int(district_df['Sanctioned Strength of Police Constables per District'].iloc[0])

    st.markdown("#### Điều chỉnh Biên chế (±10% so với mức chuẩn)")
    col1, col2, col3 = st.columns(3)
    with col1:
        sanctioned_asi = st.number_input(
            "ASI - Trợ lý Thanh tra",
            value=default_asi, min_value=int(default_asi * 0.9), max_value=int(default_asi * 1.1),
            step=1, key="asi_v2"
        )
    with col2:
        sanctioned_chc = st.number_input(
            "CHC - Thượng sĩ",
            value=default_chc, min_value=int(default_chc * 0.9), max_value=int(default_chc * 1.1),
            step=1, key="chc_v2"
        )
    with col3:
        sanctioned_cpc = st.number_input(
            "CPC - Hạ sĩ / Chiến sĩ",
            value=default_cpc, min_value=int(default_cpc * 0.9), max_value=int(default_cpc * 1.1),
            step=1, key="cpc_v2"
        )

    if "v2_default" not in st.session_state: st.session_state.v2_default = False
    if "v2_apply" not in st.session_state: st.session_state.v2_apply = False

    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        btn_default = st.button("Dùng biên chế mặc định", key="btn_def_v2", width='stretch')
    with col_btn2:
        btn_apply = st.button("Áp dụng phân bổ (V2)", key="btn_app_v2", width='stretch')

    if (btn_default or st.session_state.v2_default) and not st.session_state.v2_apply:
        st.session_state.v2_apply = False
        st.session_state.v2_default = True
        allocate_resources_v2(option, district_df, default_asi, default_chc, default_cpc, district_crimes)

    if (btn_apply or st.session_state.v2_apply) and not st.session_state.v2_default:
        st.session_state.v2_default = False
        st.session_state.v2_apply = True
        allocate_resources_v2(option, district_df, sanctioned_asi, sanctioned_chc, sanctioned_cpc, district_crimes)
