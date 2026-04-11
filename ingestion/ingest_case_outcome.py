import pandas as pd
import logging
import sys
import os

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])


def ingest_case_outcome_data():
    """
    Ingest raw FIR data and select relevant columns for Case Outcome analysis.
    
    Columns selected:
    - District_Name: Quận/Huyện xảy ra vụ án
    - UnitName: Đơn vị cảnh sát phụ trách
    - FIR_YEAR, FIR_MONTH: Năm/tháng lập hồ sơ FIR
    - FIR Type: Heinous (Nghiêm trọng) / Non Heinous (Không nghiêm trọng)
    - FIR_Stage: Trạng thái xử lý vụ án (Convicted, Pending Trial, Undetected, ...)
    - Complaint_Mode: Hình thức tiếp nhận (Written, Sue-moto by Police, ...)
    - CrimeGroup_Name: Nhóm tội phạm
    - Male, Female, Boy, Girl, Age 0: Thông tin nạn nhân theo giới tính và tuổi
    - VICTIM COUNT: Tổng số nạn nhân
    - Accused Count: Tổng số bị can
    - Arrested Male, Arrested Female, Arrested Count: Số người bị bắt
    - Accused_ChargeSheeted Count: Số bị can đã bị truy tố
    - Conviction Count: Số vụ kết án thành công
    """

    raw_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'FIR_Details_Data.csv')
    logging.info("Loading raw FIR_Details_Data.csv (~570MB)...")
    
    fir = pd.read_csv(raw_path)
    logging.info(f"Loaded {len(fir):,} rows")

    # Feature selection: lấy các cột phục vụ phân tích kết quả xử lý vụ án
    selected_cols = [
        'District_Name', 'UnitName', 'FIR_YEAR', 'FIR_MONTH',
        'FIR Type', 'FIR_Stage', 'Complaint_Mode',
        'CrimeGroup_Name',
        'Male', 'Female', 'Boy', 'Girl', 'Age 0',
        'VICTIM COUNT', 'Accused Count',
        'Arrested Male', 'Arrested Female', 'Arrested Count\tNo.',
        'Accused_ChargeSheeted Count', 'Conviction Count',
    ]

    raw_data = fir[selected_cols].copy()
    
    # Rename cột bị lỗi tab character trong header gốc
    raw_data = raw_data.rename(columns={'Arrested Count\tNo.': 'Arrested_Count'})

    logging.info(f"Selected {len(selected_cols)} features for Case Outcome Analysis")
    return raw_data
