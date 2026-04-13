import pandas as pd
import numpy as np
import logging
import sys
import os

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])


def clean_case_outcome_data(df):
    """
    Clean và chuẩn hóa dữ liệu FIR cho module Case Outcome Monitoring.
    
    Quy tắc clean tương tự các module khác:
    - Drop duplicates (giống Crime_Pattern_Analysis, Criminal_Profiling)
    - Loại bỏ các hàng CID/ISD/Coastal (giống Resource_Allocation)
    - Chuẩn hóa District_Name (giống Crime_Pattern_Analysis)
    - Chuẩn hóa FIR_Stage vào 5 nhóm chính
    - Tính Victim_Total = Male + Female + Boy + Girl + Age 0
    - Phân loại Crime Category (giống Resource_Allocation)
    """
    
    logging.info(f"Starting cleaning. Input shape: {df.shape}")
    
    # =====================================================
    # 1. Drop duplicates
    # =====================================================
    df.drop_duplicates(inplace=True)
    logging.info(f"After drop_duplicates: {len(df):,} rows")
    
    # =====================================================
    # 2. Loại bỏ các đơn vị đặc biệt không phải quận thực tế
    #    (Tương tự Resource_Allocation/clean_data.py line 8)
    # =====================================================
    exclude_districts = ['CID', 'ISD Bengaluru', 'Coastal Security Police']
    df = df[~df['District_Name'].isin(exclude_districts)]
    logging.info(f"After removing special units: {len(df):,} rows")
    
    # =====================================================
    # 3. Chuẩn hóa District_Name - mapping giống Crime_Pattern_Analysis
    #    (Crime_Pattern_Analysis/clean_data.py line 21-33)
    # =====================================================
    df['District_Name'] = df['District_Name'].replace({
        'Bengaluru City': 'Bengaluru Urban',
        'Belagavi Dist': 'Belagavi',
        'Bengaluru Dist': 'Bengaluru Rural',
        'Bagalkot': 'Bagalkote',
        'Chamarajanagar': 'Chamarajanagara',
        'Belagavi City': 'Belagavi',
        'Chickballapura': 'Chikkaballapura',
        'Mysuru City': 'Mysuru',
        'Vijayanagara': 'Vijayapura',
        'Kalaburagi City': 'Kalaburagi',
        'Hubballi Dharwad City': 'Dharwad',
    })
    logging.info("District names standardized (matching GeoJSON map)")
    
    # =====================================================
    # 4. Chuẩn hóa FIR_Stage vào 5 nhóm chính dễ phân tích
    # =====================================================
    stage_mapping = {
        'Convicted': 'Convicted',           # Kết án thành công
        'Pending Trial': 'Pending Trial',   # Đang chờ xét xử
        'Undetected': 'Undetected',         # Chưa phá được
        'Dis/Acq': 'Discharged/Acquitted',  # Tha bổng / miễn tố
        'Compounded': 'Discharged/Acquitted',
        'BoundOver': 'Discharged/Acquitted',
        'False Case': 'Discharged/Acquitted',
        'Abated': 'Discharged/Acquitted',
        'Other Disposal': 'Other',
        'Traced': 'Other',         # Missing person found
        'Un Traced': 'Undetected', # Missing person not found
    }
    df['FIR_Stage_Clean'] = df['FIR_Stage'].map(stage_mapping).fillna('Other')
    logging.info("FIR_Stage standardized into 5 groups")
    
    # =====================================================
    # 5. Chuẩn hóa FIR Type
    # =====================================================
    df['FIR_Type_Clean'] = df['FIR Type'].apply(
        lambda x: 'Heinous' if str(x).strip() == 'Heinous' else 'Non Heinous'
    )
    
    # =====================================================
    # 6. Tính tổng số nạn nhân thực tế
    #    (Cộng Male + Female + Boy + Girl + Age 0)
    # =====================================================
    victim_cols = ['Male', 'Female', 'Boy', 'Girl', 'Age 0']
    df[victim_cols] = df[victim_cols].fillna(0).astype(int)
    df['Victim_Total'] = df[victim_cols].sum(axis=1)
    
    # Phân loại nạn nhân theo giới và tuổi
    df['Victim_Adult_Male'] = df['Male']
    df['Victim_Adult_Female'] = df['Female']
    df['Victim_Minor'] = df['Boy'] + df['Girl'] + df['Age 0']  # Trẻ em
    
    logging.info("Victim columns computed")
    
    # =====================================================
    # 7. Chuẩn hóa cột số
    # =====================================================
    num_cols = ['Accused Count', 'Arrested_Count',
                'Accused_ChargeSheeted Count', 'Conviction Count']
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(int)
    
    # =====================================================
    # 8. Phân loại Crime Category (giống Resource_Allocation/clean_data.py)
    # =====================================================
    category_mapping = {
        'THEFT': 'Property Crimes',
        'BURGLARY - NIGHT': 'Property Crimes',
        'BURGLARY - DAY': 'Property Crimes',
        'ROBBERY': 'Property Crimes',
        'DACOITY': 'Property Crimes',
        'CRIMINAL BREACH OF TRUST': 'Property Crimes',
        'CHEATING': 'Property Crimes',
        'FORGERY': 'Property Crimes',
        'COUNTERFEITING': 'Property Crimes',
        'CRIMINAL MISAPPROPRIATION ': 'Property Crimes',
        'RECEIVING OF STOLEN PROPERTY': 'Property Crimes',
        'MOTOR VEHICLE ACCIDENTS NON-FATAL': 'Traffic Offenses',
        'MOTOR VEHICLE ACCIDENTS FATAL': 'Traffic Offenses',
        'DEATHS DUE TO RASHNESS/NEGLIGENCE': 'Negligence & Rash Acts',
        'NEGLIGENT ACT': 'Negligence & Rash Acts',
        'PUBLIC SAFETY': 'Public Safety Offenses',
        'PUBLIC NUISANCE': 'Public Safety Offenses',
        'MISSING PERSON': 'Missing Persons',
        ' CYBER CRIME': 'Cybercrime & Fraud',
        'CASES OF HURT': 'Violent Crimes',
        'ATTEMPT TO MURDER': 'Violent Crimes',
        'MURDER': 'Violent Crimes',
        'CULPABLE HOMICIDE NOT AMOUNTING TO MURDER': 'Violent Crimes',
        'ATTEMPT TO CULPABLE HOMICIDE NOT AMOUNTING TO MURDER': 'Violent Crimes',
        'MOLESTATION': 'Crimes Against Women',
        'KIDNAPPING AND ABDUCTION': 'Violent Crimes',
        'RIOTS': 'Violent Crimes',
        'CRUELTY BY HUSBAND': 'Crimes Against Women',
        'CRIMES RELATED TO WOMEN': 'Crimes Against Women',
        'POCSO': 'Crimes Against Children',
        'CRIMINAL INTIMIDATION': 'Violent Crimes',
        'WRONGFUL RESTRAINT/CONFINEMENT': 'Violent Crimes',
        'INSULTING MODESTY OF WOMEN (EVE TEASING)': 'Crimes Against Women',
        'ASSAULT OR USE OF CRIMINAL FORCE TO DISROBE WOMAN': 'Crimes Against Women',
        'EXPOSURE AND ABANDONMENT OF CHILD': 'Crimes Against Children',
        'DOWRY DEATHS': 'Crimes Against Women',
        'OFFENCES RELATED TO MARRIAGE': 'Crimes Against Women',
        'ASSAULT': 'Violent Crimes',
        'CRIMINAL TRESPASS': 'Violent Crimes',
        'MISCHIEF': 'Other Offenses',
        'ARSON': 'Violent Crimes',
        'CRIMINAL CONSPIRACY': 'Violent Crimes',
        'AFFRAY': 'Violent Crimes',
        'CrPC': 'Other Offenses',
        'KARNATAKA POLICE ACT 1963': 'Other Offenses',
        'Karnataka State Local Act': 'Other Offenses',
        'NARCOTIC DRUGS & PSHYCOTROPIC SUBSTANCES': 'Drug Offenses',
        'RAPE': 'Crimes Against Women',
        'IMMORAL TRAFFIC': 'Crimes Against Women',
        'SCHEDULED CASTE AND THE SCHEDULED TRIBES ': 'Hate Crimes',
        'COMMUNAL / RELIGION   ': 'Hate Crimes',
        'OFFENCES AGAINST PUBLIC SERVANTS (Public servant is a victim)': 'Crimes Against Public Servants',
        'SUICIDE': 'Other Offenses',
    }
    df['Crime_Category'] = df['CrimeGroup_Name'].map(category_mapping).fillna('Other Offenses')
    logging.info("Crime categories mapped")
    
    # =====================================================
    # 9. Chọn cột output cuối cùng
    # =====================================================
    output_cols = [
        'District_Name', 'UnitName', 'FIR_YEAR', 'FIR_MONTH',
        'FIR_Type_Clean', 'FIR_Stage_Clean', 'Complaint_Mode',
        'CrimeGroup_Name', 'Crime_Category',
        'Victim_Total', 'Victim_Adult_Male', 'Victim_Adult_Female', 'Victim_Minor',
        'Accused Count', 'Arrested_Count',
        'Accused_ChargeSheeted Count', 'Conviction Count',
    ]
    
    result = df[output_cols].copy()
    result = result.rename(columns={
        'FIR_YEAR': 'Year',
        'FIR_MONTH': 'Month',
        'FIR_Type_Clean': 'FIR_Type',
        'FIR_Stage_Clean': 'Case_Outcome',
        'Accused Count': 'Accused_Count',
        'Accused_ChargeSheeted Count': 'ChargeSheeted_Count',
        'Conviction Count': 'Conviction_Count',
    })
    
    # =====================================================
    # 10. Save
    # =====================================================
    output_path = os.path.join(os.path.dirname(__file__), '..', 
                               'data', 'processed', 'Case_Outcome_Cleaned.csv')
    result.to_csv(output_path, index=False)
    logging.info(f"Saved cleaned data to Case_Outcome_Cleaned.csv ({len(result):,} rows)")
    
    return result


if __name__ == '__main__':
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from ingestion.ingest_case_outcome import ingest_case_outcome_data
    raw = ingest_case_outcome_data()
    clean_case_outcome_data(raw)
    print("Done!")
