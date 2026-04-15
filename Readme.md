# Predictive Guardians Dashboard

Hệ thống phân tích tội phạm đô thị dựa trên dữ liệu thực tế từ **Cảnh sát Bang Karnataka, Ấn Độ**.

---

## 1. Yêu cầu hệ thống

- **Python:** Phiên bản **3.11** (Bắt buộc. Các phiên bản 3.12+ có thể gây lỗi Pillow/Folium trên Windows).
- **Java:** **JDK 8** trở lên (Bắt buộc cho H2O AutoML — dùng bởi pipeline training, không cần khi chỉ xem dashboard).
- **RAM:** Tối thiểu 4GB (Khuyến nghị 8GB).

---

## 2. Cài đặt & Chạy ứng dụng

### 2.1. Cài đặt môi trường
Dự án yêu cầu **Python 3.11**. Việc sử dụng các phiên bản cao hơn (3.12+) có thể gây lỗi tương thích với một số thư viện trực quan hóa.

```powershell
# 1. Tạo môi trường ảo
python -m venv venv

# 2. Kích hoạt môi trường (Windows)
.\venv\Scripts\activate

# 3. Cài đặt các thư viện cần thiết
pip install -r requirements.txt
```

### 2.2. Khởi chạy Dashboard
Dashboard đã được cấu hình để đọc dữ liệu đã xử lý sẵn trong thư mục `data/processed/`.

```powershell
# Chạy dashboard từ thư mục gốc của dự án
streamlit run app/app.py
```
Ứng dụng sẽ khả dụng tại địa chỉ: `http://localhost:8501`.

### 2.3. Chạy Pipeline xử lý dữ liệu (ETL)
Nếu bạn cập nhật dữ liệu mới trong `data/raw/` hoặc muốn phân tích sâu hơn:

```powershell
# Chạy quy trình Tiền xử lý dữ liệu & Phân tích
python pipelines/data_processing_pipeline.py
```

---

## 3. Cấu trúc dự án

```
├── app/                          # Streamlit UI (Phần giao diện)
├── docs/                         # Trung tâm tài liệu (Obsidian Vault)
│   ├── 00 - Home.md              # Trang chủ tài liệu
│   ├── 02 - Metadata Dataset.md  # Giải thích dữ liệu chi tiết
│   └── ...
├── data/                         # Trung tâm quản lý dữ liệu
│   ├── raw/                      # Dữ liệu gốc (FIR_Details_Data.csv, v.v.)
│   └── processed/                # Dữ liệu đã làm sạch (CSV) — dashboard đọc từ đây
│
├── ingestion/                    # Giai đoạn 1: Ingest dữ liệu thô
├── preprocessing/                # Giai đoạn 2: Cleaning & Feature Engineering
├── documentation/                # (Nếu có) Tài liệu báo cáo chi tiết
├── optimization/                 # Giai đoạn 4: Logic tối ưu hóa nguồn lực (Resource Allocation)
│
├── models/                       # Lưu trữ các file mô hình đã huấn luyện (.pkl, .mojo)
├── pipelines/                    # Pipeline tự động hóa training
├── Data_Dictionary_VN.md         # Giải thích thuật ngữ bằng tiếng Việt
└── Readme.md                     # File này
```

---

## 4. Giải thích Dữ liệu — Tại sao lấy những gì, lọc như thế nào?

Phần này được viết lại theo đúng cách dự án đang vận hành hiện tại: **đi từ câu hỏi nghiệp vụ → chọn dữ liệu tối thiểu cần thiết → làm sạch → tạo bảng processed → đưa vào dashboard**.  
Mục tiêu là để người đọc nhìn vào README có thể hình dung ngay “dự án chảy như thế nào” trước, rồi mới đi sâu vào logic phân tích của từng module.

### 4.1. Bức tranh lớn: dữ liệu đi qua dự án như thế nào?

#### Bước 1. Bắt đầu từ dữ liệu gốc

Nguồn chính của toàn bộ hệ thống là **Karnataka State Police (KSP)**:
- `data/raw/FIR_Details_Data.csv`: bộ FIR lớn nhất, khoảng **570MB**, chứa hơn **1.6 triệu hồ sơ**.

Ngoài ra, module hồ sơ tội phạm dùng thêm 3 bảng phụ:
- `data/raw/AccusedData.csv`: thông tin nhân khẩu học của nghi phạm.
- `data/raw/MOBsData.csv`: phương thức gây án.
- `data/raw/RowdySheeterDetails.csv`: danh sách đối tượng nguy cơ cao / có tiền án.

