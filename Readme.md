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

## Luồng hoạt động của code

```
app.py (Entry Point)
  │
  ├── Sidebar Menu (option_menu) ──→ selected = "Home" / "Crime Pattern..." / ...
  │
  ├── if/elif routing:
  │     │
  │     ├── "Home"
  │     │     └── Hiển thị trang giới thiệu (HTML tĩnh trong app.py)
  │     │
  │     ├── "Crime Pattern Analysis"
  │     │     ├── load_crime_pattern_data()  ←  @st.cache_data
  │     │     │     ├── Tải GeoJSON (GitHub raw URL)
  │     │     │     └── Đọc Crime_Pattern_Analysis_Cleaned.csv
  │     │     ├── temporal_analysis()   →  Biểu đồ bar theo Năm/Tháng/Ngày
  │     │     ├── chloropleth_maps()    →  Bản đồ Choropleth (Plotly Mapbox)
  │     │     └── crime_hotspots()      →  Heatmap + DBSCAN markers (Folium)
  │     │
  │     ├── "Criminal Profiling"
  │     │     └── create_criminal_profiling_dashboard()
  │     │           ├── Đọc Criminal_Profiling_cleaned.csv
  │     │           ├── Section 1-5: Phân tích đơn biến (Age, Gender, Caste, Occupation, Crime)
  │     │           └── Section 6a-6d: Phân tích tương quan (Heatmap, Treemap, Sunburst, Stacked Bar)
  │     │
  │     ├── "Predictive Modeling"
  │     │     └── predictive_modeling_recidivism()
  │     │           ├── init_h2o()              ←  @st.cache_resource (chỉ chạy 1 lần)
  │     │           ├── load_model_recidivism()  ←  @st.cache_resource
  │     │           ├── User nhập: Age, Caste, Profession, District, City
  │     │           ├── Frequency encoding  →  scaler.transform()  →  H2OFrame
  │     │           └── model.predict()  →  Kết quả: tái phạm / không tái phạm
  │     │
  │     └── "Police Resource Allocation"
  │           └── resource_allocation(df)
  │                 ├── User chọn District → lọc Beat/Village
  │                 ├── Cấu hình: Default/Custom sanctioned strength (ASI, CHC, CPC)
  │                 └── optimise_resource_allocation()
  │                       ├── PuLP LpProblem("Maximize")
  │                       ├── Objective: max Σ(severity × officers)
  │                       ├── Constraints: tổng ≤ quân số, mỗi beat ≥ 1
  │                       └── Output: bảng phân bổ ASI/CHC/CPC theo từng beat
```

---

## Chi tiết từng module

### 1. Crime Pattern Analysis (`Crime_Pattern_Analysis.py`)

**Input:** `Crime_Pattern_Analysis_Cleaned.csv` (chứa Year, Month, Day, District_Name, CrimeGroup_Name, Latitude, Longitude, FIRNo, VICTIM COUNT, Accused Count)

**Xử lý:**
- **Temporal Analysis:** Group by thời gian → bar chart Plotly (người dùng chọn filter quận + loại tội)
- **Choropleth:** Aggregate theo District → hiển thị trên bản đồ Mapbox sử dụng GeoJSON Karnataka
- **Hotspot:** Aggregate theo tọa độ → Folium HeatMap + DBSCAN(eps=0.1, min_samples=5) để tìm crime clusters

**Output:** Biểu đồ tương tác + bản đồ

---

### 2. Criminal Profiling (`Criminal_Profiling.py`)

**Input:** `Criminal_Profiling_cleaned.csv` (chứa Occupation, Crime_Group1, Crime_Head2, age, Caste, Sex)

**Xử lý:** Tính toán thống kê mô tả cho từng biến, tạo biểu đồ Plotly với insight tự động.

**Các biểu đồ:**
| Biểu đồ | Kỹ thuật |
|----------|----------|
| Age Distribution | Histogram + Mean/Median lines |
| Gender Analysis | Bar chart (log scale) |
| Caste Analysis | Top 10 bar chart |
| Occupation Analysis | Horizontal bar chart |
| Crime Categories | Grouped tabs (Category + Sub-category) |
| Age × Crime Heatmap | `pd.crosstab` → `go.Heatmap` |
| Caste × Crime Treemap | `px.treemap` |
| Gender-Age-Crime Sunburst | `px.sunburst` (3 levels) |
| Occupation × Crime Stacked Bar | `pd.crosstab` → stacked `go.Bar` |

---

### 3. Predictive Modeling (`Predictive_modeling.py`)

**Input:** User nhập 5 trường: Age, Caste, Profession, District, City

