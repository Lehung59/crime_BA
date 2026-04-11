import streamlit as st
import pandas as pd
import numpy as np
from pulp import LpVariable, LpProblem, LpMaximize, lpSum


# ======================================================================
# THUẬT TOÁN TỐI ƯU HÓA (giữ nguyên logic LP)
# ======================================================================
def optimise_resource_allocation(district_df, sanctioned_asi, sanctioned_chc, sanctioned_cpc):
    """
    Giải bài toán Linear Programming để phân bổ quân số tối ưu.
    Hàm mục tiêu: Tối đa hóa tổng (Mức độ nghiêm trọng chuẩn hóa × Số cảnh sát phân bổ).
    Ràng buộc:
      - Tổng quân số từng loại không vượt biên chế được duyệt
      - Mỗi tuyến tuần tra có ít nhất 1 cảnh sát
      - Phân bổ per-beat tỉ lệ với mức độ nghiêm trọng tội phạm
    """
    problem = LpProblem("Phan_Bo_Nguon_Luc_Toi_Uu", LpMaximize)

    asi_vars = LpVariable.dicts("ASI", district_df.index, lowBound=0, cat='Integer')
    chc_vars = LpVariable.dicts("CHC", district_df.index, lowBound=0, cat='Integer')
    cpc_vars = LpVariable.dicts("CPC", district_df.index, lowBound=0, cat='Integer')

    # Hàm mục tiêu
    problem += lpSum(
        district_df.loc[i, 'Normalised Crime Severity'] * (asi_vars[i] + chc_vars[i] + cpc_vars[i])
        for i in district_df.index
    )

    # Ràng buộc biên chế
    problem += lpSum(asi_vars[i] for i in district_df.index) <= sanctioned_asi
    problem += lpSum(chc_vars[i] for i in district_df.index) <= sanctioned_chc
    problem += lpSum(cpc_vars[i] for i in district_df.index) <= sanctioned_cpc

    # Mỗi tuyến ít nhất 1 cảnh sát
    for i in district_df.index:
        problem += asi_vars[i] + chc_vars[i] + cpc_vars[i] >= 1

    # Phân bổ tỉ lệ theo mức nghiêm trọng
    for i in district_df.index:
        problem += asi_vars[i] <= max(1, sanctioned_asi * district_df.loc[i, 'Normalised Crime Severity'])
        problem += chc_vars[i] <= max(1, sanctioned_chc * district_df.loc[i, 'Normalised Crime Severity'])
        problem += cpc_vars[i] <= max(1, sanctioned_cpc * district_df.loc[i, 'Normalised Crime Severity'])

    with st.spinner("Đang tính toán phân bổ tối ưu bằng Linear Programming..."):
        problem.solve()

    district_df = district_df.copy()
    district_df['Allocated ASI'] = [asi_vars[i].varValue for i in district_df.index]
    district_df['Allocated CHC'] = [chc_vars[i].varValue for i in district_df.index]
    district_df['Allocated CPC'] = [cpc_vars[i].varValue for i in district_df.index]
    cols = ['Allocated ASI', 'Allocated CHC', 'Allocated CPC']
    district_df[cols] = district_df[cols].apply(np.round).astype(int)
    district_df['Tổng phân bổ'] = district_df[cols].sum(axis=1)

    return district_df


# ======================================================================
# HIỂN THỊ KẾT QUẢ
# ======================================================================
def allocate_resources(option, district_df, updated_asi, updated_chc, updated_cpc):
    """Chạy tối ưu hóa và hiển thị bảng kết quả."""

    # Thông tin biên chế
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f0f4f8, #e2eaf2);
                border-left: 4px solid #1b9aaa; border-radius: 8px;
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
    result = optimise_resource_allocation(district_df, updated_asi, updated_chc, updated_cpc)
    st.success("Phân bổ hoàn tất.")

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
            "Village Area Name", "Beat Name",
            "Total Crimes per beat", "Normalised Crime Severity",
            "Allocated ASI", "Allocated CHC", "Allocated CPC", "Tổng phân bổ",
        ]].rename(columns={
            "Village Area Name": "Khu vực",
            "Beat Name": "Tuyến tuần tra",
            "Total Crimes per beat": "Tổng vụ án",
            "Normalised Crime Severity": "Mức độ nghiêm trọng",
            "Allocated ASI": "ASI phân bổ",
            "Allocated CHC": "CHC phân bổ",
            "Allocated CPC": "CPC phân bổ",
        }).reset_index(drop=True),
        use_container_width=True,
        height=450,
    )

    st.session_state.default = False
    st.session_state.apply = False


