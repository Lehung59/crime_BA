import os
import sys

# Thêm đường dẫn gốc của dự án vào sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Import các module Ingestion và Preprocessing
from ingestion.ingest_crime_pattern import *
from preprocessing.clean_crime_pattern import *
from ingestion.ingest_criminal_profiling import *
from preprocessing.clean_criminal_profiling import *
from ingestion.ingest_resource_allocation import *
from preprocessing.clean_resource_allocation import *
from ingestion.ingest_case_outcome import *
from preprocessing.clean_case_outcome import *

def run_crime_pattern_analysis():
    print("🚀 Đang xử lý: Crime Pattern Analysis...")
    raw_data = ingest_crime_pattern_analysis()
    cleaned_data = clean_data_crime_pattern_analysis(raw_data)
    update_crime_lat_long(cleaned_data)

def run_criminal_profiling():
    print("🚀 Đang xử lý: Criminal Profiling...")
    raw_data = ingest_criminal_profiling()
    clean_Criminal_Profiling(raw_data)

def run_resource_allocation():
    print("🚀 Đang xử lý: Resource Allocation...")
    raw_data = ingest_resource_data()
    clean_resource_data(raw_data)

def run_case_outcome_monitoring():
    print("🚀 Đang xử lý: Case Outcome Monitoring...")
    raw_data = ingest_case_outcome_monitoring()
    clean_case_outcome_data(raw_data)

if __name__ == "__main__":
    print("=== BẮT ĐẦU PIPELINE XỬ LÝ DỮ LIỆU BI ===")
    run_crime_pattern_analysis()
    run_criminal_profiling()
    run_resource_allocation()
    run_case_outcome_monitoring()
    print("=== HOÀN THÀNH PIPELINE ===")
