# 📂 Metadata — FIR_Details_Data.csv

> **Nguồn:** `dataset/FIR_Details_Data.csv`
> **Tags:** #dataset #metadata #FIR #Karnataka

---

## 📐 Thông tin Cơ bản

| Thuộc tính | Giá trị |
|---|---|
| **Số dòng (records)** | 1,674,734 |
| **Số cột (features)** | 34 |
| **Giai đoạn dữ liệu** | 2016 – 2024 |
| **Đơn vị hành chính** | 41 quận (Districts) |
| **Đơn vị cảnh sát** | 1,054 đồn (UnitName) |
| **Khu vực tuần tra** | 6,771 Beat |
| **Phân loại tội phạm** | 107 nhóm (CrimeGroup), 474 đầu mục (CrimeHead) |

---

## 🗃️ Mô tả Chi tiết Từng Cột

### 🏛️ Nhóm Địa lý & Tổ chức

| Cột | Dtype | Unique | Null | Mô tả |
|---|---|---|---|---|
| `District_Name` | str | 41 | 0 | Tên quận/huyện trong bang Karnataka |
| `UnitName` | str | 1,054 | 0 | Tên đồn cảnh sát |
| `Unit_ID` | int64 | 1,074 | 0 | ID số của đồn cảnh sát |
| `Beat_Name` | str | 6,771 | 0 | Tên khu vực tuần tra (Beat = đơn vị nhỏ nhất) |
| `Village_Area_Name` | str | 16,989 | 0 | Tên làng/khu vực xảy ra vụ án |
| `Latitude` | float64 | 393,101 | **1,166,600** | Tọa độ vĩ độ — **⚠️ 69.7% giá trị bị thiếu** |
| `Longitude` | float64 | 396,293 | **1,166,635** | Tọa độ kinh độ — **⚠️ 69.7% giá trị bị thiếu** |
| `Place of Offence` | str | 1,290,842 | 0 | Mô tả cụ thể địa điểm xảy ra (dạng free text) |
| `Distance from PS` | str | 416,015 | 0 | Khoảng cách từ địa điểm tội phạm đến đồn cảnh sát |

### 📅 Nhóm Thời gian

| Cột | Dtype | Unique | Null | Mô tả |
|---|---|---|---|---|
| `FIR_YEAR` | int64 | 9 | 0 | Năm nộp FIR (2016–2024) |
| `FIR_MONTH` | int64 | 12 | 0 | Tháng nộp FIR (1–12) |
| `FIR_Day` | int64 | 31 | 0 | Ngày nộp FIR (1–31) |
| `Offence_Duration` | int64 | 7,691 | 0 | Thời gian kéo dài vụ phạm tội (ngày); có 4 giá trị âm |

> **Lưu ý:** Offence_Duration trung bình ~74 ngày nhưng phần vị 75th = 0 → phần lớn vụ án xảy ra tức thời (trong ngày). Một số vụ kéo dài tới 44,195 ngày (outlier lớn).

### ⚖️ Nhóm Phân loại Tội phạm & Pháp lý

| Cột | Dtype | Unique | Null | Mô tả |
|---|---|---|---|---|
| `FIR Type` | str | 2 | 0 | Loại FIR: `Heinous` (nghiêm trọng) / `Non Heinous` |
| `CrimeGroup_Name` | str | 107 | 0 | Nhóm tội phạm lớn |
| `CrimeHead_Name` | str | 474 | 0 | Đầu mục tội phạm chi tiết |
| `ActSection` | str | 220,716 | 0 | Điều luật áp dụng (IPC, SLL...) |
| `FIR_Stage` | str | 343 | 0 | Giai đoạn xử lý vụ án (Pending Trial, Convicted...) |

### 👮 Nhóm Điều tra & Nhân sự

| Cột | Dtype | Unique | Null | Mô tả |
|---|---|---|---|---|
| `IOName` | str | 24,422 | 0 | Tên sĩ quan điều tra (Investigating Officer) |
| `KGID` | str | 29,844 | 0 | ID định danh của sĩ quan điều tra |
| `Internal_IO` | int64 | 26,398 | 0 | Mã nội bộ IO |
| `Complaint_Mode` | str | 10 | 0 | Cách thức nộp đơn (Written, Oral, Online...) |

### 👥 Nhóm Nạn nhân

| Cột | Dtype | Unique | Null | Phân tích |
|---|---|---|---|---|
| `Male` | int64 | 39 | 0 | Số nạn nhân nam (tổng: 888,251) |
| `Female` | int64 | 43 | 0 | Số nạn nhân nữ (tổng: 388,140) |
| `Boy` | int64 | 25 | 0 | Số nạn nhân nam trẻ em (tổng: 44,416) |
| `Girl` | int64 | 23 | 0 | Số nạn nhân nữ trẻ em (tổng: 67,245) |
| `Age 0` | int64 | 33 | 0 | Số nạn nhân không rõ tuổi/không xác định |
| `VICTIM COUNT` | int64 | 9 | 0 | Tổng nạn nhân |

> **Insight:** Tỷ lệ nạn nhân nam >> nữ (888K vs 388K). Trẻ em gái bị ảnh hưởng nhiều hơn trẻ em trai (67K vs 44K) — gợi ý tội phạm POCSO và bóc lột trẻ em gái.

