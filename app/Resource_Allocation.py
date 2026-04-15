import os

import numpy as np
import pandas as pd
import streamlit as st
from pulp import LpMaximize, LpProblem, LpVariable, lpSum


DISTRICT_MAPPING = {
    "Bagalkot": "SP, BAGALKOTE",
    "Ballari": "SP, BELLARY",
    "Belagavi City": "COP, BELGAUM CITY",
    "Belagavi Dist": "SP, BELGAUM",
    "Bengaluru City": "COP, BANGALORE CITY",
    "Bengaluru Dist": "SP, BANGALORE",
    "Bidar": "SP, BIDAR",
    "Chamarajanagar": "SP, CHAMARAJANAGARA",
    "Chickballapura": "SP, CHICKBALLAPURA",
    "Chikkamagaluru": "SP, CHICKMAGALURU",
    "Chitradurga": "SP, CHITRADURGA",
    "Dakshina Kannada": "SP, DK, MANGALORE",
    "Davanagere": "SP, DAVANGERE",
    "Dharwad": "SP, DHARWAD",
    "Gadag": "SP, GADAG",
    "Hassan": "SP, HASSAN",
    "Haveri": "SP, HAVERI",
    "Hubballi Dharwad City": "COP, HUBLI-DHARWAD CITY",
    "K.G.F": "SP, KGF",
    "Kalaburagi": "SP, KALABURGI",
    "Kalaburagi City": "COP, KALBURGI CITY",
    "Karnataka Railways": "SP, RAILWAYS",
    "Kodagu": "SP, KODAGU",
    "Kolar": "SP, KOLAR",
    "Koppal": "SP, KOPPAL",
    "Mandya": "SP, MANDYA",
    "Mangaluru City": "COP, MANGALORE CITY",
    "Mysuru City": "COP, MYSORE CITY",
    "Mysuru Dist": "SP, MYSORE",
    "Raichur": "SP, RAICHUR",
    "Ramanagara": "SP, RAMANAGARA",
    "Shivamogga": "SP, SHIVAMOGA",
    "Tumakuru": "SP, TUMKURU",
    "Udupi": "SP, UDUPI",
    "Uttara Kannada": "SP, UK, KARWAR",
    "Vijayanagara": "SP, VIJAYANAGARA",
    "Vijayapur": "SP, VIJAYAPURA",
    "Yadgir": "SP, YADAGIRI",
}

PATROL_CRIME_WEIGHTS = {
    "CASES OF HURT": 5,
    "ASSAULT": 5,
    "AFFRAY": 5,
    "RIOTS": 5,
    "ATTEMPT TO MURDER": 5,
    "MURDER": 5,
    "CULPABLE HOMICIDE NOT AMOUNTING TO MURDER": 5,
    "ATTEMPT TO CULPABLE HOMICIDE NOT AMOUNTING TO MURDER": 5,
    "MOLESTATION": 5,
    "INSULTING MODESTY OF WOMEN (EVE TEASING)": 5,
    "ASSAULT OR USE OF CRIMINAL FORCE TO DISROBE WOMAN": 5,
    "KIDNAPPING AND ABDUCTION": 5,
    "IMMORAL TRAFFIC": 5,
    "NARCOTIC DRUGS & PSHYCOTROPIC SUBSTANCES": 5,
    "ROBBERY": 4,
    "DACOITY": 4,
    "THEFT": 4,
    "BURGLARY - NIGHT": 4,
    "BURGLARY - DAY": 4,
    "CRIMINAL TRESPASS": 4,
    "MISCHIEF": 4,
    "ARSON": 4,
    "PUBLIC SAFETY": 3,
    "PUBLIC NUISANCE": 3,
    "MOTOR VEHICLE ACCIDENTS FATAL": 3,
    "MOTOR VEHICLE ACCIDENTS NON-FATAL": 3,
    "EXPLOSIVES": 3,
    "PREVENTION OF DAMAGE TO PUBLIC PROPERTY ACT 1984": 3,
}

