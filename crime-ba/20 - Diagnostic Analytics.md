# 🔍 Phase 2: Diagnostic Analytics

> **Tags:** #diagnostic #phase2 #root-cause
> **Trạng thái:** 🔲 Chưa bắt đầu
> **Câu hỏi cốt lõi:** *"Tại sao tội phạm lại tập trung ở những nơi và thời điểm đó?"*

---

## 🎯 Mục tiêu

Đi sâu vào **nguyên nhân** của các pattern tội phạm đã phát hiện ở Phase 1:
- Tại sao khu vực A có tội phạm cao hơn khu vực B?
- Yếu tố nào (địa lý, thời gian, nhân khẩu học) có tương quan mạnh với tội phạm?
- Vì sao tỷ lệ phá án một số loại tội phạm/quận thấp?

---

## 📋 Task List

### 2.1 Correlation Analysis
- [ ] Cramér's V cho cặp biến categorical (CrimeGroup × District, CrimeGroup × Month)
- [ ] Scatter plot: `Distance from PS` vs `Detection Rate`
- [ ] Phân tích `Offence_Duration` theo loại tội phạm (instant vs prolonged crime)
- [ ] Correlation matrix (numeric features)

### 2.2 Drill-Down Điều tra

#### Case A: Tại sao Bengaluru City chiếm 25.4%?
- [ ] So sánh mật độ crime / đồn cảnh sát giữa Bengaluru vs các quận khác
- [ ] Phân tích mix loại crime ở Bengaluru (Cyber, Theft, Traffic vs bạo lực)
- [ ] So sánh `Complaint_Mode` (Online % ở Bengaluru vs nông thôn)

#### Case B: Tại sao Cyber Crime tăng?
- [ ] Line chart Cyber Crime theo năm → xác nhận trend tăng
- [ ] Phân tích Beat/District nào là hotspot của Cyber Crime
- [ ] Complaint_Mode: bao nhiêu % là Online

#### Case C: Tại sao tỷ lệ Undetected cao?
- [ ] Bar chart: Undetected rate theo District
- [ ] Bar chart: Undetected rate theo CrimeGroup
- [ ] Phân tích IO workload: số vụ /IO → IO quá tải → detection thấp?

#### Case D: Missing Person Pattern
- [ ] Phân tích theo giới tính nạn nhân (phụ nữ/trẻ em gái vs nam)
- [ ] Phân tích theo tháng/mùa
- [ ] District nào có Missing Person cao nhất

### 2.3 Phân tích Yếu tố Xã hội học
- [ ] (Dùng Criminal_Profiling data) Occupation → Crime Type mapping
- [ ] Beat distance → detection lag
- [ ] Phân tích "Sue-moto by Police" (16.1%) → khu vực nào cảnh sát chủ động phát hiện cao nhất

---

## 🔬 Phương pháp Phân tích

| Kỹ thuật | Ứng dụng |
|---|---|
| **Cramér's V** | Đo tương quan giữa các biến categorical |
| **Chi-square test** | Kiểm định độc lập giữa hai biến phân loại |
| **Cross-tabulation** | Drill-down multi-dimension |
| **Pareto Analysis** | 20% nguyên nhân gây 80% vụ án |
| **Control Chart** | Phát hiện thời điểm bất thường |

---

## 📊 Key Hypotheses (Giả thuyết cần kiểm chứng)

| ID | Giả thuyết | Kết quả |
|---|---|---|
| H1 | Khu vực xa đồn cảnh sát có tỷ lệ Undetected cao hơn | ⬜ Chưa kiểm tra |
| H2 | Cyber Crime tăng mạnh sau 2020 (COVID → online) | ⬜ Chưa kiểm tra |
| H3 | IO có workload cao (nhiều vụ/IO) → detection rate thấp | ⬜ Chưa kiểm tra |
| H4 | Mùa hè (tháng 5-6) có tội phạm cao hơn mùa mưa | ⬜ Chưa kiểm tra |
| H5 | Heinous crimes tập trung ở urban (Bengaluru) nhiều hơn rural | ⬜ Chưa kiểm tra |

---

## 📊 Key Findings (điền khi phân tích xong)

> *[Ghi lại phát hiện chính sau khi hoàn thành phân tích]*

---

## 🔗 Điều hướng

- [[10 - Descriptive Analytics|← Phase 1: Descriptive]]
- [[30 - Predictive Analytics|→ Phase 3: Predictive]]
