# 📊 Phase 1: Descriptive Analytics

> **Tags:** #descriptive #phase1 #EDA
> **Trạng thái:** 🔲 Chưa bắt đầu
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
- [ ] Load & kiểm tra chất lượng data (null, outlier, duplicates)
- [ ] Chuẩn hóa `Beat_Name` (BEAT 1 = Beat 1 = 1)
- [ ] Nhóm `FIR_Stage` thành nhóm chính (Pending, Convicted, Undetected, Other)
- [ ] Parse `Distance from PS` (text → numeric nếu có thể)
- [ ] Tính `Arrest_Rate = Arrested Count / Accused Count`
- [ ] Tính `Conviction_Rate = Conviction Count / Accused Count`

### 1.1 Temporal Analysis
- [ ] Line chart: số vụ theo năm (2016–2024)
- [ ] Heatmap: tháng × năm (crime volume)
- [ ] Bar chart: số vụ theo tháng (seasonality)
- [ ] Analysis COVID impact (2020 dip)

### 1.2 Spatial Analysis
- [ ] Choropleth map: tội phạm theo quận
- [ ] Bar chart: Top 10 districts
- [ ] Pie/bar: Bengaluru City vs Rest
- [ ] Top Beats theo volume

### 1.3 Crime Type Analysis
- [ ] Treemap: CrimeGroup_Name
- [ ] Horizontal bar: Top 15 crime groups
- [ ] Phân tích Heinous vs Non-Heinous
- [ ] Complaint Mode distribution

### 1.4 Victim & Case Outcome
- [ ] Pie chart: nạn nhân theo giới tính
- [ ] Stacked bar: FIR_Stage breakdown
- [ ] Funnel: Accused → Arrested → Charged → Convicted
- [ ] Detection rate theo quận

### 1.5 Dashboard
- [ ] Tạo Streamlit / Power BI dashboard tổng hợp

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
