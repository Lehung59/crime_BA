# Predictive Guardians

## Mục lục

1. [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
2. [Cấu trúc thư mục](#cấu-trúc-thư-mục)
3. [Cài đặt môi trường](#cài-đặt-môi-trường)
4. [Chạy ứng dụng](#chạy-ứng-dụng)
5. [Luồng hoạt động của code](#luồng-hoạt-động-của-code)
6. [Chi tiết từng module](#chi-tiết-từng-module)
7. [Dữ liệu đầu vào](#dữ-liệu-đầu-vào)
8. [Models đã huấn luyện](#models-đã-huấn-luyện)
9. [Xử lý sự cố](#xử-lý-sự-cố)

---

## Yêu cầu hệ thống

| Thành phần | Yêu cầu |
|------------|----------|
| Python | **3.11** (bắt buộc — Python 3.13 gây lỗi Pillow DLL trên Windows) |
| Java | JDK 8+ (cần thiết cho H2O engine) |
| RAM | Tối thiểu 4 GB (khuyến nghị 8 GB do H2O khởi tạo JVM) |
| OS | Windows 10/11 |

---

## Cấu trúc thư mục

```
Predictive_Guardians-main/
├── app/                          # Source code ứng dụng Streamlit
│   ├── app.py                    # Entry point — định tuyến trang, sidebar menu
│   ├── Crime_Pattern_Analysis.py # Module phân tích hình mẫu tội phạm
│   ├── Criminal_Profiling.py     # Module hồ sơ tội phạm (storytelling)
│   ├── Predictive_modeling.py    # Module dự đoán tái phạm (H2O AutoML)
│   ├── Resource_Allocation.py    # Module phân bổ nguồn lực cảnh sát (PuLP)
│   └── Continuous_Learning_and_Feedback.py  # (đã ẩn khỏi sidebar)
│
├── Component_datasets/           # Dữ liệu đã được làm sạch (CSV)
│   ├── Crime_Pattern_Analysis_Cleaned.csv   # ~66 MB
│   ├── Criminal_Profiling_cleaned.csv       # ~3.5 MB
│   ├── Recidivism_cleaned_data.csv          # ~49 MB
│   ├── Resource_Allocation_Cleaned.csv      # ~1.9 MB
│   ├── Crime_Type_cleaned_data.csv          # ~17 MB
│   └── Feedback.csv
│
├── models/                       # Models đã huấn luyện
│   └── Recidivism_model/
│       ├── StackedEnsemble_*.zip            # H2O MOJO model (dự đoán tái phạm)
│       ├── frequency_encoding.json          # Bảng mã hóa tần suất cho các biến phân loại
│       ├── scaler.pkl                       # StandardScaler đã fit
│       └── h2o-genmodel.jar                 # H2O runtime JAR
│
├── pipelines/
│   └── training_pipeline.py      # Script huấn luyện lại model
│
├── venv311/                      # Virtual environment Python 3.11
├── requirements.txt              # Danh sách dependencies
└── Readme.md                     # File này
```

---

## Cài đặt môi trường

### Bước 1: Tạo virtual environment Python 3.11

```powershell
# Tải Python 3.11 từ https://www.python.org/downloads/release/python-3119/
# Sau khi cài, tạo venv:
"C:\path\to\python311\python.exe" -m venv venv311
```

### Bước 2: Kích hoạt venv và cài dependencies

```powershell
.\venv311\Scripts\activate
pip install -r requirements.txt
pip install joblib branca
```

**Danh sách dependencies chính:**

| Package | Vai trò |
|---------|---------|
| `streamlit` | Framework web UI |
| `streamlit-option-menu` | Sidebar menu component |
| `plotly` | Biểu đồ tương tác |
| `folium` + `streamlit-folium` | Bản đồ Choropleth & Heatmap |
| `h2o` | AutoML engine (load MOJO model) |
| `pulp` | Linear Programming (phân bổ nguồn lực) |
| `scikit-learn` | DBSCAN clustering, StandardScaler |
| `statsmodels` | Phân tích chuỗi thời gian |
| `pandas`, `numpy` | Xử lý dữ liệu |

---

## Chạy ứng dụng

```powershell
# 1. Kích hoạt môi trường
.\venv311\Scripts\activate

# 2. Di chuyển vào thư mục app
cd app

# 3. Chạy Streamlit
python -m streamlit run app.py
```

Ứng dụng sẽ mở tại `http://localhost:8501`.

> **Lưu ý:** Lần đầu chuyển sang tab "Predictive Modeling", H2O sẽ khởi tạo JVM (~15-30 giây). Các lần sau sẽ nhanh hơn do đã cache.

---