#### Bước 2. Mỗi module chỉ lấy đúng phần dữ liệu nó cần

Dự án không nạp toàn bộ cột cho mọi nơi. Thay vào đó, mỗi module có một câu hỏi riêng:
- `Crime Pattern Analysis`: Tội phạm xảy ra ở đâu, khi nào, có hotspot nào?
- `Criminal Profiling`: Nhóm nghi phạm có đặc điểm gì, liên hệ với loại tội ra sao?
- `Case Outcome Monitoring`: Hệ thống xử lý án hiệu quả đến đâu?
- `Police Resource Allocation`: Nên dồn lực lượng vào beat nào, theo mức độ rủi ro nào?

Vì vậy, trong `ingestion/`, từng script chỉ chọn các cột trực tiếp phục vụ câu hỏi đó. Cách làm này giúp:
- Giảm bộ nhớ khi đọc file gốc rất lớn.
- Giảm nhiễu trong pipeline.
- Làm cho từng bảng `processed` có ý nghĩa rõ ràng, dễ kiểm tra hơn.

#### Bước 3. Làm sạch theo 2 tầng

Pipeline hiện tại đi theo hai tầng:

1. `ingestion/`
   Mục tiêu: lấy đúng cột cần dùng cho từng bài toán.

2. `preprocessing/`
   Mục tiêu: chuẩn hóa tên cột, loại dữ liệu lỗi, gom nhóm nghiệp vụ, tạo feature mới và xuất ra `data/processed/`.

#### Bước 4. Dashboard chỉ đọc dữ liệu đã xử lý

Giao diện Streamlit trong `app/` không tự làm lại cleaning nặng mỗi lần mở. Nó chủ yếu đọc các file trong `data/processed/`, ví dụ:
- `Crime_Pattern_Analysis_Cleaned.csv`
- `Criminal_Profiling_cleaned.csv`
- `Case_Outcome_Cleaned.csv`
- `Resource_Allocation_Cleaned.csv`

Riêng phần phân bổ nguồn lực hiện tại có thêm một bước runtime:
- Lần đầu chạy, app có thể tạo `Patrol_Reference_Cleaned.csv` từ FIR gốc để tách riêng các điểm phù hợp tuần tra thực địa.
- Các lần sau sẽ đọc lại file này để tăng tốc.

### 4.2. Roadmap xử lý dữ liệu của dự án

Có thể hình dung toàn bộ dự án theo lộ trình sau:

1. **Thu thập nguồn gốc**
   Dữ liệu FIR là xương sống; các bảng nghi phạm/MOB/rowdy là dữ liệu bổ sung cho bài toán profiling.

2. **Tách câu hỏi thành 4 module**
   Mỗi module tương ứng với một quyết định nghiệp vụ cụ thể, nên dữ liệu được cắt theo nhu cầu phân tích thay vì giữ nguyên trạng.

3. **Chọn cột tối thiểu cần thiết**
   Chỉ giữ những gì trực tiếp phục vụ thống kê, trực quan hóa, hoặc tối ưu hóa.

4. **Làm sạch dữ liệu nền**
   Loại bản ghi trùng, xử lý tên quận/đơn vị, lọc giá trị vô lý, chuẩn hóa nhóm tội.

5. **Tạo feature phục vụ quyết định**
   Ví dụ: `Case_Outcome`, `Victim_Minor`, `Normalised Crime Severity`, hotspot coordinates, trọng số tuần tra.

6. **Xuất sang dữ liệu processed**
   Sau cleaning, từng module có một bảng riêng, đủ nhẹ để dashboard load nhanh và ổn định.

7. **Phân tích mô tả trước, tối ưu sau**
   Dự án cố ý đi từ “hiểu dữ liệu” sang “ra quyết định”:
   - Crime Pattern và Criminal Profiling để hiểu bối cảnh.
   - Case Outcome để hiểu hiệu quả hệ thống.
   - Resource Allocation để biến insight thành hành động phân bổ lực lượng.

### 4.3. Quy tắc cleaning chung

Đây là các quy tắc lặp lại nhiều lần trong codebase:

