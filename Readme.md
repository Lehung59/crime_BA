# Predictive Guardians Dashboard

Hệ thống phân tích tội phạm đô thị dựa trên dữ liệu thực tế từ **Cảnh sát Bang Karnataka, Ấn Độ**.

---

## 1. Yêu cầu hệ thống

- **Python:** Phiên bản **3.11** (Bắt buộc. Các phiên bản 3.12+ có thể gây lỗi Pillow/Folium trên Windows).
- **Java:** **JDK 8** trở lên (Bắt buộc cho H2O AutoML — dùng bởi pipeline training, không cần khi chỉ xem dashboard).
- **RAM:** Tối thiểu 4GB (Khuyến nghị 8GB).

---

## 2. Cài đặt & Chạy ứng dụng

```powershell
# Bước 1: Tạo môi trường ảo
python -m venv venv311

# Bước 2: Kích hoạt
.\venv311\Scripts\activate          # Windows
# source venv311/bin/activate       # macOS/Linux

# Bước 3: Cài thư viện
pip install -r requirements.txt

# Bước 4: Chạy dashboard
cd app
python -m streamlit run app.py
```

Ứng dụng mở tại `http://localhost:8501`.

---

## 3. Cấu trúc dự án

```
Predictive_Guardians-main/
├── app/                          # Streamlit UI — từng file = 1 module dashboard
│   ├── app.py                    # Entry point + routing
│   ├── Crime_Pattern_Analysis.py # Module 1: Phân tích hình mẫu
│   ├── Criminal_Profiling.py     # Module 2: Hồ sơ tội phạm
│   ├── Case_Outcome_Monitoring.py# Module 3: Theo dõi kết quả xử lý
│   └── Resource_Allocation.py    # Module 4: Phân bổ nguồn lực
│
├── Component_datasets/           # Dữ liệu đã cleaning (CSV) — dashboard đọc từ đây
│   ├── Crime_Pattern_Analysis_Cleaned.csv
│   ├── Criminal_Profiling_cleaned.csv
│   ├── Case_Outcome_Cleaned.csv
│   └── Resource_Allocation_Cleaned.csv
│
├── archive/                      # Dữ liệu gốc thô
│   └── FIR_Details_Data.csv      # 1.67 triệu dòng, 34 cột — nguồn chính
│
├── Crime_Pattern_Analysis/       # Script ingest + clean cho Module 1
├── Criminal_Profiling/           # Script ingest + clean cho Module 2
├── Case_Outcome_Monitoring/      # Script ingest + clean cho Module 3
├── Resource_Allocation/          # Script ingest + clean cho Module 4
│
├── Data_Dictionary_VN.md         # Giải thích thuật ngữ bằng tiếng Việt
└── Readme.md                     # File này
```

---

## 4. Giải thích Dữ liệu — Tại sao lấy những gì, lọc như thế nào?

### 4.1. Nguồn dữ liệu gốc

Toàn bộ dự án sử dụng dữ liệu từ **Karnataka State Police (KSP)** — cơ quan cảnh sát bang Karnataka, Ấn Độ. File gốc là `FIR_Details_Data.csv` (~570MB, 1.67 triệu bản ghi FIR từ 2016-2020+).

Ngoài ra, module Criminal Profiling kết hợp thêm 3 bộ dữ liệu phụ:
- `AccusedData.csv` — Thông tin nhân khẩu học nghi phạm (tuổi, giới, đẳng cấp, nghề).
- `MOBsData.csv` — Modus Operandi Bureau (phương thức gây án).
- `RowdySheeterDetails.csv` — Danh sách đối tượng nguy hiểm có tiền án.

### 4.2. Quy tắc cleaning chung (áp dụng cho tất cả module)

| Quy tắc | Lý do | Áp dụng ở |
|---------|-------|-----------|
| `drop_duplicates()` | Loại bỏ bản ghi trùng lặp | Tất cả module |
| Loại bỏ quận `CID`, `ISD Bengaluru`, `Coastal Security Police` | Đây là đơn vị đặc biệt (tình báo, an ninh biển), không phải quận địa lý thực tế | Resource Allocation, Case Outcome |
| Chuẩn hoá `District_Name` | Đổi tên quận cho khớp với bản đồ GeoJSON Karnataka (ví dụ `Bengaluru City` → `Bengaluru Urban`) | Crime Pattern, Case Outcome |
| Lọc tuổi `age >= 7 AND age <= 100` | Loại bỏ dữ liệu lỗi: tuổi 0 (chưa nhập), tuổi >100 (sai dữ liệu). Giữ từ 7 do luật Ấn Độ quy định trẻ từ 7 tuổi có thể chịu trách nhiệm hình sự | Criminal Profiling |
| Lọc tọa độ `11 < Lat < 19`, `74 < Lon < 78` | Giới hạn trong bbox Karnataka. Loại bỏ tọa độ sai (ví dụ 0,0 hoặc ngoài Ấn Độ) | Crime Pattern |
| `fillna('unknown')` cho cột phân loại | Giữ bản ghi thay vì xoá, đánh dấu `unknown` để biểu đồ có thể lọc ra | Criminal Profiling |
| Map `CrimeGroup_Name` → `Crime_Category` | Gom 150+ loại tội gốc vào ~12 nhóm lớn để biểu đồ dễ đọc | Resource Allocation, Case Outcome |

