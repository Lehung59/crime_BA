# 🔮 Phase 3: Predictive Analytics

> **Tags:** #predictive #phase3 #ML #forecasting
> **Trạng thái:** 🔲 Chưa bắt đầu
> **Câu hỏi cốt lõi:** *"Chuyện gì sẽ xảy ra? Ở đâu, bao nhiêu vụ, loại tội phạm gì?"*

---

## 🎯 Mục tiêu

Xây dựng các mô hình dự đoán để:
1. **Dự báo số lượng vụ án** theo thời gian và địa bàn
2. **Dự báo hotspot tội phạm** (khu vực nguy hiểm trong tương lai)
3. **Phân loại mức độ nghiêm trọng** của vụ án
4. **Dự báo khả năng phá án** (Case Resolution)

---

## 📋 Task List

### Model 1: Time-Series Forecasting (Crime Volume Prediction)

**Mục tiêu:** Dự báo số vụ án theo tháng, theo quận, trong 6-12 tháng tới

- [ ] Aggregate data: `District × CrimeGroup × Year-Month → Count`
- [ ] EDA seasonality: decomposition (trend, seasonal, residual)
- [ ] Train **Facebook Prophet** model:
  - Target: `crime_count`
  - Regressors: `month`, `district`, seasonality flags
- [ ] Train/Test split: Train đến 2022, Test 2023
- [ ] Đánh giá: MAE, MAPE, RMSE
- [ ] Forecast 12 tháng (2025)
- [ ] Visualize: forecast line + confidence interval

**Model Input:**
```
District × Month(year-month) → Predicted Crime Count
```

**Thư viện:** `prophet`, `statsmodels`, `sklearn`

---

### Model 2: Hotspot Classification (Beat Risk Scoring)

**Mục tiêu:** Phân loại Beat theo mức rủi ro (High / Medium / Low)

- [ ] Aggregate: `Beat_Name × District → crime_volume, heinous_rate, undetected_rate`
- [ ] Tính điểm tổng hợp (Composite Risk Score):
  - `Risk = 0.4×crime_volume_norm + 0.3×heinous_rate + 0.3×(1-detection_rate)`
- [ ] K-Means clustering (K=3: High/Medium/Low risk)
- [ ] Visualize clusters trên map (nếu có geo data) hoặc scatter plot
- [ ] Gán nhãn Risk Level cho mỗi Beat

**Output:** Danh sách Beat kèm Risk Level → Input cho Phase 4

---

### Model 3: Crime Severity Classification

**Mục tiêu:** Dự báo FIR Type (Heinous / Non-Heinous) từ features ban đầu

**Features sử dụng:**
- `CrimeGroup_Name` (encoded)
- `District_Name` (encoded)
- `FIR_MONTH`
- `Complaint_Mode`
- `Beat_Name` (encoded)
- `Accused Count`

**Steps:**
- [ ] Feature encoding (Label/One-Hot/Target Encoding)
- [ ] Train/Test split (80/20, stratified)
- [ ] Train **Random Forest Classifier**
- [ ] Train **XGBoost Classifier**
- [ ] Hyperparameter tuning (GridSearchCV hoặc Optuna)
- [ ] Đánh giá: Precision, Recall, F1 (focus: Heinous class)
- [ ] Confusion Matrix, ROC-AUC
- [ ] Feature Importance analysis

**Output:** Model phân loại mức độ nghiêm trọng + Feature Importance

---

### Model 4: Case Resolution Prediction (Có phá được án không?)

**Mục tiêu:** Dự đoán vụ án có bị "Undetected" không

**Target variable:** `is_undetected` (binary: 1 nếu FIR_Stage = Undetected, 0 nếu Convicted/Traced)

**Features:**
- `CrimeGroup_Name`
- `District_Name`
- `FIR_MONTH`, `FIR_YEAR`
- `Complaint_Mode`
- `IO_workload` (tính từ số vụ mỗi IOName)
- `Distance from PS` (parse numeric nếu có thể)
- `FIR Type`

**Steps:**
- [ ] Chuẩn bị target: lọc chỉ lấy vụ án đã kết thúc (Convicted, Undetected, Traced)
- [ ] Handle class imbalance (SMOTE hoặc class_weight)
- [ ] Train **Logistic Regression** (baseline)
- [ ] Train **Gradient Boosting (LightGBM)**
- [ ] Đánh giá: Recall cho class Undetected (cần nhạy với false negative)
- [ ] SHAP values để giải thích model

**Output:** Model + Dashboard cảnh báo vụ án có nguy cơ bị Undetected

---

## 📊 Model Comparison Table

| Model | Target | Algorithm | Metric | Status |
|---|---|---|---|---|
| Time-Series Forecast | Crime Count/Month | Prophet | MAPE | 🔲 |
| Hotspot Clustering | Beat Risk Level | K-Means | Silhouette | 🔲 |
| Severity Classification | Heinous/Non-Heinous | XGBoost | F1 (Heinous) | 🔲 |
| Resolution Prediction | Undetected (Y/N) | LightGBM | Recall | 🔲 |

---

## 📈 Model Results (điền khi hoàn thành)

### Time-Series Forecast
| Metric | Value |
|---|---|
| MAE | - |
| MAPE | - |
| RMSE | - |

### Severity Classifier
| Metric | Value |
|---|---|
| F1 (Heinous) | - |
| Precision | - |
| Recall | - |
| ROC-AUC | - |

### Resolution Predictor
| Metric | Value |
|---|---|
| Recall (Undetected) | - |
| Precision | - |
| F1 | - |

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