# ======================================================================
# HÀM CHÍNH
# ======================================================================
def resource_allocation(df):
    st.title("Phân bổ và Quản lý Nguồn lực Cảnh sát")
    st.markdown(
        "Tối ưu hóa phân bổ ASI, CHC, CPC đến từng tuyến tuần tra "
        "bằng thuật toán Linear Programming (PuLP)."
    )

    with st.expander("Hướng dẫn sử dụng"):
        st.markdown("""
        1. Chọn quận/huyện cần phân bổ nguồn lực.
        2. Điều chỉnh biên chế (±10% so với mức được duyệt) hoặc giữ mặc định.
        3. Nhấn **Dùng biên chế mặc định** hoặc **Áp dụng** để chạy tối ưu hóa.
        4. Xem kết quả trong bảng phân bổ chi tiết.

        **Giải thích cấp bậc:**
        - **ASI** (Assistant Sub-Inspector) — Trợ lý Thanh tra: cấp chỉ huy tuyến cơ sở
        - **CHC** (Head Constable) — Thượng sĩ: cảnh sát có kinh nghiệm
        - **CPC** (Police Constable) — Hạ sĩ / Chiến sĩ: lực lượng tuần tra chính
        """)

    st.markdown("---")

    options = ["-- Chọn Quận/Huyện --"] + list(df["District Name"].unique())
    option = st.selectbox("Chọn Quận/Huyện", options)

    if option == "-- Chọn Quận/Huyện --":
        return

    district_df = df[df["District Name"] == option]
    total_beats = len(district_df)
    total_crimes = int(district_df['Total Crimes per beat'].sum())
    st.markdown(
        f"Quận **{option}** có **{total_beats}** tuyến tuần tra, "
        f"tổng cộng **{total_crimes:,}** vụ án được ghi nhận."
    )

    default_asi = int(district_df['Sanctioned Strength of Assistant Sub-Inspectors per District'].iloc[0])
    default_chc = int(district_df['Sanctioned Strength of Head Constables per District'].iloc[0])
    default_cpc = int(district_df['Sanctioned Strength of Police Constables per District'].iloc[0])

    st.markdown("#### Điều chỉnh Biên chế (±10% so với mức được duyệt)")
    col1, col2, col3 = st.columns(3)
    with col1:
        sanctioned_asi = st.number_input(
            "ASI - Trợ lý Thanh tra",
            value=default_asi,
            min_value=int(default_asi * 0.9),
            max_value=int(default_asi * 1.1),
            step=1
        )
    with col2:
        sanctioned_chc = st.number_input(
            "CHC - Thượng sĩ",
            value=default_chc,
            min_value=int(default_chc * 0.9),
            max_value=int(default_chc * 1.1),
            step=1
        )
    with col3:
        sanctioned_cpc = st.number_input(
            "CPC - Hạ sĩ / Chiến sĩ",
            value=default_cpc,
            min_value=int(default_cpc * 0.9),
            max_value=int(default_cpc * 1.1),
            step=1
        )

    if "default" not in st.session_state:
        st.session_state.default = False
    if "apply" not in st.session_state:
        st.session_state.apply = False

    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        default = st.button("Dùng biên chế mặc định", use_container_width=True)
    with col_btn2:
        apply = st.button("Áp dụng biên chế tùy chỉnh", use_container_width=True)

    if (default or st.session_state.default) and not st.session_state.apply:
        st.session_state.apply = False
        st.session_state.default = True
        allocate_resources(option, district_df, default_asi, default_chc, default_cpc)

    if (apply or st.session_state.apply) and not st.session_state.default:
        st.session_state.default = False
        st.session_state.apply = True
        allocate_resources(option, district_df, sanctioned_asi, sanctioned_chc, sanctioned_cpc)
