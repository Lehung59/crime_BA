# Predictive Guardians Dashboard

Dự án này là một hệ thống phân tích và dự đoán dữ liệu dựa trên Streamlit và H2O AutoML.

---

## 1. Yêu cầu hệ thống

Trước khi cài đặt, đảm bảo máy tính của bạn đáp ứng các yêu cầu sau:

- **Python:** Phiên bản **3.11** (Bắt buộc. Các phiên bản 3.12 hoặc 3.13 có thể gây lỗi thư viện đồ họa Pillow/Folium trên Windows).
- **Java:** **JDK 8** trở lên (Bắt buộc. Dùng để khởi chạy công cụ học máy H2O cho phần dự đoán).
- **Hệ điều hành:** Windows 10/11 (hoặc macOS/Linux có hỗ trợ Python/Java).
- **RAM:** Tối thiểu 4GB (Khuyến nghị 8GB do H2O cần khởi tạo máy ảo Java - JVM).

---

## 2. Cài đặt môi trường

Bạn nên sử dụng môi trường ảo (Virtual Environment) để tránh xung đột thư viện với các dự án khác trên máy. Thực hiện từng bước sau trong Terminal / PowerShell:

**Bước 1: Tạo môi trường ảo (ví dụ tên là `venv311`)**
```powershell
python -m venv venv311
```
*(Lưu ý: Đảm bảo lệnh `python` của bạn đang trỏ tới Python 3.11).*

**Bước 2: Kích hoạt môi trường ảo**
- Trên Windows:
  ```powershell
  .\venv311\Scripts\activate
  ```
- Trên macOS/Linux:
  ```bash
  source venv311/bin/activate
  ```

**Bước 3: Cài đặt các thư viện cần thiết**
```powershell
pip install -r requirements.txt
```

---

## 3. Chạy ứng dụng

Sau khi cài đặt xong tất cả thư viện, bạn thực hiện các bước sau để khởi chạy giao diện Dashboard:

**Bước 1: Kích hoạt lại môi trường ảo (nếu đã tắt Terminal trước đó)**
```powershell
.\venv311\Scripts\activate
```

**Bước 2: Di chuyển vào thư mục chứa mã nguồn giao diện (`app`)**
```powershell
cd app
```

**Bước 3: Chạy ứng dụng bằng Streamlit**
```powershell
python -m streamlit run app.py
```

Ứng dụng sẽ tự động mở trên trình duyệt của bạn với địa chỉ mặc định là: `http://localhost:8501`.

---

> **⚠️ Lưu ý quan trọng khi sử dụng ứng dụng:**
> Lần đầu tiên bạn click vào tab **Predictive Modeling** trên thanh công cụ, hệ thống sẽ mất khoảng **15 - 30 giây** để khởi tạo Java Virtual Machine (H2O Engine) và tải các model nặng vào bộ nhớ. Giao diện lúc này có thể sẽ hiện trạng thái *Loading*, vui lòng không tắt trang. Các lần bấm sau sẽ diễn ra rất nhanh do dữ liệu đã được lưu vào bộ nhớ đệm (cache).