DISPLAY_UPPERCASE_COLUMNS = ["Village Area Name", "Beat Name"]
SEVERITY_WEIGHT = 0.7
VICTIM_WEIGHT = 0.3
VICTIM_SOURCE_LABEL = "Male+Female+Boy+Girl+Age 0"
SCORING_METHODS = {
    "Cách cũ: Chỉ theo mức độ nghiêm trọng": "severity_only",
    "Có victim: Mức độ nghiêm trọng + tổng số nạn nhân": "severity_with_victims",
}


@st.cache_data(show_spinner=False)
def load_patrol_reference_data():
    """Tổng hợp các beat cần tuần tra hiện trường từ dữ liệu FIR gốc."""
    processed_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "processed",
        "Patrol_Reference_Cleaned.csv",
    )
    expected_columns = {
        "District Name",
        "Police Unit",
        "Village Area Name",
        "Beat Name",
        "Patrol Crimes per beat",
        "Patrol Severity per Beat",
        "Total Victims per beat",
        "Victim Source",
    }
    if os.path.exists(processed_path):
        patrol_df = pd.read_csv(processed_path)
        if expected_columns.issubset(patrol_df.columns):
            return patrol_df

    raw_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "raw",
        "FIR_Details_Data.csv",
    )
    usecols = [
        "District_Name",
        "UnitName",
        "Village_Area_Name",
        "Beat_Name",
        "CrimeGroup_Name",
        "Male",
        "Female",
        "Boy",
        "Girl",
        "Age 0",
    ]
    grouped_chunks = []

    for chunk in pd.read_csv(
        raw_path,
        usecols=usecols,
        chunksize=100_000,
        engine="python",
        on_bad_lines="skip",
    ):
        chunk = chunk.dropna(subset=["District_Name", "UnitName", "Village_Area_Name", "Beat_Name", "CrimeGroup_Name"]).copy()
        chunk["CrimeGroup_Name"] = (
            chunk["CrimeGroup_Name"].astype(str).str.strip().str.upper()
        )
        victim_cols = ["Male", "Female", "Boy", "Girl", "Age 0"]
        chunk[victim_cols] = chunk[victim_cols].apply(
            pd.to_numeric, errors="coerce"
        ).fillna(0)
        chunk["Victim_Total"] = chunk[victim_cols].sum(axis=1)
        chunk["District Name"] = chunk["District_Name"].map(DISTRICT_MAPPING)
        chunk = chunk[chunk["District Name"].notna()].copy()
        chunk["Patrol Weight"] = chunk["CrimeGroup_Name"].map(PATROL_CRIME_WEIGHTS)
        chunk = chunk[chunk["Patrol Weight"].notna()].copy()

        if chunk.empty:
            continue

        grouped_chunks.append(
            chunk.groupby(
                ["District Name", "UnitName", "Village_Area_Name", "Beat_Name"],
                as_index=False,
            ).agg(
                Patrol_Crimes=("CrimeGroup_Name", "count"),
                Patrol_Severity=("Patrol Weight", "sum"),
                Patrol_Victims=("Victim_Total", "sum"),
            )
        )

    if not grouped_chunks:
        return pd.DataFrame(
            columns=[
                "District Name",
                "Police Unit",
                "Village Area Name",
                "Beat Name",
                "Patrol Crimes per beat",
                "Patrol Severity per Beat",
                "Total Victims per beat",
                "Victim Source",
            ]
        )

    patrol_df = pd.concat(grouped_chunks, ignore_index=True)
    patrol_df = patrol_df.groupby(
        ["District Name", "UnitName", "Village_Area_Name", "Beat_Name"],
        as_index=False,
    )[["Patrol_Crimes", "Patrol_Severity", "Patrol_Victims"]].sum()

    patrol_df = patrol_df.rename(
        columns={
            "UnitName": "Police Unit",
            "Village_Area_Name": "Village Area Name",
            "Beat_Name": "Beat Name",
            "Patrol_Crimes": "Patrol Crimes per beat",
            "Patrol_Severity": "Patrol Severity per Beat",
            "Patrol_Victims": "Total Victims per beat",
        }
    )
    patrol_df["Victim Source"] = VICTIM_SOURCE_LABEL
    patrol_df.to_csv(processed_path, index=False)
    return patrol_df


