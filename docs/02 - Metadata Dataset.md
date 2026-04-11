# 📂 Metadata & Giải thích Hệ thống Dữ liệu (Dataset Explanation)

> **Thông tin:** Tài liệu này kết hợp thông tin kỹ thuật (metadata) và giải thích ngữ cảnh xã hội, pháp lý từ thực tế tại Karnataka, Ấn Độ để giúp hiểu sâu hơn về bộ dữ liệu dự án Crime Analytics.

---

## 📐 Thông tin Tổng quan (Overview)

| Thuộc tính | Giá trị |
|---|---|
| **Số dòng (records)** | 1,674,734 |
| **Số cột (features)** | 34 |
| **Giai đoạn dữ liệu** | 2016 – 2024 |
| **Nguồn dữ liệu** | Bang Karnataka, Ấn Độ (Cảnh sát Bang Karnataka - KSP) |

---

## 🗃️ Giải thích Chi tiết Từng Cột (Data Dictionary)

### 🏛️ 1. Nhóm Địa lý & Tổ chức (Geography & Administration)

| Cột | Mô tả | Chi tiết / Ngữ cảnh |
|---|---|---|
| `District_Name` | Tên quận/huyện | Có 41 đơn vị hành chính. `Bengaluru City` chiếm ~25% tổng số vụ án toàn bang. |
| `UnitName` | Tên đồn cảnh sát | Đơn vị trực tiếp tiếp nhận và xử lý FIR. Có 1,054 đồn. |
| `Beat_Name` | Khu vực tuần tra | **Beat** là đơn vị nhỏ nhất trong quản lý cảnh sát cơ sở (tuyến tuần tra). |
| `Latitude`, `Longitude` | Tọa độ địa lý | **⚠️ 69.7% bị thiếu.** Cần lưu ý khi vẽ bản đồ nhiệt (hotspot). |

### ⚖️ 2. Nhóm Phân loại Tội phạm & Pháp lý (Crime Classification)

| Cột | Mô tả | Giải thích Thuật ngữ |
|---|---|---|
| `FIR Type` | Loại FIR | **Heinous** (Cực kỳ nghiêm trọng) / **Non Heinous**. |
| `CrimeGroup_Name` | Nhóm tội lớn | (Xem chi tiết bảng bên dưới) |
| `FIR_Stage` | Giai đoạn xử lý | **Convicted** (Đã kết án), **Pending Trial** (Đang chờ xét xử), **Undetected** (Chưa phá án). |
| `Complaint_Mode` | Hình thức nộp đơn | **Written** (Văn bản), **Sue-moto** (Cảnh sát tự phát hiện - Tuần tra), **Oral** (Lời nói). |

#### 📖 Chi tiết một số loại tội đặc thù:
- **POCSO (Protection of Children from Sexual Offences):** Đạo luật bảo vệ trẻ em khỏi xâm hại tình dục. Xuất hiện trong cột `Crime Category`.
- **DACOITY:** Cướp có tổ chức. Luật Ấn Độ định nghĩa là vụ cướp do nhóm từ **5 người trở lên** thực hiện.
- **SLL (Special and Local Laws):** Các tội danh theo luật riêng của bang/địa phương, khác với Bộ luật Hình sự Ấn Độ (IPC).
- **DOWRY (Của hồi môn):** Các tội phạm liên quan đến tranh chấp hoặc bạo hành do của hồi môn (thường gặp trong `CRIMES AGAINST WOMEN`).

---

## 👥 3. Đặc điểm Nhân khẩu học (Sociological Context)

Đây là phần quan trọng nhất để hiểu về bối cảnh xã hội của dữ liệu.

### 🕉️ Hệ thống Đẳng cấp (Caste)
Dữ liệu ghi nhận chi tiết cột `Caste`, phản ánh sự phân tầng xã hội sâu sắc tại Ấn Độ:
1. **SC (Scheduled Castes) & ST (Scheduled Tribes):** Các giai cấp và bộ lạc chịu thiệt thòi (ví dụ: *ADI KARNATAKA*, *NAYAKA*). Thường có tỷ lệ dính líu đến tội phạm cao do nghèo đói và thiếu giáo dục.
2. **OBC (Other Backward Classes):** Giai cấp cấp thấp khác nhưng đã có vị thế kinh tế/chính trị nhất định (ví dụ: *VOKKALIGA*, *LINGAYATH*).
3. **Forward Castes:** Các tầng lớp cao cấp (Brahmin, Kshatriya) ít xuất hiện trong hồ sơ tội phạm phổ thông/đường phố.

> **💡 Insight từ H2O AutoML:** Mô hình dự đoán **Tái phạm (Recidivism)** đánh trọng số cao vào `Caste` và `Occupation`, phản ánh mối tương quan giữa điều kiện kinh tế-xã hội và hành vi phạm tội.

### 🔨 Nghề nghiệp (Occupation/Profession)
- **Labourer (Lao động tự do):** Nhóm chiếm tỷ trọng cao nhất. Sức ép sinh tồn là nguyên nhân chính dẫn đến trộm cắp hoặc bạo lực.
- **Farmer (Nông dân):** Thường liên quan đến bạo lực do tranh chấp đất đai hoặc bạo lực gia đình ở nông thôn.
- **Driver (Tài xế):** Thường dính vào các vụ vi phạm giao thông hoặc đụng độ trên đường phố.

---

## ⚠️ Vấn đề Chất lượng Dữ liệu (Data Quality)

1. **Latitude/Longitude thiếu 70%:** Hạn chế lớn nhất cho phân tích không gian (GIS).
2. **Beat_Name không chuẩn hóa:** Dữ liệu cùng 1 beat có thể viết khác nhau (BEAT 1 vs Beat 1), cần tiền xử lý (cleaning).
3. **Outliers thời gian:** Một số vụ án có `Offence_Duration` bất thường (hàng chục năm).

---

## 🔗 Liên kết Tài liệu
- [[01 - Ke hoach thuc hien|← Kế hoạch thực hiện]]
- [[10 - Descriptive Analytics|→ Phân tích Mô tả]]
- [[95 - Code Cleanup Report|Báo cáo dọn dẹp Code]]
