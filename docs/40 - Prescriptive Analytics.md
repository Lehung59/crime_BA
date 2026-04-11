# 🎯 Phase 4: Prescriptive Analytics

> **Tags:** #prescriptive #phase4 #optimization #resource-allocation
> **Trạng thái:** ✅ Hoàn thành
> **Câu hỏi cốt lõi:** *"Chúng ta cần làm gì để tối ưu hóa phân bổ cảnh sát và giảm thiểu tội phạm?"*

---

## 🎯 Mục tiêu

Chuyển hóa các insights từ Phase 1-3 thành **hành động cụ thể**:
1. **Phân bổ cảnh sát tối ưu** theo Beat/District dựa trên Risk Score
2. **Lịch tuần tra tối ưu** theo giờ/ngày/tháng cao điểm
3. **Chiến lược phòng ngừa** theo loại tội phạm
4. **Dashboard hỗ trợ ra quyết định** cho chỉ huy cảnh sát

---

## 📋 Task List & Implementation

### ✅ Model: Police Resource Optimization (LP)

**Mục tiêu:** Tối ưu hóa phân bổ nhân lực (ASI, CHC, CPC) đến từng khu vực bằng thuật toán **Linear Programming** (PuLP).

- [x] Thu thập dữ liệu lực lượng hiện tại (từ `Resource_Allocation_Cleaned.csv`)
- [x] Xây dựng model bằng **PuLP Optimizer**.
- [x] Định nghĩa **Hàm mục tiêu**: Tối đa hóa tổng trọng số mức độ nghiêm trọng × số lượng cảnh sát được phân bổ.
- [x] Thiết lập các **Ràng buộc (Constraints)**:
  - Tổng số cảnh sát không vượt quá định biên (Sanctioned Strength) của quận.
  - Mỗi Beat phải có ít nhất 1 cảnh sát (Minimum coverage).
  - Phân bổ dựa trên mức độ nghiêm trọng chuẩn hóa (Normalised Severity).
- [x] Interactive Dashboard:
  - Cho phép chọn Quận/Huyện.
  - Điều chỉnh định biên (Sanctioned Strength) để xem kịch bản "What-if".
  - Hiển thị bảng phân bổ chi tiết cho ASI, CHC, CPC.

---

## 🚀 Kết quả Thực thi

| Tham số | Chi tiết |
|---|---|
| Framework | PuLP (Python Optimization Library) |
| Đối tượng phân bổ | ASI, CHC, CPC |
| Đơn vị đích | Police Unit / Beat |
| Input chính | Normalised Crime Severity Score |

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