def prepare_patrol_district_data(df, option, scoring_mode="severity_only"):
    """Chỉ giữ các beat có tội phạm phù hợp tuần tra thực địa."""
    district_df = df[df["District Name"] == option].copy()
    district_df = district_df.drop(columns=["Total Victims per beat"], errors="ignore")
    patrol_df = load_patrol_reference_data()
    district_patrol_df = patrol_df[patrol_df["District Name"] == option].copy()

    if district_patrol_df.empty:
        return district_df.iloc[0:0].copy()

    merge_keys = ["District Name", "Police Unit", "Village Area Name", "Beat Name"]
    district_df = district_df.merge(
        district_patrol_df[
            merge_keys
            + [
                "Patrol Crimes per beat",
                "Patrol Severity per Beat",
                "Total Victims per beat",
            ]
        ],
        on=merge_keys,
        how="inner",
    )

    if district_df.empty:
        return district_df

    district_df["Total Crimes per beat"] = district_df["Patrol Crimes per beat"]
    total_patrol_severity = district_df["Patrol Severity per Beat"].sum()
    total_patrol_victims = district_df["Total Victims per beat"].sum()

    if total_patrol_severity > 0:
        severity_share = district_df["Patrol Severity per Beat"] / total_patrol_severity
    else:
        severity_share = pd.Series(1 / len(district_df), index=district_df.index)

    if total_patrol_victims > 0:
        victim_share = district_df["Total Victims per beat"] / total_patrol_victims
    else:
        victim_share = pd.Series(0.0, index=district_df.index)

    if scoring_mode == "severity_with_victims":
        district_df["Normalised Crime Severity"] = (
            SEVERITY_WEIGHT * severity_share + VICTIM_WEIGHT * victim_share
        )
    else:
        district_df["Normalised Crime Severity"] = severity_share

    return district_df.drop(columns=["Patrol Severity per Beat"])


def uppercase_display_fields(df):
    formatted_df = df.copy()
    for column in DISPLAY_UPPERCASE_COLUMNS:
        if column in formatted_df.columns:
            formatted_df[column] = formatted_df[column].astype(str).str.strip().str.upper()
    return formatted_df


# ======================================================================
# THUẬT TOÁN TỐI ƯU HÓA
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

    asi_vars = LpVariable.dicts("ASI", district_df.index, lowBound=0, cat="Integer")
    chc_vars = LpVariable.dicts("CHC", district_df.index, lowBound=0, cat="Integer")
    cpc_vars = LpVariable.dicts("CPC", district_df.index, lowBound=0, cat="Integer")

    problem += lpSum(
        district_df.loc[i, "Normalised Crime Severity"]
        * (asi_vars[i] + chc_vars[i] + cpc_vars[i])
        for i in district_df.index
    )

    problem += lpSum(asi_vars[i] for i in district_df.index) <= sanctioned_asi
    problem += lpSum(chc_vars[i] for i in district_df.index) <= sanctioned_chc
    problem += lpSum(cpc_vars[i] for i in district_df.index) <= sanctioned_cpc

    for i in district_df.index:
        problem += asi_vars[i] + chc_vars[i] + cpc_vars[i] >= 1

    for i in district_df.index:
        problem += (
            asi_vars[i]
            <= max(1, sanctioned_asi * district_df.loc[i, "Normalised Crime Severity"])
        )
        problem += (
            chc_vars[i]
            <= max(1, sanctioned_chc * district_df.loc[i, "Normalised Crime Severity"])
        )
        problem += (
            cpc_vars[i]
            <= max(1, sanctioned_cpc * district_df.loc[i, "Normalised Crime Severity"])
        )

    with st.spinner("Đang tính toán kịch bản phân bổ nguồn lực..."):
        problem.solve()

    district_df = district_df.copy()
    district_df["Allocated ASI"] = [asi_vars[i].varValue for i in district_df.index]
    district_df["Allocated CHC"] = [chc_vars[i].varValue for i in district_df.index]
    district_df["Allocated CPC"] = [cpc_vars[i].varValue for i in district_df.index]
    cols = ["Allocated ASI", "Allocated CHC", "Allocated CPC"]
    district_df[cols] = district_df[cols].apply(np.round).astype(int)
    district_df["Tổng phân bổ"] = district_df[cols].sum(axis=1)

    return district_df


