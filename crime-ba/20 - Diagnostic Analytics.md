# 🔍 Phase 2: Diagnostic Analytics

> **Tags:** #diagnostic #phase2 #root-cause
> **Trạng thái:** ✅ Hoàn thành
> **Câu hỏi cốt lõi:** *"Tại sao tội phạm lại tập trung ở những nơi và thời điểm đó?"*

---

## 🎯 Mục tiêu

Đi sâu vào **nguyên nhân** của các pattern tội phạm đã phát hiện ở Phase 1:
- Tại sao khu vực A có tội phạm cao hơn khu vực B?
- Yếu tố nào (địa lý, thời gian, nhân khẩu học) có tương quan mạnh với tội phạm?
- Vì sao tỷ lệ phá án một số loại tội phạm/quận thấp?

---

## 📋 Task List

### 2.1 Correlation & Relationship Analysis
- [x] Heatmap: Nhóm tuổi × Loại tội phạm
- [x] Sunburst: Giới tính → Nhóm tuổi → Loại tội
- [x] Treemap: Đẳng cấp (Caste) → Loại tội phạm
- [x] Stacked Bar: Nghề nghiệp × Nhóm tội
- [x] Phân tích tương quan giữa nhân khẩu học và hành vi phạm tội

### 2.2 Hotspot Analysis (Điểm nóng)
- [x] Thuật toán **DBSCAN** để phát hiện cụm tội phạm (Cluster)
- [x] **Folium Heatmap** để trực quan hóa mật độ tội phạm
- [x] Lọc theo thời gian và loại tội phạm để chẩn đoán cụ thể từng loại hotspot
- [x] Marker cụm lân cận để xác định chính xác khu vực cần điều tra nguyên nhân

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
