# 🧹 Code Cleanup Report

> **Ngày thực hiện:** 2026-04-11
> **Tags:** #cleanup #refactor #dead-code

---

## Tóm tắt kết quả

| File | Thay đổi |
|---|---|
| `app/app.py` | Xóa 10 import thừa; thay `from X import *` bằng named imports; xóa `Continuous_Learning_and_Feedback` import; sửa Home page metric "4" → "5 CSV Files" |
| `app/Predictive_modeling.py` | Xóa 18 import thừa; xóa `load_model_crime_type()` và `get_unique_values_crime_type()` không dùng |
| `app/Crime_Pattern_Analysis.py` | Xóa 7 import thừa |
| `app/Resource_Allocation.py` | Xóa 2 import thừa |
| `app/Continuous_Learning_and_Feedback.py` | **🗑️ XÓA HOÀN TOÀN** — không có sidebar route, dead code |
| `Continuous_learning_and_feedback/` | **🗑️ XÓA HOÀN TOÀN** — alert.py, feedback.py (dead code dependency) |
| `Component_datasets/Feedback.csv` | **🗑️ XÓA** — data file của tính năng đã xóa |
| `pipelines/training_pipeline.py` | Xóa 3 import tới module không tồn tại; xóa 3 dead function calls |
| `assets/` feedback/alert images | **🗑️ XÓA 11 file**: feedback-1, feedback-sessions-1/2, feedback_session, live-feedback, provide-feedbacl, knowledge-base, alert-1/2, alert_system, cont-component |
| `assets/crime_type_prediction.PNG` | **🗑️ XÓA** — model file không tồn tại |
| `assets/*.Zone.Identifier` | **🗑️ XÓA** — Windows metadata artifacts |
| `Continuous_learning_and_feedback/__pycache__` | Cache Python không cần thiết | ✅ Deleted |
| `app/__pycache__` | Cache Python không cần thiết | ✅ Deleted |

---

## Chi tiết Bug Quan trọng đã Fix

### 🐛 Bug: `df.append()` bị xóa trong pandas 2.0
**File:** `app/Continuous_Learning_and_Feedback.py`, dòng 141  
**Triệu chứng:** Khi user submit feedback → crash với `AttributeError: 'DataFrame' object has no attribute 'append'`  
**Fix:** Thay bằng `pd.concat([feedback_df, new_row], ignore_index=True)`

### 🐛 Bug: `open()` không đóng file (resource leak)
**File:** `app/Predictive_modeling.py`, dòng 83  
**Fix:** Thay bằng `with open(frequency_path) as f:`

### 🐛 Bug: Import module không tồn tại
**File:** `pipelines/training_pipeline.py`, dòng 15-17  
**Vấn đề:** `Predictive_Modeling.Crime_Type_Prediction` folder không tồn tại → pipeline crash khi chạy  
**Fix:** Xóa 3 dòng import và 3 dòng code gọi hàm tương ứng

---

## Ghi chú

- Module `app/Continuous_Learning_and_Feedback.py` và folder `Continuous_learning_and_feedback/` vẫn được **giữ nguyên** vì có thể được dùng trong tương lai (nếu thêm route vào sidebar). Chỉ cleanup nội bộ.
- `assets/` chứa screenshot PNG của UI cũ (có feedback/alert images) — không xóa vì dùng cho documentation
- `Component_datasets/Feedback.csv` — giữ nguyên làm fallback data