| Quy tắc | Tại sao cần | Áp dụng ở đâu |
|---------|-------------|---------------|
| `drop_duplicates()` | Dữ liệu FIR và dữ liệu hồ sơ có nhiều dòng lặp; nếu giữ lại sẽ làm phồng số vụ, số nghi phạm hoặc số nạn nhân | Hầu hết module |
| Loại bỏ `CID`, `ISD Bengaluru`, `Coastal Security Police` | Đây là đơn vị đặc thù, không đại diện cho quận địa lý thông thường nên dễ làm sai so sánh theo địa bàn | Resource Allocation, Case Outcome |
| Chuẩn hóa `District_Name` theo mapping | Tên quận/đơn vị trong dữ liệu gốc không luôn khớp với tên dùng trong dashboard hoặc bảng biên chế | Resource Allocation, Crime Pattern, Case Outcome |
| Giữ lại đúng dải tuổi hợp lý | Tuổi quá nhỏ, bằng 0 hoặc quá lớn thường là lỗi nhập liệu; nếu không lọc sẽ làm méo phân tích profiling | Criminal Profiling |
| Chuẩn hóa / gom nhóm `CrimeGroup_Name` | Dữ liệu gốc có quá nhiều nhóm tội chi tiết; cần gom thành nhóm đọc được và so sánh được | Resource Allocation, Case Outcome |
| Tách feature nghiệp vụ mới từ cột gốc | Dữ liệu gốc thường quá chi tiết hoặc quá nhiễu; dashboard cần các biến đã quy đổi sẵn để hiển thị ổn định | Tất cả module |

### 4.4. Dự án đang chọn dữ liệu theo nguyên tắc nào?

Nguyên tắc xuyên suốt là:

- **Không lấy dữ liệu vì “có sẵn”, mà chỉ lấy vì nó trả lời được một câu hỏi.**
- **Không giữ dữ liệu thô trong dashboard nếu có thể đẩy việc chuẩn hóa xuống preprocessing.**
- **Không cố tối ưu quá sớm bằng mô hình phức tạp nếu dữ liệu nền chưa đủ sạch hoặc chưa đủ diễn giải được.**

Nói cách khác, đây là một dự án được xây theo hướng:

1. Hiểu được dữ liệu.
2. Tin được dữ liệu.
3. Mới dùng dữ liệu để khuyến nghị hành động.

### 4.5. Phân tích chuyên sâu theo từng module

#### Module 1: Crime Pattern Analysis

**Câu hỏi nghiệp vụ:** Tội phạm tập trung ở đâu, khi nào, và có điểm nóng không?

**Nguồn chính:** `FIR_Details_Data.csv`

**Những cột được lấy:**

| Cột | Vai trò trong module | Tại sao cần |
|-----|----------------------|-------------|
| `District_Name` | Đơn vị địa lý cấp quận | Vẽ choropleth và so sánh theo địa bàn |
| `UnitName` | Đơn vị cảnh sát | Liên kết với vị trí đồn và cụm điểm |
| `FIRNo` | Định danh hồ sơ | Tránh đếm sai số vụ |
| `Year`, `Month`, `FIR_Reg_DateTime` | Trục thời gian | Phân tích xu hướng theo năm/tháng/ngày |
| `CrimeGroup_Name` | Loại tội | Bộ lọc và phân tách hotspot theo nhóm tội |
| `Latitude`, `Longitude` | Tọa độ hiện trường | Vẽ heatmap và DBSCAN |
| `Distance from PS` | Mô tả khoảng cách/hướng từ đồn | Dùng để ước tính lại tọa độ khi bị thiếu |
| `VICTIM COUNT`, `Accused Count` | Quy mô vụ việc | Làm giàu ngữ cảnh khi phân tích điểm nóng |

**Logic xử lý nổi bật:**
- Dữ liệu tọa độ trong FIR gốc thiếu khá nhiều hoặc không đáng tin.
- Pipeline dùng vị trí đồn cảnh sát cộng với thông tin hướng/khoảng cách trong `Distance from PS` để nội suy tọa độ xấp xỉ.
- Sau đó mới đưa vào heatmap và DBSCAN để tìm hotspot thực tế hơn.

**Ý nghĩa với dự án:**
- Đây là lớp “nhìn bản đồ để biết chuyện gì đang xảy ra”.
- Nó trả lời câu hỏi nền tảng trước khi bàn đến phân bổ lực lượng.

---

#### Module 2: Criminal Profiling

**Câu hỏi nghiệp vụ:** Nhóm nghi phạm có đặc điểm gì, và những đặc điểm đó liên hệ thế nào với loại tội?

