# 🚀 Lộ trình Phát triển Tiếp theo (Project Roadmap)

> **Mục tiêu:** Nâng cấp hệ thống Predictive Guardians từ mức độ đồ án lên mức độ ứng dụng thực tế chuyên nghiệp (Ready-to-use).

---

## 🎯 1. Giao diện & Trải nghiệm Người dùng (UX/UI)

- [ ] **Tab "Tổng quan Chiến lược" (Executive Dashboard):**
    - Xây dựng một trang tóm tắt các chỉ số KPIs quan trọng nhất (Top-down view).
    - Sử dụng `st.metric` để hiển thị biến động tội phạm so với tháng/năm trước.
- [ ] **Đa ngôn ngữ (Localization):**
    - Hoàn thiện việc chuyển đổi toàn bộ giao diện sang tiếng Việt (hiện tại một số biểu đồ Plotly vẫn dùng nhãn tiếng Anh).
- [ ] **Chế độ Dark/Light mode:** Tối ưu hóa CSS để giao diện trông cao cấp hơn trên mọi thiết bị.

## 🛠️ 2. Tính năng Nâng cao (Advanced Features)

- [ ] **Xuất báo cáo (Exporting):**
    - Thêm nút cho phép tải kết quả **Phân bổ nguồn lực** về tệp Excel hoặc PDF.
    - Tự động tạo bản tóm tắt (Summary Report) cho cấp quản lý.
- [ ] **Mô phỏng kịch bản (What-if Scenarios):**
    - Cho phép người dùng nhập các tình huống giả định (ví dụ: "Nếu giảm 20% biên chế tại Quận X thì rủi ro sẽ tăng bao nhiêu?").
- [ ] **Tích hợp bản đồ trực tiếp (Live Mapping):**
    - Thay thế bản đồ tĩnh bằng các bản đồ có khả năng drill-down sâu hơn vào từng khu phố nếu dữ liệu tọa độ được cải thiện.

## 🚀 4. Phân tích & Mô hình (Analytics & Models)

- [ ] **Mở rộng Phân tích Tương quan:** Tích hợp các kiểm định thống kê (như Cramer's V) để đo lường sức mạnh của các mối quan hệ nhân khẩu học.
- [ ] **Nâng cấp Cây Quyết định:** Tinh chỉnh các tham số để đạt độ chính xác cao hơn trong việc phân loại kịch bản `Heinous` của vụ án.
- [ ] **Xử lý dữ liệu tọa độ thiếu:** 
    - Geocoding dựa trên địa điểm thực tế để hoàn thiện bản đồ nhiệt (Heatmap).

## 🚀 4. Tổng kết & Báo cáo (Summary & Reporting)

- [ ] **Video Demo:** Quay video giới thiệu các luồng nghiệp vụ chính: *Phát hiện điểm nóng -> Phân tích hồ sơ -> Đề xuất chia quân.*
- [ ] **Tài liệu hướng dẫn (User Manual):** Viết hướng dẫn sử dụng nhanh dành cho cán bộ cảnh sát.
- [ ] **Slide thuyết trình:** Tổng hợp các insight quan trọng nhất từ 4 module phân tích.

---

## 📅 Lịch trình dự kiến (Estimation)

| Nhiệm vụ | Thời gian | Ưu tiên |
|---|---|---|
| Tab Executive Overview | 2 ngày | 🔴 Cao |
| Việt hóa 100% | 1 ngày | 🟡 Trung bình |
| Tính năng Xuất báo cáo | 3 ngày | 🔴 Cao |
| Xử lý tọa độ còn thiếu | 5 ngày | 🟢 Thấp |

---
**Predictive Guardians** — *Tương lai an toàn bắt đầu từ dữ liệu.*