**Xử lý:**
1. `h2o.init()` — Khởi tạo JVM (cached, chỉ chạy 1 lần)
2. Load MOJO model: `StackedEnsemble_BestOfFamily_2_AutoML_1_20240719_183320.zip`
3. Frequency encoding: Chuyển categorical → numeric dùng `frequency_encoding.json`
4. StandardScaler: Chuẩn hóa features dùng `scaler.pkl`
5. Chuyển sang `H2OFrame` → `model.predict()`

**Output:** Binary classification — "Likely to repeat" hoặc "Not likely to repeat"

**Model:** H2O StackedEnsemble (AutoML), được huấn luyện offline bằng `pipelines/training_pipeline.py`

---

### 4. Police Resource Allocation (`Resource_Allocation.py`)

**Input:** `Resource_Allocation_Cleaned.csv` (chứa District_Name, UnitName, Beat, Village_Area_Name, Normalised Crime Severity, ASI_Sanctioned, CHC_Sanctioned, CPC_Sanctioned)

**Xử lý:**
1. User chọn District → lọc danh sách Beat/Village
2. Chọn Default hoặc Custom sanctioned strength
3. Gọi `optimise_resource_allocation()`:
   - Thư viện: **PuLP** (Linear Programming)
   - Biến quyết định: `ASI[i]`, `CHC[i]`, `CPC[i]` cho mỗi beat (integer ≥ 0)
   - Hàm mục tiêu: `Maximize Σ (crime_severity[i] × (ASI[i] + CHC[i] + CPC[i]))`
   - Ràng buộc:
     - `Σ ASI[i] ≤ ASI_Sanctioned` (tương tự cho CHC, CPC)
     - `ASI[i] + CHC[i] + CPC[i] ≥ 1` (mỗi beat ít nhất 1 người)
     - `ASI[i] ≤ severity[i] × ASI_Sanctioned` (giới hạn theo tỷ lệ severity)

**Output:** Bảng DataFrame hiển thị số ASI/CHC/CPC được phân bổ cho mỗi Beat

---

## Dữ liệu đầu vào

Tất cả dữ liệu nằm trong `Component_datasets/`. Đây là dữ liệu **đã được làm sạch** — quá trình cleaning nằm trong các notebook ở thư mục gốc của từng component (`Crime_Pattern_Analysis/`, `Criminal_Profiling/`, v.v.).

| File | Kích thước | Số cột chính |
|------|-----------|-------------|
| `Crime_Pattern_Analysis_Cleaned.csv` | 66 MB | Year, Month, Day, District_Name, CrimeGroup_Name, Lat, Lon, FIRNo, VICTIM COUNT, Accused Count |
| `Criminal_Profiling_cleaned.csv` | 3.5 MB | Occupation, Crime_Group1, Crime_Head2, age, Caste, Sex |
| `Recidivism_cleaned_data.csv` | 49 MB | District_Name, age, Caste, Profession, PresentCity |
| `Resource_Allocation_Cleaned.csv` | 1.9 MB | District_Name, UnitName, Beat, Village_Area_Name, Normalised Crime Severity, ASI/CHC/CPC Sanctioned |

---

## Models đã huấn luyện

Nằm trong `models/Recidivism_model/`:

| File | Mô tả |
|------|--------|
| `StackedEnsemble_*.zip` | H2O MOJO model — StackedEnsemble (kết hợp GBM + Deep Learning) |
| `frequency_encoding.json` | Mapping value → frequency cho Caste, Profession, District_Name, PresentCity |
| `scaler.pkl` | Scikit-learn StandardScaler đã fit trên training data |
| `h2o-genmodel.jar` | H2O Java runtime (cần thiết để load MOJO) |

Để huấn luyện lại model: `python pipelines/training_pipeline.py`

---

## Xử lý sự cố

### Lỗi "Application Control Policy" / Pillow DLL bị block

**Nguyên nhân:** Windows Security chặn DLL của Pillow trên Python 3.13.

**Giải pháp:** Sử dụng Python 3.11 (đã tạo trong `venv311`).

---

### Lỗi "H2O init" bị treo / Java not found

**Nguyên nhân:** Chưa cài Java hoặc `JAVA_HOME` chưa được set.

**Giải pháp:**
```powershell
# Kiểm tra Java
java -version

# Nếu chưa có, cài JDK 8+ từ https://adoptium.net/
```

---

### Lỗi khi chuyển tab (nội dung cũ hiển thị)

**Nguyên nhân:** Streamlit re-run script, H2O load chậm.

**Đã xử lý:** Custom CSS ẩn stale content + loading overlay. Nếu vẫn gặp, nhấn F5 để refresh hoàn toàn.

---

### Ứng dụng chạy chậm lần đầu

**Bình thường.** Lần đầu cần:
- Tải GeoJSON từ GitHub (~1-2 giây)
- Khởi tạo H2O JVM (~15-30 giây)
- Load CSV lớn (~2-5 giây)

Các lần sau sẽ nhanh hơn nhờ `@st.cache_data` và `@st.cache_resource`.