**Nguồn chính:**
- `AccusedData.csv`
- `MOBsData.csv`
- `RowdySheeterDetails.csv`

**Cách ghép dữ liệu hiện tại:**
- `inner join` theo khóa: `(District_Name, Unit_Name, Name)`

**Những cột được giữ lại:**

| Cột | Vai trò trong module | Tại sao cần |
|-----|----------------------|-------------|
| `age` | Tuổi nghi phạm | Nhìn phân bố tuổi, nhóm tuổi rủi ro |
| `Sex` | Giới tính | So sánh cấu trúc nam/nữ |
| `Caste` | Yếu tố xã hội | Làm biến mô tả bối cảnh xã hội |
| `Occupation` | Nghề nghiệp | Xem tương quan nghề - loại tội |
| `Crime_Group1` | Nhóm tội chính | Trục phân tích trung tâm |
| `Crime_Head2` | Loại tội chi tiết | Drill-down chuyên sâu |
| `Rowdy_Classification_Details`, `Activities_Description`, `PrevCase_Details` | Tiền sử và mức độ nguy cơ | Bổ sung chiều sâu cho hồ sơ nghi phạm |
| `PresentAddress`, `PresentCity`, `Year`, `Month` | Bối cảnh không gian - thời gian | Dùng khi cần cắt lớp thêm theo thời gian/địa bàn |

**Logic xử lý nổi bật:**
- Lọc tuổi trong khoảng hợp lý để bỏ lỗi nhập liệu.
- Đổi tên cột giữa các bảng để chuẩn hóa khóa join.
- Chỉ giữ các bản ghi khớp ở cả 3 nguồn, vì mục tiêu của module là “hồ sơ đủ thông tin”, không phải thống kê toàn dân số nghi phạm.

**Ý nghĩa với dự án:**
- Đây là lớp “hiểu con người phía sau vụ án”.
- Nó giúp tạo bối cảnh xã hội học cho các biểu đồ crime pattern và case outcome.

---

#### Module 3: Case Outcome Monitoring

**Câu hỏi nghiệp vụ:** Hệ thống xử lý án đang hiệu quả đến đâu, nghẽn ở đâu, và nhóm tội nào khó xử lý nhất?

**Nguồn chính:** `FIR_Details_Data.csv`

**Những cột được lấy:**

| Cột | Vai trò trong module | Tại sao cần |
|-----|----------------------|-------------|
| `District_Name`, `UnitName` | Địa bàn và đơn vị xử lý | So sánh hiệu quả theo quận/đơn vị |
| `FIR_YEAR`, `FIR_MONTH` | Trục thời gian | Theo dõi xu hướng xử lý theo năm/tháng |
| `FIR Type` | Mức nghiêm trọng | Tách Heinous và Non-Heinous |
| `FIR_Stage` | Trạng thái hồ sơ | Suy ra kết cục vụ án |
| `Complaint_Mode` | Kênh phát hiện/tiếp nhận | Đánh giá vai trò tiếp nhận tố giác và tuần tra |
| `CrimeGroup_Name` | Nhóm tội | So sánh loại tội nào khó kết án, khó phá |
| `Male`, `Female`, `Boy`, `Girl`, `Age 0`, `VICTIM COUNT` | Hồ sơ nạn nhân | Phân tích cơ cấu nạn nhân |
| `Accused Count`, `Arrested Male`, `Arrested Female`, `Arrested_Count` | Tình trạng bắt giữ | Theo dõi năng lực điều tra - bắt giữ |
| `Accused_ChargeSheeted Count`, `Conviction Count` | Kết quả tư pháp | Đo hiệu quả xử lý sau điều tra |

**Logic xử lý nổi bật:**
- Gom `FIR_Stage` thành các nhóm đọc được hơn như `Convicted`, `Pending Trial`, `Undetected`, `Discharged/Acquitted`, `Other`.
- Gộp thông tin nạn nhân thành các nhóm phục vụ dashboard: nam trưởng thành, nữ trưởng thành, trẻ vị thành niên.
- Chuẩn hóa nhóm tội để so sánh được giữa các biểu đồ thay vì giữ hàng trăm nhãn rời rạc.

**Ý nghĩa với dự án:**
- Đây là lớp “hậu kiểm”: không chỉ biết tội phạm xảy ra ở đâu, mà còn biết hệ thống tư pháp phản ứng ra sao.
- Nó tạo cầu nối giữa phân tích mô tả và quyết định phân bổ nguồn lực.