### 🔒 Nhóm Kết quả Điều tra

| Cột | Dtype | Unique | Null | Mô tả |
|---|---|---|---|---|
| `Accused Count` | int64 | 130 | 0 | Số người bị tình nghi |
| `Arrested Male` | int64 | 89 | 0 | Số nam bị bắt |
| `Arrested Female` | int64 | 25 | 0 | Số nữ bị bắt |
| `Arrested Count No.` | int64 | 90 | 0 | Tổng số người bị bắt |
| `Accused_ChargeSheeted Count` | int64 | 127 | 0 | Số người bị truy tố/truy cứu |
| `Conviction Count` | int64 | 50 | 0 | Số người bị kết án |

---

## 📊 Phân tích Thống kê Quan trọng

### Phân bố Năm (FIR_YEAR)

| Năm | Số vụ | Ghi chú |
|---|---|---|
| 2016 | 227,717 | |
| 2017 | 246,839 | 📈 Đỉnh cao nhất |
| 2018 | 219,447 | |
| 2019 | 175,486 | |
| 2020 | 160,547 | 📉 Giảm — COVID-19 |
| 2021 | 175,857 | |
| 2022 | 195,170 | |
| 2023 | 231,326 | 📈 Phục hồi cao |
| 2024 | 42,345 | ⚠️ Dữ liệu chưa đủ năm |

### Top 10 Quận Nhiều Vụ Án Nhất

| Quận | Số vụ |
|---|---|
| Bengaluru City | 425,408 (25.4%) |
| Bengaluru Dist | 64,004 |
| Tumakuru | 61,553 |
| Shivamogga | 61,338 |
| Mandya | 59,701 |
| Belagavi Dist | 59,569 |
| Hassan | 58,256 |
| Mysuru Dist | 50,599 |
| Chitradurga | 47,754 |
| Ramanagara | 44,232 |

> **Insight:** Bengaluru City chiếm 25.4% toàn bộ số vụ án — hotspot tập trung cực kỳ cao.

### Top 15 Nhóm Tội phạm (CrimeGroup_Name)

| Nhóm | Số vụ |
|---|---|
| MOTOR VEHICLE ACCIDENTS NON-FATAL | 242,976 |
| THEFT | 159,021 |
| CrPC | 137,939 |
| CASES OF HURT | 126,211 |
| MISSING PERSON | 124,811 |
| KARNATAKA POLICE ACT 1963 | 107,576 |
| Karnataka State Local Act | 90,742 |
| MOTOR VEHICLE ACCIDENTS FATAL | 83,040 |
| CYBER CRIME | 78,502 |
| CHEATING | 48,675 |
| MOLESTATION | 42,856 |
| PUBLIC SAFETY | 42,380 |
| RIOTS | 36,695 |
| BURGLARY - NIGHT | 35,729 |
| NARCOTIC DRUGS & PSYCHOTROPIC SUBSTANCES | 27,856 |

### Phân loại FIR

| Loại | Số vụ | % |
|---|---|---|
| Non Heinous | 1,482,992 | 88.5% |
| Heinous | 191,742 | 11.5% |

### Trạng thái Xử lý (FIR_Stage — Top 10)

| Trạng thái | Số vụ |
|---|---|
| Pending Trial | 498,324 |
| Convicted | 343,660 |
| Undetected | 188,150 |
| Dis/Acq (Dismissed/Acquitted) | 134,001 |
| Bound Over | 111,480 |
| Traced | 111,024 |
| Under Investigation | 95,582 |
| False Case | 84,726 |
| Compounded | 49,673 |
| Other Disposal | 29,492 |

### Cách Nộp Đơn (Complaint_Mode)

| Phương thức | Số vụ |
|---|---|
| Written (Bằng văn bản) | 1,112,118 (66.4%) |
| Sue-moto by Police (Cảnh sát tự phát hiện) | 269,430 (16.1%) |
| Oral (Trực tiếp) | 143,224 (8.6%) |
| Others | 98,993 |
| Online | 5,028 |

---

## ⚠️ Vấn đề Chất lượng Dữ liệu

| Vấn đề | Mức độ | Ghi chú |
|---|---|---|
| Latitude/Longitude thiếu 69.7% | 🔴 Nghiêm trọng | Hạn chế phân tích địa lý trực tiếp |
| Offence_Duration âm (4 records) | 🟢 Nhỏ | Cần lọc bỏ |
| Beat_Name không chuẩn hóa | 🟡 Trung bình | "BEAT 1" vs "Beat 1" vs "1" là cùng một beat |
| Place of Offence free-text | 🟡 Trung bình | Không thể dùng trực tiếp cho phân tích |
| FIR_Stage có 343 giá trị unique | 🟡 Trung bình | Cần nhóm lại thành các stage chính |
| 2024 data chưa đủ (6 tháng) | 🟡 Trung bình | Loại khỏi trend analysis dài hạn |

---

## 🔗 Liên kết

- [[01 - Ke hoach thuc hien|← Về Kế hoạch]]
- [[10 - Descriptive Analytics|→ Bắt đầu Descriptive Analysis]]