### 4.3. Chi tiết từng module lấy dữ liệu gì

#### Module 1: Crime Pattern Analysis
**Nguồn:** `FIR_Details_Data.csv` + `Polce_Stations_Lat_Long.csv`  
**Cột được chọn:**
| Cột | Ý nghĩa | Lý do cần |
|-----|---------|-----------|
| `District_Name` | Quận/huyện | Vẽ bản đồ Choropleth |
| `Year`, `Month`, `Day` | Thời gian (trích từ `FIR_Reg_DateTime`) | Phân tích xu hướng theo thời gian |
| `CrimeGroup_Name` | Nhóm tội phạm | Bộ lọc tương tác |
| `Latitude`, `Longitude` | Tọa độ (impute từ tọa độ đồn cảnh sát + hướng/khoảng cách) | Heatmap + DBSCAN clustering |
| `Distance from PS` | Khoảng cách từ hiện trường tới đồn | Tính toạ độ thực tế |

**Cleaning đặc biệt:** Tọa độ ban đầu bị thiếu rất nhiều → script dùng tọa độ đồn cảnh sát + cột `Distance from PS` (hướng + khoảng cách dạng text) để **tính toạ độ xấp xỉ** bằng công thức lượng giác Earth radius.

---

#### Module 2: Criminal Profiling
**Nguồn:** `AccusedData.csv` + `MOBsData.csv` + `RowdySheeterDetails.csv`  
**Cách kết hợp:** Inner join 3 bảng qua `(District_Name, Unit_Name, Name)`  
**Cột được chọn:**
| Cột | Ý nghĩa | Lý do cần |
|-----|---------|-----------|
| `age` | Tuổi nghi phạm (lọc 7-100) | Phân bố tuổi, nhóm tuổi rủi ro |
| `Sex` | Giới tính | Tỷ lệ nam/nữ trong tội phạm |
| `Caste` | Đẳng cấp xã hội (hệ thống Varna của Ấn Độ) | Proxy cho điều kiện kinh tế - xã hội |
| `Occupation` | Nghề nghiệp | Mối tương quan nghề - tội phạm |
| `Crime_Group1` | Nhóm tội chính | Phân tích loại tội |
| `Crime_Head2` | Phân loại tội chi tiết | Drill-down |

**Tại sao lọc tuổi 7-100?** Luật hình sự Ấn Độ (IPC Section 82-83) quy định trẻ dưới 7 tuổi không chịu trách nhiệm hình sự. Giá trị tuổi 0 hoặc >100 là dữ liệu nhập sai.

---

#### Module 3: Case Outcome Monitoring *(Mới)*
**Nguồn:** `FIR_Details_Data.csv`  
**Cột được chọn:**
| Cột | Ý nghĩa | Lý do cần |
|-----|---------|-----------|
| `FIR_Stage` → gom thành `Case_Outcome` | Trạng thái vụ án (Convicted/Pending Trial/Undetected/Discharged/Other) | Tỷ lệ phá án, kết án |
| `FIR Type` → `FIR_Type` | Heinous (nghiêm trọng) / Non Heinous | Xu hướng mức độ nghiêm trọng |
| `Complaint_Mode` | Hình thức phát hiện (Written/Sue-moto by Police/...) | Đánh giá tuần tra chủ động |
| `Male, Female, Boy, Girl, Age 0` → `Victim_*` | Nạn nhân theo giới tính và tuổi | Phân tích nạn nhân |
| `Accused Count`, `Arrested_Count` | Số bị can, số bị bắt | Tỷ lệ bắt giữ |
| `Conviction Count` | Số vụ kết án | Hiệu quả tư pháp |

**Cleaning đặc biệt:**  
- `FIR_Stage` gốc có ~11 giá trị khác nhau → gom lại thành **5 nhóm**: Convicted, Pending Trial, Undetected, Discharged/Acquitted, Other.
- Cột nạn nhân (Male/Female/Boy/Girl/Age 0) được cộng lại thành `Victim_Total` và chia thành 3 nhóm: `Victim_Adult_Male`, `Victim_Adult_Female`, `Victim_Minor`.

---

#### Module 4: Police Resource Allocation
**Nguồn:** `FIR_Details_Data.csv` + bảng sanctioned strength (hardcoded)  
**Cột được chọn:**
| Cột | Ý nghĩa | Lý do cần |
|-----|---------|-----------|
| `District_Name` | Quận | Map tới bảng quân số cảnh sát |
| `UnitName` | Đồn cảnh sát | Đơn vị phân bổ |
| `Beat_Name` | Tuyến tuần tra | Đơn vị nhỏ nhất |
| `CrimeGroup_Name` → `Crime Severity` | Trọng số mức nghiêm trọng (1-5) | Hàm mục tiêu cho Linear Programming |
| `ASI`, `CHC`, `CPC` | Quân số ASI/Head Constable/Police Constable của mỗi quận | Ràng buộc tối ưu hoá |

**Cleaning đặc biệt:** Map 150+ `CrimeGroup_Name` → 10 nhóm lớn → gán trọng số severity (Violent=5, Property=3, Other=1). Dùng PuLP Linear Programming để tối ưu phân bổ.

---

## 5. Tham khảo thêm

- `Data_Dictionary_VN.md` — Giải thích chi tiết hệ thống đẳng cấp Ấn Độ, nghề nghiệp, nhóm tội phạm bằng tiếng Việt.