# ======================================================================
# HIỂN THỊ KẾT QUẢ
# ======================================================================
def allocate_resources(option, district_df, updated_asi, updated_chc, updated_cpc, score_label):
    """Chạy tối ưu hóa và hiển thị bảng kết quả."""
    st.markdown(
        f"""
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
        """,
        unsafe_allow_html=True,
    )

    result = optimise_resource_allocation(
        district_df, updated_asi, updated_chc, updated_cpc
    )
    st.success("Phân bổ hoàn tất.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tổng ASI phân bổ", f"{int(result['Allocated ASI'].sum()):,}")
    col2.metric("Tổng CHC phân bổ", f"{int(result['Allocated CHC'].sum()):,}")
    col3.metric("Tổng CPC phân bổ", f"{int(result['Allocated CPC'].sum()):,}")
    col4.metric("Điểm tuần tra", f"{len(result):,}")

    st.markdown("---")
    st.markdown("#### Bảng kết quả phân bổ cho các điểm cần tuần tra")

    police_units = ["Tất cả"] + list(result["Police Unit"].unique())
    selected_units = st.multiselect(
        "Lọc theo Đơn vị cảnh sát:", police_units, default=["Tất cả"]
    )
    if "Tất cả" in selected_units and len(selected_units) > 1:
        selected_units = [unit for unit in selected_units if unit != "Tất cả"]

    view = (
        result
        if ("Tất cả" in selected_units or not selected_units)
        else result[result["Police Unit"].isin(selected_units)]
    )
    view = uppercase_display_fields(view)

    st.dataframe(
        view[
            [
                "Police Unit",
                "Village Area Name",
                "Beat Name",
                "Total Crimes per beat",
                "Total Victims per beat",
                "Normalised Crime Severity",
                "Allocated ASI",
                "Allocated CHC",
                "Allocated CPC",
                "Tổng phân bổ",
            ]
        ]
        .rename(
            columns={
                "Police Unit": "Đơn vị cảnh sát",
                "Village Area Name": "Khu vực",
                "Beat Name": "Tuyến tuần tra",
                "Total Crimes per beat": "Số vụ đã xảy ra",
                "Total Victims per beat": "Tổng số nạn nhân",
                "Normalised Crime Severity": score_label,
                "Allocated ASI": "ASI phân bổ",
                "Allocated CHC": "CHC phân bổ",
                "Allocated CPC": "CPC phân bổ",
            }
        )
        .reset_index(drop=True),
        width="stretch",
        height=450,
    )


