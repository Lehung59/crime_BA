# 📊 Phase 1: Descriptive Analytics

> **Tags:** #descriptive #phase1 #EDA
> **Trạng thái:** ✅ Hoàn thành
> **Câu hỏi cốt lõi:** *"Chuyện gì đã xảy ra với tội phạm ở Karnataka giai đoạn 2016–2024?"*

---

## 🎯 Mục tiêu

Mô tả toàn diện bức tranh tội phạm qua:
- **Không gian:** Tội phạm tập trung ở đâu?
- **Thời gian:** Tội phạm xảy ra vào lúc nào?
- **Loại:** Tội phạm gì phổ biến nhất?
- **Đối tượng:** Ai là nạn nhân? Ai là thủ phạm?

---

## 📋 Task List

### Chuẩn bị Dữ liệu
- [x] Load & kiểm tra chất lượng data (null, outlier, duplicates)
- [x] Chuẩn hóa `Beat_Name`
- [x] Nhóm `FIR_Stage` thành nhóm chính
- [x] Parse `Distance from PS`
- [x] Tính `Arrest_Rate` & `Conviction_Rate`

### 1.1 Temporal Analysis
- [x] Line/Bar chart: số vụ theo năm (2016–2024)
- [x] Heatmap/Bar: tháng/ngày × năm
- [x] Analysis COVID impact (phản ánh trong xu hướng năm)

### 1.2 Spatial Analysis
- [x] Choropleth map: tội phạm theo quận (Plotly Mapbox)
- [x] Bar chart: Top districts
- [x] Top Beats/Police Units theo volume

### 1.3 Crime Type Analysis
- [x] Treemap: CrimeGroup_Name (trong Criminal Profiling)
- [x] Horizontal bar: Top crime groups

### 1.4 Victim & Criminal Profiling
- [x] Phân tích nhân khẩu học: Tuổi, Giới tính, Đẳng cấp (Caste), Nghề nghiệp
- [x] Sunburst/Heatmap: Tương quan đa chiều (Caste × Crime, Age × Sex × Crime)

### 1.5 Dashboard
- [x] Xây dựng Streamlit Dashboard tích hợp (app.py)

---

## 📊 Key Findings (điền khi phân tích xong)

> *[Ghi lại phát hiện chính sau khi hoàn thành phân tích]*

### Findings tạm thời từ Metadata:
- **Bengaluru City** chiếm 25.4% tổng số vụ — cần ưu tiên nguồn lực cao nhất
- **Motor Vehicle Accidents Non-Fatal** là nhóm tội phạm phổ biến nhất (14.5%)
- **Latitude/Longitude thiếu 69.7%** — hạn chế spatial analysis trực tiếp, cần dùng District/Beat làm proxy
- **Theft** là crime group phổ biến thứ 2 và có tác động kinh tế trực tiếp
- **Cyber Crime** đứng thứ 9 (78,502 vụ) — trend gia tăng cần kiểm tra
- Nạn nhân nam >> nữ (888K vs 388K) nhưng trẻ em gái > trai (67K vs 44K)
- **Tỷ lệ Undetected cao** (188,150 vụ = 11.2%) — cần phân tích nguyên nhân

---

## 🔗 Điều hướng

- [[01 - Ke hoach thuc hien|← Về Kế hoạch]]
- [[20 - Diagnostic Analytics|→ Phase 2: Diagnostic]]
