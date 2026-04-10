# 🎯 Phase 4: Prescriptive Analytics

> **Tags:** #prescriptive #phase4 #optimization #resource-allocation
> **Trạng thái:** 🔲 Chưa bắt đầu
> **Câu hỏi cốt lõi:** *"Chúng ta cần làm gì để tối ưu hóa phân bổ cảnh sát và giảm thiểu tội phạm?"*

---

## 🎯 Mục tiêu

Chuyển hóa các insights từ Phase 1-3 thành **hành động cụ thể**:
1. **Phân bổ cảnh sát tối ưu** theo Beat/District dựa trên Risk Score
2. **Lịch tuần tra tối ưu** theo giờ/ngày/tháng cao điểm
3. **Chiến lược phòng ngừa** theo loại tội phạm
4. **Dashboard hỗ trợ ra quyết định** cho chỉ huy cảnh sát

---

## 📋 Task List

### 4.1 Composite Risk Score Framework

**Công thức đề xuất:**
```
Risk_Score(beat) = 
    w1 × Normalized_Crime_Volume
  + w2 × Heinous_Crime_Rate
  + w3 × (1 - Detection_Rate)
  + w4 × Predicted_Crime_Growth (từ Phase 3)
```

**Trọng số gợi ý:** w1=0.35, w2=0.30, w3=0.20, w4=0.15

- [ ] Tính Risk Score cho tất cả Beat
- [ ] Phân hạng Beat: **Tier 1** (High Risk), **Tier 2** (Medium), **Tier 3** (Low)
- [ ] Visualize bản đồ phân hạng (choropleth theo District)
- [ ] Sensitivity analysis: test các bộ trọng số khác nhau

---

### 4.2 Resource Allocation Optimization

**Bài toán tối ưu:**

```
Maximize: Σ(Crime_Reduction_i × Officers_Allocated_i)
Subject to:
  Σ Officers_Allocated_i = Total_Force_Available
  Officers_i ≥ Min_Officers_per_Beat (e.g., 2)
  Officers_i ≤ Max_Officers_per_Beat
  Officers_i ∈ Integer
```

- [ ] Thu thập dữ liệu lực lượng hiện tại (từ `Resource_Allocation_Cleaned.csv`)
- [ ] Xây dựng model LP/IP bằng **PuLP** hoặc **scipy.optimize**
- [ ] Tính `Crime_Reduction_Rate` cho mỗi Beat (giả định: thêm 1 cảnh sát → giảm X% vụ)
- [ ] Chạy optimization với tổng lực lượng hiện tại
- [ ] So sánh: **Hiện tại** vs **Đề xuất tối ưu**
- [ ] Output: Bảng phân bổ cụ thể theo District × Beat

**Output Table:**
| District | Beat | Hiện tại | Đề xuất | Thay đổi |
|---|---|---|---|---|
| Bengaluru City | Beat 1 | 5 | 8 | +3 |
| Mysuru Dist | Beat 12 | 4 | 2 | -2 |

---

### 4.3 Patrol Scheduling Optimization

**Mục tiêu:** Khi nào cần tuần tra mạnh hơn?

- [ ] Phân tích heatmap: `FIR_MONTH × FIR_Day` → giờ/ngày cao điểm
- [ ] Xây dựng ma trận lịch tuần tra (shift × beat × day-of-week)
- [ ] Đề xuất 3 ca tuần tra (sáng/chiều/tối) cho mỗi Beat theo weekday/weekend
- [ ] Tính coverage gap: Beat nào đang thiếu cảnh sát vào giờ cao điểm?

**Output:** Mô hình lịch tuần tra gợi ý (Gantt-style)

---

### 4.4 Prevention Strategy Matrix

Dựa trên loại tội phạm phổ biến, đề xuất chiến lược phòng ngừa cụ thể:

| Nhóm Tội phạm | Chiến lược Phòng ngừa | Ưu tiên |
|---|---|---|
| Motor Vehicle Accidents (14.5%) | Tăng checkpoint giao thông, camera tốc độ, phân công traffic warden | 🔴 Cao |
| Theft (9.5%) | Tuần tra đêm tại khu thương mại, hệ thống camera, khóa xe thông minh | 🔴 Cao |
| Cases of Hurt (7.5%) | Patrols tại điểm tụ tập, đường tối, quán nhậu | 🟠 Trung bình |
| Missing Person (7.5%) | Hotline 24/7, phối hợp cộng đồng, alert system | 🟠 Trung bình |
| Cyber Crime (4.7%) | Tập huấn nhận thức số, đội cyber crime chuyên trách | 🟠 Trung bình |
| Molestation (2.6%) | Patrol đêm khu dân cư, camera công cộng | 🔴 Cao |
| Narcotics (1.7%) | Kiểm tra định kỳ, thông tin viên | 🟠 Trung bình |

- [ ] Ưu tiên chiến lược theo: Crime Volume × Nguy hiểm × Khả thi
- [ ] ROI Analysis: chiến lược nào giảm crime nhiều nhất / chi phí thấp nhất

---

### 4.5 What-If Scenario Analysis

"Nếu tôi có thêm X cảnh sát, nên phân bổ vào đâu?"

- [ ] Scenario 1: Tăng thêm 50 cảnh sát toàn tỉnh — phân bổ tối ưu?
- [ ] Scenario 2: Bengaluru City tăng 30 cảnh sát — vào Beat nào?
- [ ] Scenario 3: Cắt giảm 10% lực lượng — loại bỏ từ đâu để ít ảnh hưởng nhất?

- [ ] Xây dựng hàm `optimize_allocation(total_force, district_filter)` tái sử dụng
- [ ] Interactive slider trong dashboard

---

### 4.6 Decision Support Dashboard

**Người dùng mục tiêu:** Chỉ huy cảnh sát cấp quận (District Superintendent)

**Tính năng:**
- [ ] **Map view:** Bản đồ Risk Heat Map theo Beat/District
- [ ] **Allocation panel:** Lực lượng hiện tại vs Lực lượng đề xuất (giao thanh)
- [ ] **Forecast panel:** Dự báo crime 6 tháng tới cho quận được chọn
- [ ] **Alert panel:** Beat nào đang underserved (Risk cao nhưng ít cảnh sát)
- [ ] **What-if slider:** Điều chỉnh tổng lực lượng → cập nhật phân bổ tối ưu ngay lập tức

**Stack:** **Streamlit** + Plotly + PuLP

---

## 📊 Expected Impacts (Dự kiến kết quả)

| Chỉ số | Hiện tại | Mục tiêu | Phương pháp |
|---|---|---|---|
| Tỷ lệ Undetected | ~11.2% | < 8% | Phân bổ IO hợp lý hơn |
| Thời gian phản ứng (ước tính) | Baseline | Giảm 15% | Patrol lịch tối ưu |
| Coverage Beat nguy cơ cao | Baseline | +20% | Reallocation |
| Crime Growth Rate | trend hiện tại | Flatten | Preventive deployment |

---

## ⚠️ Giới hạn & Khuyến nghị

| Hạn chế | Tác động | Giải pháp |
|---|---|---|
| Không có dữ liệu thực tế về số cảnh sát/beat | Không tối ưu chính xác | Dùng ước tính từ Resource_Allocation dataset |
| Không có dữ liệu kinh tế - xã hội chi tiết | Thiếu context ngoại sinh | Document rõ assumption |
| Model LP giả định linear crime reduction | Oversimplification | Test sensitivity analysis |
| Thiếu feedforward data (crime sau khi deployed) | Không validate impact thực | Đề xuất framework đánh giá sau 6 tháng |

---

## 🔗 Điều hướng

- [[30 - Predictive Analytics|← Phase 3: Predictive]]
- [[90 - Progress Log|→ Progress Log]]
- [[00 - Home|🏠 Home]]