# ======================================================================
# HÀM CHÍNH
# ======================================================================
def resource_allocation(df):
    st.title("Kịch bản Phân bổ Nguồn lực Cảnh sát")
    st.markdown(
        "So sánh và đề xuất phương án phân bổ ASI, CHC, CPC đến từng tuyến tuần tra "
        "dựa trên mức độ rủi ro và nhu cầu tuần tra thực địa."
    )
    st.caption("Thuật toán tối ưu hóa tuyến tính (PuLP) được dùng như công cụ hỗ trợ ra quyết định ở phía sau.")

    st.markdown("---")

    options = ["-- Chọn Quận/Huyện --"] + list(df["District Name"].unique())
    option = st.selectbox("Chọn Quận/Huyện", options)

    if option == "-- Chọn Quận/Huyện --":
        return

    scoring_choice = st.radio(
        "Chọn cách tính điểm ưu tiên phân bổ",
        list(SCORING_METHODS.keys()),
    )
    scoring_mode = SCORING_METHODS[scoring_choice]

    district_df = prepare_patrol_district_data(df, option, scoring_mode=scoring_mode)
    if district_df.empty:
        st.warning(
            "Không tìm thấy điểm tuần tra thực địa phù hợp trong quận/huyện này "
            "(đã loại trừ cyber, tài chính/gian lận và các nhóm tội không phù hợp tuần tra hiện trường)."
        )
        return

    total_beats = len(district_df)
    total_crimes = int(district_df["Total Crimes per beat"].sum())
    st.markdown(
        f"Quận **{option}** có **{total_beats}** điểm cần tuần tra thực địa, "
        f"tổng cộng **{total_crimes:,}** vụ phù hợp tuần tra."
    )
    st.caption(
        "Chỉ giữ các vị trí có tội phạm hiện trường như đánh nhau, gây rối, trộm cắp, cướp, "
        "tai nạn, tệ nạn; loại trừ cyber, gian lận tài chính, giả mạo và các vụ không phù hợp tuần tra."
    )
    if scoring_mode == "severity_with_victims":
        st.caption(
            "Chế độ hiện tại dùng điểm ưu tiên tổng hợp: 70% mức độ nghiêm trọng của loại tội và 30% tổng số nạn nhân tại beat."
        )
        score_label = "Điểm ưu tiên (severity + victim)"
    else:
        st.caption(
            "Chế độ hiện tại dùng cách cũ: chỉ phân bổ theo mức độ nghiêm trọng của loại tội tại beat, chưa tính victim."
        )
        score_label = "Điểm ưu tiên (cách cũ)"

    default_asi = int(
        district_df[
            "Sanctioned Strength of Assistant Sub-Inspectors per District"
        ].iloc[0]
    )
    default_chc = int(
        district_df["Sanctioned Strength of Head Constables per District"].iloc[0]
    )
    default_cpc = int(
        district_df["Sanctioned Strength of Police Constables per District"].iloc[0]
    )

    st.markdown("#### Điều chỉnh Biên chế (±10% so với mức được duyệt)")
    col1, col2, col3 = st.columns(3)
    with col1:
        sanctioned_asi = st.number_input(
            "ASI - Trợ lý Thanh tra",
            value=default_asi,
            min_value=int(default_asi * 0.9),
            max_value=int(default_asi * 1.1),
            step=1,
        )
    with col2:
        sanctioned_chc = st.number_input(
            "CHC - Thượng sĩ",
            value=default_chc,
            min_value=int(default_chc * 0.9),
            max_value=int(default_chc * 1.1),
            step=1,
        )
    with col3:
        sanctioned_cpc = st.number_input(
            "CPC - Hạ sĩ / Chiến sĩ",
            value=default_cpc,
            min_value=int(default_cpc * 0.9),
            max_value=int(default_cpc * 1.1),
            step=1,
        )

    if "default" not in st.session_state:
        st.session_state.default = False
    if "apply" not in st.session_state:
        st.session_state.apply = False

    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        default = st.button("Dùng biên chế mặc định", width="stretch")
    with col_btn2:
        apply = st.button("Áp dụng biên chế tùy chỉnh", width="stretch")

    if (default or st.session_state.default) and not st.session_state.apply:
        st.session_state.apply = False
        st.session_state.default = True
        allocate_resources(option, district_df, default_asi, default_chc, default_cpc, score_label)

    if (apply or st.session_state.apply) and not st.session_state.default:
        st.session_state.default = False
        st.session_state.apply = True
        allocate_resources(
            option,
            district_df,
            sanctioned_asi,
            sanctioned_chc,
            sanctioned_cpc,
            score_label,
        )