---

#### Module 4: Police Resource Allocation

**Câu hỏi nghiệp vụ:** Nếu phải phân bổ lực lượng cảnh sát, nên ưu tiên beat nào và theo logic nào?

**Nguồn chính hiện tại:**
- `FIR_Details_Data.csv`
- `data/raw/police_sanction_strength.csv` (biên chế ASI/CHC/CPC theo quận, đã tách khỏi code)

**Những cột được lấy trong preprocessing:**

| Cột | Vai trò trong module | Tại sao cần |
|-----|----------------------|-------------|
| `District_Name` | Quận nguồn | Map sang tên quận chuẩn và bảng biên chế |
| `UnitName` | Đồn cảnh sát | Đơn vị triển khai lực lượng |
| `Village_Area_Name` | Khu vực nhỏ | Gắn với địa bàn cụ thể trong beat |
| `Beat_Name` | Tuyến tuần tra | Đơn vị nhỏ nhất để phân bổ |
| `FIRNo` | Số hồ sơ | Đếm tổng số vụ theo beat |
| `CrimeGroup_Name` | Nhóm tội gốc | Quy đổi sang mức độ nghiêm trọng và loại tội tuần tra |

**Feature được tạo trong preprocessing:**

| Feature | Ý nghĩa |
|---------|---------|
| `Total Crimes per beat` | Tổng số vụ trên từng beat |
| `Crime Severity per Beat` | Tổng điểm nghiêm trọng trên beat |
| `Normalised Crime Severity` | Mức nghiêm trọng chuẩn hóa trong nội bộ quận |
| `Sanctioned Strength of ...` | Biên chế ASI / CHC / CPC đọc từ CSV ngoài |

**Điểm mới theo trạng thái code hiện tại:**
- Bảng biên chế **không còn hardcode trong Python**; hiện được đọc từ `police_sanction_strength.csv`.
- Dashboard hiện tại còn lọc riêng các điểm **phù hợp tuần tra thực địa**:
  - Giữ các nhóm tội như đánh nhau, gây rối, trộm/cướp, tai nạn, tệ nạn, xâm nhập trái phép...
  - Loại các nhóm như cyber, gian lận tài chính, giả mạo hoặc các vụ không phù hợp tuần tra ngoài thực địa.
- Kết quả lọc này có thể được materialize thành `Patrol_Reference_Cleaned.csv` để tăng tốc lần chạy sau.

**Logic xử lý nổi bật:**
- `CrimeGroup_Name` được gom về nhóm nghiệp vụ lớn rồi gán trọng số severity.
- Mỗi beat được tính điểm rủi ro tương đối trong phạm vi quận.
- Bài toán phân bổ dùng **Linear Programming (PuLP)** để tối ưu dưới ràng buộc biên chế ASI, CHC, CPC.

**Ý nghĩa với dự án:**
- Đây là lớp “ra quyết định”.
- Nó biến dữ liệu lịch sử thành khuyến nghị hành động cụ thể: quận nào cần ưu tiên, beat nào cần giữ quân số, tuyến nào phù hợp tuần tra thực địa.

### 4.6. Tóm tắt: vì sao cấu trúc dữ liệu của dự án hợp lý?

Nếu đọc toàn bộ luồng trên theo thứ tự, có thể thấy dự án được thiết kế theo một trình tự khá tự nhiên:

1. **Có dữ liệu gốc rất lớn nhưng không dùng nguyên xi.**
2. **Mỗi module chỉ giữ phần dữ liệu phục vụ đúng một quyết định.**
3. **Cleaning không làm cho “đẹp dữ liệu”, mà để tránh trả lời sai câu hỏi nghiệp vụ.**
4. **Processed data là lớp trung gian giúp dashboard nhẹ, dễ bảo trì, dễ kiểm chứng.**
5. **Phần tối ưu nguồn lực chỉ xuất hiện sau khi đã có lớp mô tả, hồ sơ và hậu kiểm.**

Đó cũng là lý do phần dữ liệu của dự án không chỉ là “mô tả cột”, mà là một **roadmap xử lý để biến dữ liệu thô thành quyết định vận hành**.

---

## 5. Tham khảo thêm

- `docs/02 - Metadata Dataset.md` — Giải thích chi tiết hệ thống đẳng cấp Ấn Độ, nghề nghiệp, nhóm tội phạm bằng tiếng Việt.
