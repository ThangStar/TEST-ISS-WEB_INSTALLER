# T2Tool – Công cụ hỗ trợ đa năng

T2Tool là một ứng dụng Windows tiện ích, cung cấp giao diện thân thiện và chức năng hữu ích cho người dùng. Bộ cài đặt sử dụng **trình cài đặt web (Web Installer)**, tải và giải nén ứng dụng từ máy chủ từ xa, giúp giảm kích thước file cài đặt ban đầu và dễ dàng cập nhật.

---

## ✨ Tính năng chính

- **Tự động tải ứng dụng từ máy chủ**: File chính (`test.exe`) được đóng gói trong file `.rar` và tải về trong quá trình cài đặt.
- **Tạo biểu tượng ngoài màn hình chính**: Tùy chọn tạo shortcut trên Desktop.
- **Khởi động cùng Windows**: Hỗ trợ bật/tắt tính năng tự khởi động khi bật máy.
- **Giao diện cài đặt đẹp mắt**: Sử dụng hình ảnh tùy chỉnh và icon chuyên nghiệp.
- **Yêu cầu quyền Admin**: Đảm bảo cài đặt ổn định vào thư mục chương trình mặc định của Windows.
- **Bảo trì dễ dàng**: Cấu trúc mã nguồn Inno Setup rõ ràng, dễ mở rộng và cập nhật.

---

## 📦 Cách sử dụng

1. **Tải bộ cài**:
   - Tên file: `T2Tool-WebInstaller-1.0.0.exe`
   - [Link mẫu trên GitHub Releases](https://github.com/ThangStar/TEST-ISS-WEB_INSTALLER/releases)

2. **Chạy file cài đặt**:
   - Chạy với quyền **Administrator** (bắt buộc).
   - Làm theo hướng dẫn trên màn hình.

3. **Cấu hình tùy chọn**:
   - ☑️ **Tạo biểu tượng trên &màn hình**: Thêm shortcut ra Desktop.
   - ☑️ **&Khởi động cùng Windows**: Tự động chạy T2Tool khi khởi động máy.

4. **Khởi chạy ứng dụng**:
   - Sau khi cài xong, bạn có thể chọn **Khởi chạy T2Tool** ngay lập tức.

---

## ⚙️ Yêu cầu hệ thống

- **Hệ điều hành**: Windows 7/8/10/11 (64-bit hoặc 32-bit)
- **Quyền truy cập**: Administrator (bắt buộc để viết vào `Program Files`)
- **Kết nối Internet**: Bắt buộc để tải file ứng dụng từ máy chủ

---

## 🛠 Cấu hình dành cho nhà phát triển

Nếu bạn muốn **tùy chỉnh hoặc build lại bộ cài**, hãy đảm bảo:

- Cấu trúc thư mục:
