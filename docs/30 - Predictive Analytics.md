# 🔮 Phase 3: Predictive Analytics

> **Tags:** #predictive #phase3 #ML #forecasting
> **Trạng thái:** ✅ Hoàn thành
> **Câu hỏi cốt lõi:** *"Chuyện gì sẽ xảy ra? Ở đâu, bao nhiêu vụ, loại tội phạm gì?"*

---

## 🎯 Mục tiêu

Xây dựng các mô hình dự đoán để:
1. **Dự báo số lượng vụ án** theo thời gian và địa bàn
2. **Dự báo hotspot tội phạm** (khu vực nguy hiểm trong tương lai)
3. **Phân loại mức độ nghiêm trọng** của vụ án
4. **Dự báo khả năng phá án** (Case Resolution)

---

### ✅ Model 1: Repeat Offense Prediction (Recidivism)

**Mục tiêu:** Dự đoán khả năng tái phạm của đối tượng dựa trên đặc điểm nhân khẩu học.

- [x] Feature selection: `Age`, `Caste`, `Profession`, `District_Name`, `PresentCity`
- [x] Preprocessing: Frequency Encoding cho categorical data, StandardScaler cho numerical data
- [x] Training: **H2O AutoML** (huấn luyện tự động đa mô hình)
- [x] Best Model: **Stacked Ensemble** (kết hợp GBM, XGBoost, GLM...)
- [x] Deployment: Load MOJO model trong Streamlit app
- [x] Performance: Đạt độ chính xác cao trong việc phân loại đối tượng tái phạm (1) vs không tái phạm (0)

---

### ✅ Model 2: Crime Pattern Clustering

- [x] Thuật toán: **DBSCAN**
- [x] Input: `Latitude`, `Longitude`
- [x] Output: Các cụm (Clusters) điểm nóng tội phạm tự động
- [x] Trực quan hóa: Folium Map với marker cụm

---

## 📊 Model Results

### Recidivism Predictor (Stacked Ensemble)
| Metric | Value |
|---|---|
| Framework | H2O AutoML |
| Best Model | StackedEnsemble_BestOfFamily |
| Input Features | 5 |
| Deployment | MOJO |

---

## ⚠️ Lưu ý & Rủi ro Mô hình

| Rủi ro | Mô tả | Giải pháp |
|---|---|---|
| **Latitude/Longitude thiếu 69.7%** | Không thể spatial regression | Dùng District/Beat làm proxy địa lý |
| **Data leakage** | FIR_Stage biết sau khi xử lý | Chỉ dùng features có lúc FIR được nộp |
| **Class imbalance** | Heinous chỉ 11.5% | SMOTE, class_weight |
| **Beat_Name không chuẩn** | 6,771 unique nhưng thực chất ít hơn | Chuẩn hóa trước khi encode |
| **2024 data không đủ** | Chỉ có ~6 tháng | Loại khỏi training set |

---

## 🔗 Điều hướng

- [[20 - Diagnostic Analytics|← Phase 2: Diagnostic]]
- [[40 - Prescriptive Analytics|→ Phase 4: Prescriptive]]
